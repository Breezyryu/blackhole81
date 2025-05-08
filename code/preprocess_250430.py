import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import tkinter as tk
from tkinter import filedialog
import bisect

def extract_capacity(folder_path):
    """
    Extract the capacity (mAh) from the top level folder path.
    
    Args:
        folder_path (str): Path to the top level folder
        
    Returns:
        int: Capacity value in mAh
    """
    # Get the top level folder name
    top_folder = os.path.basename(os.path.normpath(folder_path))
    
    # Use regex to find the number before "mAh"
    match = re.search(r'(\d+)mAh', top_folder)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Could not extract capacity from folder name: {top_folder}")


def set_pne_paths():
    """
    Set up paths for PNE data processing using a file dialog.
    
    Returns:
        tuple: Tuple containing cyclename, cyclepath, and mincapacity lists
    """
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Ask user to select the TXT file
    try:
        # Try to use D:/Work_pc_D/datapath directory first
        datafilepath = filedialog.askopenfilename(initialdir=r"D:/Work_pc_D/datapath", title="Choose Test files", filetypes=[("Text files", "*.txt")])
    except:
        # Fall back to home directory if the specified directory is not accessible
        datafilepath = filedialog.askopenfilename(initialdir=os.path.expanduser("~"), title="Choose Test files", filetypes=[("Text files", "*.txt")])
    
    if not datafilepath:
        raise ValueError("No file selected")
    
    # Read the CSV file with tab separator
    df = pd.read_csv(datafilepath, sep="\t", engine="c", encoding="UTF-8", 
                    skiprows=1, on_bad_lines='skip')
    
    # Extract cyclename and cyclepath
    cyclename = df['cyclename'].tolist() if 'cyclename' in df.columns else []
    cyclepath = df['cyclepath'].tolist() if 'cyclepath' in df.columns else []
    
    # Extract capacity from each cyclepath to create mincapacity list
    mincapacity = []
    for path in cyclepath:
        match = re.search(r'(\d+)mAh', path)
        if match:
            capacity = int(match.group(1))
            mincapacity.append(capacity)
        else:
            mincapacity.append(0)  # Default value if capacity not found
    
    return cyclename, cyclepath, mincapacity

def pne_search_cycle(rawdir, inicycle=None, endcycle=None):
    """
    Search for cycle files in the specified directory within the given cycle range.
    
    Args:
        rawdir (str): Directory containing the cycle files
        inicycle (int, optional): Initial cycle number to start from
        endcycle (int, optional): End cycle number to stop at
        
    Returns:
        tuple: (file_start, file_end) indices for the cycle range
    """
    if not os.path.isdir(rawdir):
        return -1, -1
    
    # Get all CSV files in the directory
    subfiles = [f for f in os.listdir(rawdir) if f.endswith(".csv")]
    
    # Directly find SaveEndData file
    save_end_data_file = next((f for f in subfiles if "SaveEndData" in f), None)
    
    if not save_end_data_file:
        return -1, -1
        
    df = pd.read_csv(os.path.join(rawdir, save_end_data_file), sep=",", skiprows=0, engine="c", header = None, encoding="cp949", on_bad_lines='skip')
   
    if inicycle is None or endcycle is None:
        if inicycle is None:
            inicycle = df.loc[:,27].min()
        if endcycle is None:
            endcycle = df.loc[:,27].max()
    
    # Get index for initial cycle
    index_min = df.loc[(df.loc[:,27]==(inicycle-1)),0].tolist()
    # Get index for end cycle
    index_max = df.loc[(df.loc[:,27]==endcycle),0].tolist()
    
    # Define inicycle and endcycle if they are None
    df2 = pd.read_csv(os.path.join(rawdir, "savingFileIndex_start.csv"), sep="\\s+", skiprows=0, engine="c", header = None, encoding="cp949", on_bad_lines='skip')
    df2 = df2.loc[:,3].tolist() #result index number
    
    index2 = []
    for element in df2:
        new_element = int(element.replace(',',''))
        index2.append(new_element)
        
    if len(index_min) != 0:
        file_start = bisect.bisect_left(index2, index_min[-1]+1)-1
        file_end = bisect.bisect_left(index2, index_max[-1]+1)-1
    else:
        file_start = -1
        file_end = -1

    return file_start, file_end, inicycle, endcycle
    # Output:
    # file_start: Index of the starting file in the cycle range
    # file_end: Index of the ending file in the cycle range
    # inicycle: Updated initial cycle number if it was None
    # endcycle: Updated end cycle number if it was None

            

def pne_continue_data(path, inicycle=None, endcycle=None):
    
    df = pd.DataFrame()
    profile_raw = None
    
    # Check for Restore directory
    restore_dir = os.path.join(path, "Restore")
    if os.path.isdir(restore_dir):
        print(f"Processing Restore directory at: {restore_dir}")
        
        # Get files within the cycle range
      
        file_start, file_end, inicycle, endcycle = pne_search_cycle(restore_dir, inicycle, endcycle)
        subfile = [f for f in os.listdir(restore_dir) if f.endswith(".csv")]
        
        if file_start != -1:
            for files in subfile[(file_start):(file_end+1)]:
                if "SaveData" in files:
                    profileRawTemp = pd.read_csv(os.path.join(restore_dir, files), sep=",", skiprows=0, engine="c", header = None, encoding="cp949", on_bad_lines='skip')
                    if profile_raw is not None:
                        profile_raw = pd.concat([profile_raw, profileRawTemp], ignore_index=True)
                    else:
                        profile_raw = profileRawTemp
    
    # Store the profile data in the DataFrame properly
    if profile_raw is not None:
        df = profile_raw
        
    return df

