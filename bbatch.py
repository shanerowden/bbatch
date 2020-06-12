from pathlib import Path
from pprint import pprint as pp
import subprocess
import pickle
import sys
import json
import os
import getpass

'''
bbatch.py
UTILITY: Move child files in sub dirs of a root parent directly into the parent,
          removing all of the child dirs if possible without overwriting anything.
          After processing, saves all the file contents of the project PROOT directory
          a data stucture for additional processing.

Author: Shane Rowden
License: GNU Geneeral Public License 3.0
Version: 0.1

Usage: "python3 mcf2pd.py [serialize_with]"
[serialize_with] 'json' tells the script to serialize data to json instead of pickle.
                  Just leave blank if you prefer pickle.
'''


# GLOBAL
REALLY_DELETE_SWITCH = False  


def init_root_dir():
    print('Looking for Path to project PROOT in exported env variable MCF2PD_PROOT')
    try:
        PROOT = Path(os.environ.get('MCF2PD_PROOT'))
        print(f'Found at {PROOT}')
    except TypeError:
        print("Failed to find this variable in the environment.")
    finally:
        if isinstance(PROOT, Path) and PROOT.is_dir():
            return PROOT
    
    try:
        print("Attempting to use my Local Dev Environment Module Hacks...")
        from dev_hacks import MY_PROOT_PATH  # Just a local dev environment hack
        return MY_PROOT_PATH
    except ModuleNotFoundError:
        print(f"Module Hack not found -- attempting to make a test directory at {PROOT}")
    finally:
        PROOT = Path.home() / getpass.getuser() / "mcf2pd-test"
    
    try:
        PROOT.mkdir(parents=True)
        os.path.chdir(PROOT)
        return PROOT
    except (PermissionError, FileNotFoundError):
        print(f"Permission Denied or '{PROOT}' Does Not Exist for Some Reason Still")
    except FileExistsError:
        pass
    finally:
        assert isinstance(PROOT, Path) and PROOT.is_dir()
    
    return PROOT

PROOT = init_root_dir()
PICKLE = PROOT / 'files.pickle'
JSON = PROOT / 'files.json'


def parse_data_opt(args=sys.argv):
    '''
    For now uses sys.argv instead of argparse to determine if the 'json' option is used.
    This is the only argument atm.
    '''
    _, *a = args
    #a = a.splstrip()
    if a[0] == 'json':
        return True
    else:
        print('Failed to parse args. Use no arguments or specify \n'\
            + 'Use "python3 script.py json" if you want')
            

def init_get_paths(get_generator=False):
    '''
    This is used to apply the global values used at the bottom if __naame__ == '__main__'
    It directs to get_files_and_dirs, under the assumption that this is the main script.
    '''
    return get_files_and_dirs(get_generator=get_generator)

def get_files_and_dirs(get_generator=False):
    '''
    Uses the get_generator option to allow usage of len() for some operations, namely removing
    files and determing if that is safe; and being able to make the files and firs iterable as a gen
    for improved speed when building the data structure and serializing it
    '''
    if get_generator:
        dirs =  (d for d in PROOT.iterdir() if d.is_dir())
        files = (f for f in PROOT.iterdir() if f.is_file())
        return dirs, files
    else:
        dirs =  [d for d in PROOT.iterdir() if d.is_dir()]
        files = [f for f in PROOT.iterdir() if f.is_file()]
        if len(dirs) != 0:
            print(f'LENGTH OF DIRS: {len(dirs)}')
        print(f'LENGTH OF FILES: {len(files)}')
        return dirs, files

def remove_empty_dirs(dirs):
    '''
    Checks if the contents of a directory inside of PROOT is empty and removes it if so
    '''
    for d in dirs:
        child_paths = [p for p in d.iterdir()]
        if len(child_paths) == 0:
            d.rmdir()
            print(f'REMOVING EMPTY DIR: {d}')

