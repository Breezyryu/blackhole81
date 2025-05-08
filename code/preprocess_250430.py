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
        return -1, -1, inicycle, endcycle
    
    # Get all CSV files in the directory
    subfiles = [f for f in os.listdir(rawdir) if f.endswith(".csv")]
    
    # Directly find SaveEndData file
    save_end_data_file = next((f for f in subfiles if "SaveEndData" in f), None)
    
    if not save_end_data_file:
        return -1, -1, inicycle, endcycle
        
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
                df = pd.read_csv(os.path.join(restore_dir, save_end_data_file), sep=",", skiprows=0, engine="c", header = None, encoding="cp949", on_bad_lines='skip')
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


def extract_base_name(cycname):
    """
    Extract the base name from a cycle name by removing the sequence number at the end.
    For example, 'A1_MP1_T23_1' -> 'A1_MP1_T23'
    
    Args:
        cycname (str): Cycle name
        
    Returns:
        str: Base name without sequence number
    """
    parts = cycname.split('_')
    # Check if the last part is a number
    if parts[-1].isdigit():
        return '_'.join(parts[:-1])
    return cycname


def extract_sequence_number(cyclename):
    """
    Extract the sequence number from a cyclename.
    For example, 'A1_MP1_T23_1' -> 1, 'A1_MP1_T23_2' -> 2
    
    Args:
        cyclename (str): Cycle name
        
    Returns:
        int: Sequence number (default to 0 if not found)
    """
    parts = cyclename.split('_')
    if parts[-1].isdigit():
        return int(parts[-1])
    return 0


def get_channel_position(subfolder, sequence_num):
    """
    Determines the position of a channel within its sequence group.
    
    Args:
        subfolder (str): Path to the subfolder containing channel information
        sequence_num (int): Sequence number of the current data
        
    Returns:
        int: Position index of the channel in its sequence
    """
    # Extract channel information
    channel, channel_id = extract_channel_number(subfolder)
    if not channel:
        return -1
    
    # Convert channel to integer if possible
    try:
        channel_int = int(channel)
        return channel_int % 10  # Use last digit as position
    except ValueError:
        # If channel cannot be converted to int, use string hash
        return hash(channel) % 10


def sanitize_filename(filename):
    """
    Sanitize a filename by replacing or removing invalid characters.
    
    Args:
        filename (str): The filename to sanitize
        
    Returns:
        str: Sanitized filename
    """
    # Replace invalid characters with underscores
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove any leading/trailing periods or spaces
    sanitized = sanitized.strip('. ')
    
    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "unnamed"
        
    return sanitized


