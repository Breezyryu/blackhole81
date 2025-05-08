import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import bisect
import logging
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def set_pne_paths():
    """
    파일에서 PNE 데이터 처리를 위한 경로 설정
    
    Args:
        filepath (str): cyclename과 cyclepath를 포함하는 텍스트 파일 경로
        
    Returns:
        tuple: (cyclename, cyclepath, capacity) 리스트를 포함하는 튜플
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
    
    try:
        # 탭 구분자로 파일 읽기
        df = pd.read_csv(datafilepath, sep="\t", engine="c", encoding="UTF-8", 
                        skiprows=0, on_bad_lines='skip')
        
        # cyclename과 cyclepath 추출
        cyclename = df['cyclename'].tolist() if 'cyclename' in df.columns else []
        cyclepath = df['cyclepath'].tolist() if 'cyclepath' in df.columns else []
        
        if not cyclename or not cyclepath:
            logger.warning(f"파일 {datafilepath}에서 cyclename 또는 cyclepath를 찾을 수 없습니다.")
            return [], [], []
            
        # 각 cyclepath에서 용량 추출하여 capacity 리스트 생성
        capacity = []
        for cycname in cyclename:
            match = re.search(r'(\d+)mAh', cycname)
            if match:
                cap = int(match.group(1))
                capacity.append(cap)
            else:
                logger.warning(f"'{cycname}'에서 용량을 찾을 수 없습니다. 기본값 0을 사용합니다.")
                capacity.append(0)  # 용량을 찾을 수 없는 경우 기본값
        
        logger.info(f"{len(cyclename)}개의 사이클 정보를 로드했습니다.")
        return cyclename, cyclepath, capacity
        
    except Exception as e:
        logger.error(f"파일 로드 중 오류 발생: {str(e)}")
        return [], [], []

def pne_search_cycle(rawdir, inicycle=None, endcycle=None):
    """
    지정된 사이클 범위 내에서 사이클 파일 검색
    
    Args:
        rawdir (str): 사이클 파일이 포함된 디렉토리
        inicycle (int, optional): 시작 사이클 번호
        endcycle (int, optional): 종료 사이클 번호
        
    Returns:
        tuple: 사이클 범위에 대한 (file_start, file_end, inicycle, endcycle) 인덱스
    """
    if not os.path.isdir(rawdir):
        logger.warning(f"디렉토리가 존재하지 않습니다: {rawdir}")
        return -1, -1, inicycle, endcycle
    
    # 디렉토리의 모든 CSV 파일 가져오기
    subfiles = [f for f in os.listdir(rawdir) if f.endswith(".csv")]
    
    # SaveEndData 파일 직접 찾기
    save_end_data_file = next((f for f in subfiles if "SaveEndData" in f), None)
    
    if not save_end_data_file:
        logger.warning(f"{rawdir}에서 SaveEndData 파일을 찾을 수 없습니다.")
        return -1, -1, inicycle, endcycle
    
    try:
        df = pd.read_csv(os.path.join(rawdir, save_end_data_file), sep=",", skiprows=0, 
                         engine="c", header=None, encoding="cp949", on_bad_lines='skip')
   
        # inicycle 또는 endcycle이 None인 경우 설정
        if inicycle is None or endcycle is None:
            if inicycle is None:
                inicycle = int(df.loc[:,27].min())
            if endcycle is None:
                endcycle = int(df.loc[:,27].max())
        
        # 시작 사이클의 인덱스
        index_min = df.loc[(df.loc[:,27]==(inicycle)),0].tolist()
        # 종료 사이클의 인덱스
        index_max = df.loc[(df.loc[:,27]==endcycle),0].tolist()
        
        # 인덱스 파일 읽기
        index_file_path = os.path.join(rawdir, "savingFileIndex_start.csv")
        if not os.path.exists(index_file_path):
            logger.warning(f"인덱스 파일을 찾을 수 없습니다: {index_file_path}")
            return -1, -1, inicycle, endcycle
            
        df2 = pd.read_csv(index_file_path, sep="\\s+", skiprows=0, 
                          engine="c", header=None, encoding="cp949", on_bad_lines='skip')
        index2 = [int(element.replace(',','')) for element in df2.loc[:,3].tolist()]
        
        if len(index_min) != 0:
            file_start = bisect.bisect_left(index2, index_min[-1]+1)-1
            file_end = bisect.bisect_left(index2, index_max[-1]+1)-1
            logger.debug(f"사이클 {inicycle}-{endcycle}에 대한 파일 인덱스: {file_start}-{file_end}")
            return file_start, file_end, inicycle, endcycle
        else:
            logger.warning(f"사이클 {inicycle}에 대한 인덱스를 찾을 수 없습니다.")
            return -1, -1, inicycle, endcycle
            
    except Exception as e:
        logger.error(f"사이클 검색 중 오류 발생: {str(e)}")
        return -1, -1, inicycle, endcycle

def load_pne_data(path, inicycle=None, endcycle=None):
    """
    Restore 디렉토리에서 프로파일 데이터와 사이클 데이터 로드
    
    Args:
        path (str): Restore 디렉토리를 포함하는 경로
        inicycle (int, optional): 시작 사이클 번호
        endcycle (int, optional): 종료 사이클 번호
        
    Returns:
        tuple: (profile_data, cycle_data) - 로드된 프로파일 및 사이클 데이터
    """
    profile_data = pd.DataFrame()
    cycle_data = pd.DataFrame()
    
    # Restore 디렉토리 확인
    restore_dir = os.path.join(path, "Restore")
    if not os.path.isdir(restore_dir):
        logger.warning(f"Restore 디렉토리가 존재하지 않습니다: {restore_dir}")
        return profile_data, cycle_data
    
    logger.info(f"Restore 디렉토리 처리 중: {restore_dir}")
    
    try:
        # 사이클 범위 내 파일 가져오기
        file_start, file_end, inicycle, endcycle = pne_search_cycle(restore_dir, inicycle, endcycle)
        subfiles = [f for f in os.listdir(restore_dir) if f.endswith(".csv")]
        
        # 프로파일 데이터 로드
        if file_start != -1:
            profile_raw = None
            for files in subfiles[(file_start):(file_end+1)]:
                if "SaveData" in files:
                    file_path = os.path.join(restore_dir, files)
                    profileRawTemp = pd.read_csv(file_path, sep=",", skiprows=0, 
                                              engine="c", header=None, encoding="cp949", on_bad_lines='skip')
                    if profile_raw is not None:
                        profile_raw = pd.concat([profile_raw, profileRawTemp], ignore_index=True)
                    else:
                        profile_raw = profileRawTemp
            
            if profile_raw is not None:
                profile_data = profile_raw
        
        # 사이클 데이터 로드
        save_end_data_file = next((f for f in subfiles if "SaveEndData" in f), None)
        if save_end_data_file:
            file_path = os.path.join(restore_dir, save_end_data_file)
            cycle_data = pd.read_csv(file_path, sep=",", skiprows=0, 
                                  engine="c", header=None, encoding="cp949", on_bad_lines='skip')
        
        return profile_data, cycle_data
        
    except Exception as e:
        logger.error(f"데이터 로드 중 오류 발생: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

def extract_channel_info(path):
    """
    경로 문자열에서 채널 번호 추출
    
    Args:
        path (str): 채널 정보가 포함된 경로
        
    Returns:
        dict: 채널 정보 (channel, channel_id)
    """
    # "M01Ch045[045]" 또는 "M01Ch046[046]" 같은 패턴 찾기
    match = re.search(r'M\d+Ch(\d+)(?:\[(\d+)\])?', path)
    if match:
        # 채널 번호와 괄호 안의 숫자 반환
        channel = match.group(1)
        channel_id = match.group(2) if match.group(2) else channel
        return {
            'channel': channel,
            'channel_id': channel_id
        }
    return None

def extract_base_cycle_name(path):
    """
    경로에서 기본 사이클 이름 추출 (예: A1_MP1_T45_1에서 A1_MP1_T45)
    
    Args:
        path (str): 전체 경로
        
    Returns:
        str: 기본 사이클 이름
    """
    # 경로에서 파일 이름 추출 (경로 구분자 처리)
    basename = os.path.basename(path)
    
    # '_'로 분리하고 성적으로 '_'로 결합
    parts = basename.split('_')
    
    # 마지막 부분이 숫자인 경우 제외
    if len(parts) > 1 and parts[-1].isdigit():
        return '_'.join(parts[:-1])
    
    return basename

def process_cycle_data(cycle_data, inicycle, endcycle, metadata):
    """
    사이클 데이터 처리 및 필터링
    
    Args:
        cycle_data (DataFrame): 처리할 사이클 데이터
        inicycle (int): 시작 사이클 번호
        endcycle (int): 종료 사이클 번호
        metadata (dict): 추가할 메타데이터
        
    Returns:
        DataFrame: 처리된 사이클 데이터
    """
    if cycle_data.empty:
        return pd.DataFrame()
    
    # 사이클 데이터 필터링
    filtered_data = cycle_data[
        (cycle_data[2].isin([1, 2])) & 
        (cycle_data[27] >= inicycle if inicycle is not None else True) & 
        (cycle_data[27] <= endcycle if endcycle is not None else True)
    ]
    
    if filtered_data.empty:
        return pd.DataFrame()
    
    # 필요한 열만 선택하고 이름 변경
    processed_data = filtered_data[[0, 8, 9, 10, 11]].copy()
    processed_data.columns = ['time', 'voltage', 'current', 'chg_capacity', 'dchg_capacity']
    
    # 메타데이터 추가
    for key, value in metadata.items():
        processed_data[key] = value
    
    return processed_data

def get_user_input_cycles():
    """
    사용자로부터 사이클 범위 입력 받기
    
    Returns:
        tuple: (inicycle, endcycle) - 시작 및 종료 사이클 번호
    """
    inicycle = None
    endcycle = None
    
    try:
        user_input = input("시작 사이클 번호 입력 (모든 사이클은 Enter): ").strip()
        if user_input:
            inicycle = int(user_input)
        
        user_input = input("종료 사이클 번호 입력 (모든 사이클은 Enter): ").strip()
        if user_input:
            endcycle = int(user_input)
            
        logger.info(f"입력된 사이클 범위: {inicycle if inicycle is not None else '처음'} - {endcycle if endcycle is not None else '마지막'}")
        
    except ValueError:
        logger.warning("잘못된 사이클 번호가 제공되었습니다. 모든 사이클을 사용합니다.")
    
    return inicycle, endcycle

def identify_channel_groups(cycle_df):
    """
    채널 ID를 기반으로 데이터 그룹 자동 생성
    
    Args:
        cycle_df (DataFrame): 사이클 데이터
        
    Returns:
        dict: 채널 ID로부터 그룹으로의 매핑
    """
    # 모든 발견된 채널 ID 수집
    all_channel_ids = set()
    
    # cycle_df에서 파일 경로 검사하여 채널 ID 추출
    for path in cycle_df['cyclepath']:
        if not os.path.exists(path):
            logger.warning(f"경로가 존재하지 않습니다: {path}")
            continue
            
        # 하위 폴더 검사
        subfolders = [f.path for f in os.scandir(path) if f.is_dir() and "Pattern" not in f.path]
        
        for subfolder in subfolders:
            channel_info = extract_channel_info(subfolder)
            if channel_info and 'channel_id' in channel_info:
                all_channel_ids.add(channel_info['channel_id'])
    
    # 모든 채널 ID를 개별 그룹으로 할당 (고정된 그룹이 없으므로)
    channel_to_group = {}
    for i, channel_id in enumerate(sorted(all_channel_ids)):
        group_name = f"Data#{i+1}"
        channel_to_group[channel_id] = group_name
    
    logger.info(f"자동으로 {len(channel_to_group)}개의 채널 그룹이 식별되었습니다.")
    return channel_to_group

def main():
    """
    메인 처리 함수
    """
    try:
        # 1. 경로 파일 로드
        filepath = "filepath.txt"
        if not os.path.exists(filepath):
            logger.error(f"파일을 찾을 수 없습니다: {filepath}")
            return
        
        # 2. cyclename, cyclepath, capacity 추출
        cyclename, cyclepath, capacity = set_pne_paths(filepath)
        
        # 경로가 성공적으로 로드되었는지 확인
        if not cyclepath:
            logger.error("사이클 경로를 찾을 수 없습니다.")
            return
        
        # 3. 사이클 범위 입력 받기
        inicycle, endcycle = get_user_input_cycles()
        
        # 사이클 정보로 DataFrame 생성
        cycle_df = pd.DataFrame({
            'cyclename': cyclename,
            'cyclepath': cyclepath,
            'capacity': capacity
        })
        
        # 4. 기본 사이클 이름으로 그룹화 (예: A1_MP1_T23)
        # cyclepath에서 기본 사이클 이름 추출
        cycle_df['base_cycle'] = cycle_df['cyclepath'].apply(extract_base_cycle_name)
        
        # 채널 ID에서 그룹으로의 매핑 생성 (자동화)
        channel_to_group = identify_channel_groups(cycle_df)
        
        # 그룹별 데이터 저장을 위한 딕셔너리
        group_data = defaultdict(list)
        
        # 5. 각 기본 사이클 그룹 처리
        for base_cycle, group in cycle_df.groupby('base_cycle'):
            logger.info(f"\n기본 사이클 처리 중: {base_cycle}")
            
            # cyclename으로 정렬하여 올바른 순서 보장
            group = group.sort_values('cyclename')
            
            # 그룹의 각 경로 처리
            for _, row in group.iterrows():
                path = row['cyclepath']
                cycname = row['cyclename']
                
                logger.info(f"{path}에서 {cycname} 처리 중")
                
                # 이 경로가 존재하는지 확인
                if not os.path.exists(path):
                    logger.warning(f"경로가 존재하지 않습니다: {path}")
                    continue
                
                # 이 경로에 대한 모든 하위 폴더 가져오기 (채널 표시)
                subfolders = [f.path for f in os.scandir(path) if f.is_dir() and "Pattern" not in f.path]
                
                # 각 채널 폴더 처리
                for subfolder in subfolders:
                    channel_info = extract_channel_info(subfolder)
                    
                    if channel_info and 'channel_id' in channel_info:
                        channel_id = channel_info['channel_id']
                        logger.info(f"  채널 발견: {channel_info['channel']}, ID: {channel_id} (위치: {subfolder})")
                        
                        # 이 채널을 그룹화해야 하는지 확인
                        if channel_id in channel_to_group:
                            group_name = channel_to_group[channel_id]
                            
                            # 5-1. 이 채널에 대한 데이터 로드
                            profile_data, cycle_data = load_pne_data(subfolder, inicycle, endcycle)
                            
                            # 사이클 데이터 처리
                            if not cycle_data.empty:
                                metadata = {
                                    'cyclename': cycname,
                                    'base_cycle': base_cycle,
                                    'subfolder': subfolder,
                                    'channel_id': channel_id
                                }
                                
                                processed_data = process_cycle_data(cycle_data, inicycle, endcycle, metadata)
                                
                                if not processed_data.empty:
                                    # 이 그룹의 컬렉션에 추가
                                    group_data[group_name].append(processed_data)
                                    logger.info(f"    {group_name}에 데이터 추가됨 (channel_id: {channel_id})")
        
        # 각 그룹에 대한 데이터 병합 및 내보내기
        for group_name, data_list in group_data.items():
            if data_list:
                # 메타데이터가 있는 DataFrame 생성
                group_df_with_metadata = pd.DataFrame({
                    'cyclename': [df['cyclename'].iloc[0] for df in data_list],
                    'base_cycle': [df['base_cycle'].iloc[0] for df in data_list],
                    'data': data_list,
                    'channel_id': [df['channel_id'].iloc[0] for df in data_list]
                })
                
                # 시퀀스 번호 추출 및 정렬
                group_df_with_metadata['seq_num'] = group_df_with_metadata['cyclename'].apply(
                    lambda x: int(x.split('_')[-1]) if len(x.split('_')) > 1 and x.split('_')[-1].isdigit() else 0
                )
                
                # 올바른 순서를 보장하기 위해 시퀀스 번호로 정렬 (1, 2, 3, 등)
                group_df_with_metadata = group_df_with_metadata.sort_values('seq_num')
                
                # 정렬된 순서로 DataFrame 연결
                sorted_data_list = group_df_with_metadata['data'].tolist()
                group_merged = pd.concat(sorted_data_list, ignore_index=True)
                
                # 누적 시간 계산
                group_merged['cumulative_time'] = group_merged['time'].cumsum()
                
                # CSV로 내보내기
                output_filename = f"{group_name}_merged_cycles.csv"
                group_merged.to_csv(output_filename, index=False)
                logger.info(f"{group_name}에 대한 병합된 사이클 데이터를 {output_filename}으로 내보냈습니다")
        
        # 처리된 데이터 요약 인쇄
        logger.info("\n데이터 요약:")
        for group_name, data_list in group_data.items():
            if data_list:
                total_rows = sum(df.shape[0] for df in data_list)
                num_channels = len(set(df['channel_id'].iloc[0] for df in data_list))
                num_cyclenames = len(set(df['cyclename'].iloc[0] for df in data_list))
                logger.info(f"  - {group_name}: {num_cyclenames}개 cyclenames와 {num_channels}개 채널에서 총 {total_rows}개 행")
                
    except Exception as e:
        logger.error(f"처리 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    main()