def get_files_ready_to_move():
    '''
    Checks every directory in PROOT and gathers every file inside (no subdirs) and processes it for moving
    Checks if the destination outside of the directory in PROOT is already existing and would overwrite
    another file. It returns a list of tuples, for srcs and dests for move jobs 
    '''
    files_ready_to_move = []
    for child_dir in DIRS:
        child_files = [f for f in child_dir.iterdir() if f.is_file()]
        for f in child_files:
            POSSIBLE_DEST = PROOT / f.name
            print(f'Checking path: {POSSIBLE_DEST}')
            if POSSIBLE_DEST.exists():
                print(f'ALREADY EXISTS: {POSSIBLE_DEST}')
            else:
                f_dest = POSSIBLE_DEST
                print(f"FILE WILL BE MOVING: {f.parent / f} TO {f_dest}")
                files_ready_to_move.append((f, f_dest))
    return files_ready_to_move

def move_all_files(jobs):
    '''
    Moves the files
    TODO This actually seems to repeat the check made in get_files_ready_to_move
    '''
    for job in jobs:
        s, d = job
        if s in FILES:
            print("Already a file named {s}; skipping...")
        else:
            s = s.resolve()
            d = d.resolve()
            print(f'MOVING TO NEW PATH: {d}')
            s.rename(d)

def check_if_dupe_files_same_size():
    '''
    Processes all files to determine if the file in the files with the same names in both PROOT and
    the child_dir are also the same size, confirming it's safe to just delete the one in the child_dir
    Returns a list of confirmed files for deletion
    
    TODO: You shouldn't need to assemble the possible dupes again. 
          You already did a similar process
          in get_files_ready_to_move
    '''
    maybe_dupes = []
    confirmed_dupes = []
    for child_dir in DIRS:
        child_files = [(f, PROOT / f.name) for f in child_dir.iterdir() if f.is_file()]
        maybe_dupes += child_files
        
    for f in maybe_dupes:
        s, d = f
        print(f'SRC: {s.name} - size {s.stat().st_size}')
        print(f'PROOT: {d.name} - size {d.stat().st_size}')
        
        if d.exists():
            size = (s.stat().st_size, d.stat().st_size)
            if size[0] == size[1]:
                print(f'NOTICE: {s.parent.name}/{s.name} is the same size as {d.name}')
                confirmed_dupes.append(s.resolve())
    return confirmed_dupes

def remove_old_paths(delete_list, delete=REALLY_DELETE_SWITCH):
    '''
    The function that actually deletes the files
    '''
    for f in delete_list:
        if delete:
            f.unlink()
            print(f'REMOVING: {f}')
        else:
            print(f'TEST REMOVE: {f}')

def delete_all_with_low_size(files):
    '''
    prints files with low bytes of size, the min value is adjustable in remove_files_and_store_data()
    '''
    pp(files)
    for f in files:
        if f.exists():
            print(f'DELETING: {f.resolve()} - size {f.stat().st_size}')
            f.unlink()
        else:
            print(f'NOTICE: Encoutered file that does not exist -- {f.name}')