def process_data_from_channel(path, inicycle=None, endcycle=None):
    """
    Process data from a channel directory.
    
    Args:
        path (str): Path to the channel directory
        inicycle (int, optional): Initial cycle number
        endcycle (int, optional): End cycle number
        
    Returns:
        tuple: (processed_data, channel_id)
    """
    # Extract channel number
    _, channel_id = extract_channel_number(path)
    
    # Get cycle data
    pneCycle = pne_cyc_continue_data(path)
    
    if pneCycle.empty:
        return None, channel_id
    
    # Filter cycle data
    cycle_data = pneCycle[
        (pneCycle[2].isin([1, 2])) & 
        (pneCycle[27] >= inicycle if inicycle is not None else True) & 
        (pneCycle[27] <= endcycle if endcycle is not None else True)
    ]
    
    if cycle_data.empty:
        return None, channel_id
    
    # Select and rename columns
    processed_data = cycle_data[[0, 8, 9, 10, 11]].copy()
    processed_data.columns = ['time', 'voltage', 'current', 'chg_capacity', 'dchg_capacity']
    
    # Add metadata
    processed_data['channel_id'] = channel_id
    processed_data['subfolder'] = path
    
    return processed_data, channel_id


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
    
    # Create output directory if it doesn't exist
    output_dir = "merged_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Define a function to get all channel directories in a path
    def get_channel_dirs(path):
        path = path.replace('\\', '/')
        try:
            # Find all subdirectories that contain "Ch" and not "Pattern"
            return [d.path for d in os.scandir(path) if d.is_dir() and "Pattern" not in d.path]
        except FileNotFoundError:
            print(f"Warning: Path {path} not found")
            return []
    
    # Create a DataFrame from the cycle information
    cycle_df = pd.DataFrame({
        'cyclename': cyclename,
        'cyclepath': cyclepath,
        'mincapacity': mincapacity,
        'base_name': [extract_base_name(name) for name in cyclename],
        'seq_num': [extract_sequence_number(name) for name in cyclename]
    })
    
    # Group by base_name
    all_channels = []
    base_name_groups = cycle_df.groupby('base_name')
    
    # Collect all channel information
    for base_name, group in base_name_groups:
        # Skip if only one sequence (we need at least 2 sequences to merge)
        if len(group['seq_num'].unique()) < 2:
            continue
            
        print(f"\nProcessing base name: {base_name}")
        
        # Process each sequence
        for _, row in group.iterrows():
            path = row['cyclepath']
            seq_num = row['seq_num']
            
            channel_dirs = get_channel_dirs(path)
            
            # Process each channel in this sequence
            for i, channel_dir in enumerate(sorted(channel_dirs)):
                channel, channel_id = extract_channel_number(channel_dir)
                if channel:
                    # Store channel info with its position in the sorted list
                    # This position will be used to match channels across sequences
                    all_channels.append({
                        'base_name': base_name,
                        'seq_num': seq_num,
                        'path': channel_dir,
                        'channel': channel,
                        'channel_id': channel_id,
                        'position': i  # Use index in sorted list as position
                    })
    
    # Create a DataFrame for easier processing
    channels_df = pd.DataFrame(all_channels)
    
    # Create merged groups
    merged_groups = []
    
    # Only process if we have channels
    if not channels_df.empty:
        # Process each base_name separately
        for base_name, group in channels_df.groupby('base_name'):
            # Skip if only one sequence
            if len(group['seq_num'].unique()) < 2:
                continue
                
            # For each position, collect channels from all sequences
            for position in group['position'].unique():
                position_channels = group[group['position'] == position]
                
                # Only process if we have channels from multiple sequences
                if len(position_channels['seq_num'].unique()) >= 2:
                    group_channels = []
                    
                    # Collect one channel from each sequence at this position
                    for seq_num in sorted(position_channels['seq_num'].unique()):
                        seq_channel = position_channels[position_channels['seq_num'] == seq_num].iloc[0]
                        group_channels.append(seq_channel)
                    
                    # Add this group to our list
                    merged_groups.append(group_channels)
    
    # Process each merged group
    merged_data = {}
    
    # Print all merged groups for debugging
    print(f"\nFound {len(merged_groups)} merged groups to process")
    for i, group in enumerate(merged_groups):
        channel_ids = [ch['channel_id'] for ch in group]
        print(f"Group {i+1}: Ch{' + Ch'.join(channel_ids)}")
    
    # Process each group
    for group_idx, group in enumerate(merged_groups):
        # Create a name for this group
        channel_ids = [ch['channel_id'] for ch in group]
        group_key = f"Ch{'_Ch'.join(channel_ids)}"
        safe_group_key = sanitize_filename(group_key)
        
        print(f"\nProcessing merged group {group_idx+1}: {group_key}")
        
        # Print paths in this group
        for i, ch in enumerate(group):
            print(f"  {i+1}. {ch['path']} (seq: {ch['seq_num']}, channel: {ch['channel_id']})")
        
        # Process each channel
        all_data = []
        
        for idx, ch in enumerate(group):
            path = ch['path']
            channel_id = ch['channel_id']
            
            # Get cycle data
            pneCycle = pne_cyc_continue_data(path)
            pneProfile = pne_continue_data(path, inicycle, endcycle)
            
            if not pneCycle.empty:
                # Filter cycle data
                cycle_data = pneCycle[
                    (pneCycle[2].isin([1, 2])) & 
                    (pneCycle[27] >= inicycle if inicycle is not None else True) & 
                    (pneCycle[27] <= endcycle if endcycle is not None else True)
                ]
                
                # Process data
                if not cycle_data.empty:
                    processed_data = cycle_data[[0, 8, 9, 10, 11]].copy()
                    processed_data.columns = ['time', 'voltage', 'current', 'chg_capacity', 'dchg_capacity']
                    
                    # Add metadata
                    processed_data['cyclename'] = ch['base_name'] + f"_{ch['seq_num']}"
                    processed_data['path_seq'] = idx
                    processed_data['subfolder'] = path
                    processed_data['channel_id'] = channel_id
                    
                    all_data.append(processed_data)
                    print(f"    Added {processed_data.shape[0]} rows of data for channel {channel_id}")
        
        # Merge all data for this group
        if all_data:
            # Concatenate all DataFrames
            group_merged = pd.concat(all_data, ignore_index=True)
            
            # Calculate cumulative time for the entire sequence
            # First, calculate time difference within each path
            group_merged['path_time'] = group_merged.groupby('path_seq')['time'].transform(lambda x: x - x.iloc[0] if len(x) > 0 else 0)
            
            # Then calculate the cumulative time across all paths
            group_merged['cumulative_time'] = 0
            prev_end_time = 0
            
            for seq in sorted(group_merged['path_seq'].unique()):
                # Adjust time for this sequence based on previous end time
                mask = group_merged['path_seq'] == seq
                if seq > 0:
                    # Add the previous end time to all rows in this sequence
                    group_merged.loc[mask, 'cumulative_time'] = group_merged.loc[mask, 'path_time'] + prev_end_time
                else:
                    # For the first sequence, cumulative_time = path_time
                    group_merged.loc[mask, 'cumulative_time'] = group_merged.loc[mask, 'path_time']
                
                # Update prev_end_time for the next sequence
                if mask.any():
                    prev_end_time = group_merged.loc[mask, 'cumulative_time'].max()
            
            # Store merged data
            merged_data[safe_group_key] = group_merged
            
            # Export to CSV in the output directory
            output_filename = os.path.join(output_dir, f"{safe_group_key}_merged_cycles.csv")
            try:
                group_merged.to_csv(output_filename, index=False)
                print(f"Exported merged data to {output_filename}")
            except Exception as e:
                print(f"Error saving file {output_filename}: {str(e)}")
                # Try with a simplified filename as a fallback
                fallback_filename = os.path.join(output_dir, f"merged_group_{group_idx+1}.csv")
                try:
                    group_merged.to_csv(fallback_filename, index=False)
                    print(f"Exported using fallback filename: {fallback_filename}")
                except Exception as e2:
                    print(f"Error saving fallback file: {str(e2)}")
    
    # Print a summary
    if merged_data:
        print("\nData summary:")
        for key, df in merged_data.items():
            print(f"  - {key}: {df.shape[0]} rows, {df.shape[1]} columns")
            # Count unique cyclenames
            unique_cyclenames = df['cyclename'].nunique()
            print(f"    Contains data from {unique_cyclenames} cyclenames/paths")
            # Show channel IDs
            channel_ids = ", ".join(sorted(df['channel_id'].unique()))
            print(f"    Channel IDs: {channel_ids}")
    else:
        print("Warning: No data was processed. Check your input paths and cycle numbers.")
    
    print(f"\nProcessed {len(merged_data)} unique channel groups with data")
    print(f"Output files saved to the '{output_dir}' directory")
    return merged_data


def main():
    merged_data = concatenate()
    return merged_data

if __name__ == "__main__":
    main()