def pne_cyc_continue_data(path):
    df = pd.DataFrame()
    restore_dir = os.path.join(path, "Restore")
    if os.path.isdir(restore_dir):
        print(f"Processing Restore directory at: {restore_dir}")
        subfile = [f for f in os.listdir(restore_dir) if f.endswith(".csv")]
  
        save_end_data_file = next((f for f in subfile if "SaveEndData" in f), None)
        if save_end_data_file:
                df.Cycrawtemp = pd.read_csv(os.path.join(restore_dir, save_end_data_file), sep=",", skiprows=0, engine="c", header = None, encoding="cp949", on_bad_lines='skip')
    return df     


def extract_channel_number(path):
    """
    Extract channel number from a path string.
    
    Args:
        path (str): Path containing channel information
        
    Returns:
        str: Extracted channel number or None if not found
    """
    # Look for patterns like "M01Ch045[045]" or "M01Ch046[046]"
    match = re.search(r'M\d+Ch(\d+)(?:\[(\d+)\])?', path)
    if match:
        # Return both the channel number and the number in brackets if available
        channel = match.group(1)
        channel_id = match.group(2) if match.group(2) else channel
        return channel, channel_id
    return None, None


def concatenate():
    cyclename, cyclepath, mincapacity = set_pne_paths()
    
    # Check if paths were successfully loaded
    if not cyclepath:
        raise ValueError("No cycle paths found")
    
    # Ask for cycle range (or use default values)
    inicycle = None
    endcycle = None
    try:
        user_input = input("Enter initial cycle number (or press Enter for all cycles): ").strip()
        if user_input:
            inicycle = int(user_input)
        
        user_input = input("Enter end cycle number (or press Enter for all cycles): ").strip()
        if user_input:
            endcycle = int(user_input)
    except ValueError:
        print("Invalid cycle numbers provided. Using all cycles.")
    
    # Create a DataFrame from the cycle information
    cycle_df = pd.DataFrame({
        'cyclename': cyclename,
        'cyclepath': cyclepath,
        'mincapacity': mincapacity
    })
    
    # Group the data by cyclename
    grouped = cycle_df.groupby('cyclename')
    
    # Dictionary to store all processed data
    all_cycle_data = []
    
    # Process each group
    for cycname, group in grouped:
        print(f"\nProcessing cyclename: {cycname}")
        
        # Process each path in the group
        for cycle_idx, (_, row) in enumerate(group.iterrows()):
            path = row['cyclepath']
            
            # Get all subfolders for this path
            subfolders = [f.path for f in os.scandir(path) if f.is_dir() and "Pattern" not in f.path]
            
            # Debug print
            print(f"Cycle[{cycle_idx}] has {len(subfolders)} subfolders:")
            
            # Process each subfolder
            for j, subfolder in enumerate(subfolders):
                channel, channel_id = extract_channel_number(subfolder)
                print(f"  subfolder[{j}]\t{subfolder}\tcycle[{cycle_idx}]\t{cycname}\tchannel: {channel}, id: {channel_id}")
                
                if channel:
                    # Create a unique key for each channel
                    channel_key = f"{cycname}_Ch{channel_id}"
                    
                    # Extract data
                    pneProfile = pne_continue_data(subfolder, inicycle, endcycle)
                    pneCycle = pne_cyc_continue_data(subfolder)
                    
                    # Process cycle data
                    if not pneCycle.empty:
                        # Filter cycle data
                        cycle_data = pneCycle.cycrawtemp[
                            (pneCycle.cycrawtemp[2].isin([1, 2])) & 
                            (pneCycle.cycrawtemp[27] >= inicycle if inicycle is not None else True) & 
                            (pneCycle.cycrawtemp[27] <= endcycle if endcycle is not None else True)
                        ]
                        
                        # Select and rename columns
                        if not cycle_data.empty:
                            processed_data = cycle_data[[0, 8, 9, 10, 11]].copy()
                            processed_data.columns = ['time', 'voltage', 'current', 'chg_capacity', 'dchg_capacity']
                            
                            # Add metadata
                            processed_data['channel_key'] = channel_key
                            processed_data['cycle_idx'] = cycle_idx
                            processed_data['subfolder'] = subfolder
                            
                            # Add to the collection
                            all_cycle_data.append(processed_data)
                            print(f"Processed cycle data for {channel_key}, cycle {cycle_idx}")
    
    # If we have processed data, merge and export
    if all_cycle_data:
        # Concatenate all processed data
        combined_data = pd.concat(all_cycle_data, ignore_index=True)
        
        # Process by channel
        merged_data = {}
        for channel_key, channel_group in combined_data.groupby('channel_key'):
            # Sort by cycle_idx
            channel_group = channel_group.sort_values('cycle_idx')
            
            # Calculate cumulative time
            channel_group['cumulative_time'] = channel_group['time'].cumsum()
            
            # Store merged data
            merged_data[channel_key] = channel_group
            
            # Export to CSV
            output_filename = f"{channel_key}_merged_cycles.csv"
            channel_group.to_csv(output_filename, index=False)
            print(f"Exported merged cycle data for {channel_key} to {output_filename}")
    else:
        merged_data = {}
        print("Warning: No data was processed. Check your input paths and cycle numbers.")
    
    # Print a summary
    if merged_data:
        print("\nData summary:")
        for key, df in merged_data.items():
            print(f"  - {key}: {df.shape[0]} rows, {df.shape[1]} columns")
    
    print(f"\nProcessed {len(merged_data)} unique channels with data")
    return merged_data

def main():
    
    concatenate()

if __name__ == "__main__":
    main()