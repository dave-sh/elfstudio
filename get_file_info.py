import subprocess
import json
from collections import Counter
import math

# Wrapper for Command Line Utilities
# Formats data into JSON for easy processing by GUI.

def run_command(command: list) -> str:
    '''Helper function to run a shell command and return its output or None in case of an error.'''
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"error: {e}")
        return None


def get_file_info(file_path: str) -> dict:
    '''Returns File Info in structured JSON:
       - File Type, Architecture (32 or 64 bit), Version, Libraries, Linker, BuildID, OS.'''
    output = run_command(['file', file_path])
    if output:
        file_info_arr = output.split(", ")
        return {
            "file_type": file_info_arr[0],
            "architecture": file_info_arr[1],
            "version": file_info_arr[2],
            "linking": file_info_arr[3],
            "interpreter": file_info_arr[4] if len(file_info_arr) > 4 else None,
            "build_id": file_info_arr[5] if len(file_info_arr) > 5 else None,
            "os": file_info_arr[6] if len(file_info_arr) > 6 else None
        }
    return None


def get_file_hash(file_path: str) -> str:
    '''Returns sha256 file hash.'''
    output = run_command(['sha256sum', file_path])
    if output:
        return output.split()[0]
    return None


def get_strings(file_path: str) -> list:
    '''Returns strings associated with the file as a list.'''
    output = run_command(['strings', file_path])
    if output:
        return output.splitlines()
    return None


def get_header(file_path: str) -> dict:
    '''Returns ELF header as a structured dictionary.'''
    output = run_command(['readelf', '-h', file_path])
    if output:
        return {"header": output.splitlines()}
    return None


def get_shared_libraries(file_path: str) -> list:
    '''Returns external shared libraries used in the file as a list.'''
    output = run_command(['ldd', file_path])
    if output:
        return output.splitlines()
    return None

def get_entropy(file_path):
    with open(file_path, 'rb') as f:
        byte_arr = f.read() 

    file_size = len(byte_arr)
    
    if file_size == 0:
        return 0  
    
    byte_freqs = Counter(byte_arr)

    entropy = 0.0
    for freq in byte_freqs.values():
        p_x = freq / file_size
        entropy -= p_x * math.log2(p_x)

    return entropy

# # Example Usage
# file_path = '/home/blueteamtortoise/project2-main/attack-a'

# file_info = get_file_info(file_path)
# if file_info:
#     print(f"File Info: {json.dumps(file_info, indent=4)}")

# file_hash = get_file_hash(file_path)
# if file_hash:
#     print(f"File hash: {file_hash}")

# strings = get_strings(file_path)
# if strings:
#     print(f"Strings: {json.dumps(strings, indent=4)}")

# header = get_header(file_path)
# if header:
#     print(f"Header: {json.dumps(header, indent=4)}")

# libraries = get_shared_libraries(file_path)
# if libraries:
#     print(f"Libraries: {json.dumps(libraries, indent=4)}")