def run_file_shell_command_on_all(files, is_json):
    '''
    Determines qualities of all files, like mimetype, charset... Uses subprocess in bash to accomplish this.
    TODO: Will not work in windows
    '''
    d = get_data_dict(
        data_is_json=False if is_json else True
    )
    for f in files:
        command_spec = ['file', '-i', f]
        output = subprocess.run(
            command_spec, stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        path, mime, charset = parse_file_command_output(output)
        path = Path(path)
        d[path.name] = {'abspath': str(path.resolve()), 'mime': mime, 'charset': charset}
        print(f'ADDING: {path.name} to dict {mime}, {charset}')
    return d


def parse_file_command_output(string):
    '''
    a helper func -- this parses the output from the bash "file" command returning it in a format 
    usable in the dict returned by  run_file_shell_command_on_all()
    '''
    p, meta = string.strip().split(':')
    m, c = meta.split(';')
    c = c.split('charset=')[1]
    return p.strip(), m.strip(), c.strip()

def get_data_dict(empty=True, data_is_json=False):
    '''
    By default initializes a dict object; otherwise, it uses the PATH constants and the presencse of
    the command line argument from parse_data_opt() to determine if serialized in pickle or json
    Will always default to pickle.
    '''
    if empty:
        return {}
    
    if PICKLE.exists() and not data_is_json:
        with PICKLE.open('rb') as fo:
            d = pickle.load(fo)
            print(f'LOADED PICKLE: {PICKLE}')
        return d
    
    elif JSON.exists() and data_is_json:
        with JSON.open('r') as fo:
            d = json.load(fo)
            print(f'LOADED JSON DATA: {JSON}')
        return d
        
    elif not DATA_PATH.exists():
        print(f"NO PICKLE FILE AT: {PICKLE} -- Writing File")
        return get_data_dict()

def init_serialize_data(path):
    '''
    helper of get_data_dict() -- confirms if the user wants to serialize to the path, writing over it...
    '''
    if path.exists():
        data_type = path.name.split('.')[-1].upper()
        prompt = f'\nWRITE OVER {data_type} FILE? Yn?\n> '
        confirm = input(prompt).lower()
        if confirm.startswith('y'):
            return
        else:
            print('Cannot Confirm. Aborting...')
            sys.exit()

def pickle_dict(data):
    '''
    Serialize data to pickle file
    '''
    with PICKLE.open('wb') as fo:
        pickle.dump(data, fo)

def jsonify_dict(data):
    '''
    Serialize data to json file
    '''
    with JSON.open('w') as fo:
        json.dump(data, fo)
        

def main_remove_files_and_store_data(read_from_json_opt=False, min_size=1000):
    '''
    First function called by main() after parse_data_opt()
    Assembles files as a list iterable, moves the files, assembles dupes, removes dupes,
    Reassembles the files as they will now be changed, and sends them to store_data_changes_after_removal
    The min_size option will cause any file smaller than this in bytes to be removed Default is 1kb.
    '''
    mv_jobs = get_files_ready_to_move()
    move_all_files(mv_jobs)
    
    dupes = check_if_dupe_files_same_size()
    remove_old_paths(dupes)
    
    new_dirs, new_files = get_files_and_dirs()
    delete_all_with_low_size(
        [f for f in new_files if f.stat().st_size < min_size]
    )
    remove_empty_dirs(new_dirs)
    print(f"All files were moved from dirs to {PROOT}")

    store_data_changes_after_removal(
        read_from_json_opt=read_from_json_opt
    )
    print(f"Files Contents Were Stored to Data {JSON if read_from_json_opt else PICKLE}")

def store_data_changes_after_removal(read_from_json_opt=False):
    '''
    Represents a data gathering process after file changes or having done no file changes
    Its purpose is for storing the file data. Uses the parse_data_opt() func to determine file type.
    This is what you should use if calling a data gathering process from another module.
    '''
    _, remaining_files = get_files_and_dirs(get_generator=True)
    
    data = run_file_shell_command_on_all(
        remaining_files, is_json=True if read_from_json_opt else False
    )
    
    init_serialize_data(
        JSON if read_from_json_opt else PICKLE
    )
    if read_from_json_opt:
        jsonify_dict(data)
    else:
        pickle_dict(data)
        
    print('Data Successfully Serialized')
 

def really_delete_opt(really_delete=REALLY_DELETE_SWITCH):
    '''
    Notice of Delete Switch Setting and Option to Turn it On or Back Out
    '''
    print(f"Really Delete Switch is Set to -- {really_delete}")
    if not really_delete:
        inp = input('TYPE "DEL" to set to True > ').lower()
        if 'del' in inp:
            really_delete = True
            inp = input("Really going to delete. Press Any Key > ")
            return really_delete
    else:
        inp = input("Really going to delete. Press Any Key > ")
        return REALLY_DELETE_SWITCH


def main():
    '''
    Move all files inside of child dirs of PROOT directly into root if this is safe.
    Clean up empty dirs. Remove duplicate files if found. Serialize data after.
    '''
    data_option = parse_data_opt()
    if data_option:
        print(f"You have selected to serialize to json")
    input("PRESS ANY KEY > ")
    
    main_remove_files_and_store_data(
        read_from_json_opt=data_option
    )
    
    data = get_data_dict(
        empty=False, data_is_json=data_option
    )
    return data


if not __name__ == '__main__':
    DIRS, FILES = init_get_paths(get_generator=True)
else:
    # Change to True when ready to really Delete Files
    REALLY_DELETE_SWITCH = really_delete_opt()
    DIRS, FILES = init_get_paths()
    
    d = main()

