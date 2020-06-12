# bbatch
This is the Basis for An Attempt to Make Big Batch Moves and Write Data on Some of My Files... 

## version 0.1

### UTILITY: 
Move child files in sub dirs of a root parent directly into the parent,
removing all of the child dirs if possible without overwriting anything.
After processing, saves all the file contents of the project PROOT directory
a data stucture for additional processing.

To get the most use out of this tool right now, you should have a directory full of other directories with many files inside of them that you would like to pull out and organize in the project root.
Right now it will not walk subdirs inside of subdirs -- it's active pulling files to the project root from only one level of directory depth

### PREREQUISITES
1. Install python3 -- `apt install python3`
2. Be Using Linux -- `python3 -m pip install virtualenv`

+ Optionally, you can have virtualenv to do venvs and automate installing requirements as they are needed. Currently there is not much need though.

### INSTALL: 
```bash
git clone https://github.com/shanerowden/bbatch.git
cd bbatch
python3 -m virtualenv venv
source venv/bin/activate
python -m pip install -r requirements.txt
chmod u+x bbatch
```

### USAGE
```bash
./bbatch <'/path/to/project/root/'> <'json'>
```

+ Use first argument to set the PROJECT ROOT Absolute Path
+ Use an optional second that can only be 'json' if you prefer that to pickle data
+ 'json' tells the script to serialize data to json instead of pickle.
+ Just leave blank and do `python3 main.py` if you prefer pickle.

### NOTE ON PROJECT PATH
If the program cannot find a project root it will attempt to make one at 
`/home/$USER/mcf2pd-test/` -- but there will be no files there to process.
