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
    
    # Set default values for inicycle and endcycle
    inicycle = 1 if inicycle is None else inicycle
    endcycle = df.loc[:,27].max() if endcycle is None else endcycle
    
    # Get index for initial cycle
    index_min = df.loc[(df.loc[:,27]==(inicycle-1)),0].tolist()
    
    # Get index for end cycle
    index_max = df.loc[(df.loc[:,27]==endcycle),0].tolist()
        
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

    return file_start, file_end

            

def pne_continue_data(path, inicycle=None, endcycle=None):
    
    df = pd.DataFrame()
    profile_raw = None
    
    # Check for Restore directory
    restore_dir = os.path.join(path, "Restore")
    if os.path.isdir(restore_dir):
        print(f"Processing Restore directory at: {restore_dir}")
        
        # Get files within the cycle range
      
        filepos = pne_search_cycle(restore_dir, inicycle, endcycle)
        subfile = [f for f in os.listdir(restore_dir) if f.endswith(".csv")]
        
        if filepos[0] != -1:
            for files in subfile[(filepos[0]):(filepos[1]+1)]:
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
    
    print(f"Processing cycles: {'all' if inicycle is None else inicycle} to {'all' if endcycle is None else endcycle}")
    
    # Organize paths by cyclename
    organized_data = {}
    
    # First, group all paths by cyclename
    for i, path in enumerate(cyclepath):
        cycname = cyclename[i]
        if cycname not in organized_data:
            organized_data[cycname] = {'paths': [], 'indices': []}
        
        organized_data[cycname]['paths'].append(path)
        organized_data[cycname]['indices'].append(i)
    
    # For each cyclename, collect all subfolders
    for cycname, data in organized_data.items():
        all_subfolders = []
        for path in data['paths']:
            subfolders = [f.path for f in os.scandir(path) if f.is_dir() and "Pattern" not in f.path]
            all_subfolders.append(subfolders)
        
        # Store subfolders in the organized_data dictionary
        data['all_subfolders'] = all_subfolders
    
    # Dictionary to store all channel-specific dataframes
    output_data = {}
    
    # Process each cyclename group
    for cycname, data in organized_data.items():
        all_subfolders = data['all_subfolders']
        
        # Debug print
        print(f"\nProcessing cyclename: {cycname}")
        for i, subfolders in enumerate(all_subfolders):
            print(f"Cycle[{i}] has {len(subfolders)} subfolders:")
            for j, subfolder in enumerate(subfolders):
                channel, channel_id = extract_channel_number(subfolder)
                print(f"  all_subfolders[{i}][{j}]\t{subfolder}\tcycle[{i}]\t{cycname}\tchannel: {channel}, id: {channel_id}")
        
        # Process each cycle
        for cycle_idx, subfolders in enumerate(all_subfolders):
            # Process each subfolder for this cycle
            for subfolder in subfolders:
                channel, channel_id = extract_channel_number(subfolder)
                if channel:
                    # Create a unique key for each channel
                    channel_key = f"{cycname}_Ch{channel_id}"
                    
                    # Extract data from the subfolder
                    '''
                    # Column
                    #0 Index,#1 default(2)
                    #2 Step_type 1:충전, 2:방전, 3:휴지, 4: OCV, 5: Impedance, 8:loop
                    #3 ChgDchg 1:CV, 2:CC, 255:rest
                    #4 Current application classification 1:전류 비인가 직전 포인트, 2: 전류인가
                    #5 CCCV 0:CC, 1:CV
                    #6 EndState 0: Pattern 시작, 64:휴지, 65:CC, 66:CV, 69:Pattern종료, 78:용량
                    #7 Step count step(CC/CCCV/Rest/Loop), Repeat: 7125, Go to: 리셋
                    #8 Voltage[uV], #9 Current[uA], #10 Chg Capacityuan] step 충방전의 경우 합산 필요
                    #11 Dchg Capacity[uAh], #12 Chg Power(mW), #13 Dchg Power(mW)
                    #14 Chg WattHour(Wh), #15 Dchg WattHour(Wh)
                    #16 repeat pattern count (per 8 or 9) 0, 1, 2, ...
                    #17 StepTimel/100s], #18 TotTime(day), #19 TotTime(/100s)
                    #20 Impedance, #21 Temperature, #22 Temperature, #23 Temperature, #24 Temperature, #25?2 or 0, #26 Repeat count
                    #27 TotalCycle, #28 Current Cycle, #29 Average Voltage(uV), #30 Average Current(UA), #31-
                    #32 CV 구간, #33 Date(YYYY/MM/DD), #34 Time(HH/mm/ssss[/100s])
                    #35 -, #36 -, #37 -, #38 Step별?
                    #39 CC 충전 구간, #40 CV 구간, #41 방전 구간, #42-
                    #43 구간별 평균 전압, #44 누적 step, #45 Voltage max(uV), #46 Voltage min(uV)
                    #46 Voltage min(uV)
                    #46 Voltage min(uV)
                    '''
                    pneProfile = pne_continue_data(subfolder, inicycle, endcycle)
                    pneCycle = pne_cyc_continue_data(subfolder, inicycle, endcycle)

                    # Extract and process cycle data
                    if not pneCycle.empty:
                        # Filter cycle data for charging (1) and discharging (2) steps
                        cycle_data = pneCycle.cycrawtemp[
                            (pneCycle.cycrawtemp[2].isin([1, 2])) & 
                            (pneCycle.cycrawtemp[27] >= inicycle) & 
                            (pneCycle.cycrawtemp[27] <= endcycle)
                        ]
                        
                        # Select relevant columns and rename them
                        cycle_data = cycle_data[[0, 8, 9, 10, 11]]  # Index, Voltage, Current, Chg Capacity, Dchg Capacity
                        cycle_data.columns = ['time', 'voltage', 'current', 'chg_capacity', 'dchg_capacity']
                        
                        # Store processed cycle data
                        if channel_key not in output_data:
                            output_data[channel_key] = {'cycle': []}
                        output_data[channel_key]['cycle'].append({
                            'cycle_idx': cycle_idx,
                            'data': cycle_data,
                            'subfolder': subfolder
                        })
                        print(f"Processed cycle data for {channel_key}, cycle {cycle_idx}")

        # Merge data for each channel
        merged_data = {}
        for channel_key, data in output_data.items():
            if 'cycle' in data and data['cycle']:
                # Sort cycles by cycle_idx
                sorted_cycles = sorted(data['cycle'], key=lambda x: x['cycle_idx'])
                
                # Concatenate all cycle data
                merged_cycles = pd.concat([cycle['data'] for cycle in sorted_cycles], ignore_index=True)
                
                # Calculate cumulative time
                merged_cycles['cumulative_time'] = merged_cycles['time'].cumsum()
                
                # Store merged data
                merged_data[channel_key] = merged_cycles
                
                # Export to CSV
                output_filename = f"{channel_key}_merged_cycles.csv"
                merged_cycles.to_csv(output_filename, index=False)
                print(f"Exported merged cycle data for {channel_key} to {output_filename}")                   
    
    # Check if any data was processed
    if not merged_data:
        print("Warning: No data was processed. Check your input paths and cycle numbers.")
    else:
        # Print a summary of the processed data
        print("\nData summary:")
        for key, df in merged_data.items():
            print(f"  - {key}: {df.shape[0]} rows, {df.shape[1]} columns")
    
    print(f"\nProcessed {len(merged_data)} unique channels with data")
    return merged_data

def main():
    
    concatenate()

if __name__ == "__main__":
    main()