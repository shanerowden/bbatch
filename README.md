*WIP*

# bbatch v0.2
This is the Basis for An Attempt to Make Big Batch Moves and Write Data on Some of My Files...

+ version 0.2 -- added bdata.py
+ version 0.1 -- started with the mess of bbatch.py

### UTILITY: 
To get the most use out of this tool right now, you should have a directory full of other directories with many files inside of them that you would like to pull out and organize in the project root.
Right now it will not walk subdirs inside of subdirs -- it's actively pulling files to the project root from only one level of directory depth. This is mainly because doing more than that at one time means putting more effort into making sure files can get unique names.


### PREREQUISITES
+ Be using Linux.
+ Install python3
+ Install virtualenv


### INSTALL
```bash
apt install python3 python3-pip
python3 -m pip install virtualenv

git clone https://github.com/shanerowden/bbatch.git
cd bbatch

python3 -m virtualenv venv
source venv/bin/activate

python -m pip install -r requirements.txt

chmod u+x bbatch
```

#### USAGE EXAMPLE
Before running the script, this is an example directory path with the listed contents. Lets pretend I have included the hundreds of directories instead of just these.

```
user@host:/path/to/test/$ ls
Archaic/                          dist/               genwrapper.py      img-resize/      mancer-term/             
backup_simpai/                    dproj/              GetBackInto/       InstagramAPI/    moviepy_testing/        
bbatch/                           es6/                get_good_django/   interject-lib/   nameless-space-replace/
```

When you run this command...

```bash
./bbatch '/path/to/project/root/' ['json']
```

*Notes on Command Arguments*
+ It's pretty simple.
+ Use first argument to set the PROJECT ROOT.
+ Use an optional 'json' at the end if you prefer; leave it blank for pickle.
+ If the program cannot find a project root it will attempt to make `/home/$USER/mcf2pd-test/`
+ You can also do this if you think it's more sophisticated:
    
```bash
export MCF2PD_DEST="/path/to/project/root/"
python3 bbatch.py
```

...it will start like this:
    
```
Looking for Path to project DEST in exported env variable MCF2PD_DEST
Found at /path/to/project/root/
Really Delete Switch is Set to -- False
TYPE "DEL" to set to True > DEL
Really going to delete. Press Any Key > 
LENGTH OF DIRS: 54
LENGTH OF FILES: 203
PRESS ANY KEY > 
Checking path: /path/to/project/root/README.md
ALREADY EXISTS: /path/to/project/root/README.md
Checking path: /path/to/project/root/LICENSE
ALREADY EXISTS: /path/to/project/root/LICENSE
Checking path: /path/to/project/root/LICENSE
ALREADY EXISTS: /path/to/project/root/LICENSE
Checking path: /path/to/project/root/webpack.config.js
FILE WILL BE MOVING: /path/to/project/root/vanilla-terminal-CLONE/webpack.config.js TO /path/to/project/root/webpack.config.js
```

...and go on to...

```
MOVING TO NEW PATH: /path/to/project/root/webpack.config.js
MOVING TO NEW PATH: /path/to/project/root/jest.config.js
MOVING TO NEW PATH: /path/to/project/root/webpack.config.js
MOVING TO NEW PATH: /path/to/project/root/jest.config.js
SRC: README.md - size 1230
DEST: README.md - size 4070
SRC: LICENSE - size 35141
DEST: LICENSE - size 1067
SRC: LICENSE - size 1076
DEST: LICENSE - size 1067
SRC: README.md - size 4070
DEST: README.md - size 4070
NOTICE: vanilla-terminal-CLONE/README.md is the same size as README.md
SRC: package.json - size 1247
DEST: package.json - size 1299
```

When it starts comparing file sizes, it is try to determine if files that it cannot move are the same files that exist somewhere else or if they are different files. If they are different, the program will leave them in their directories but if they're the same, it will move them and reduce the excess copies.

```
DELETING: /path/to/project/root/webpack.config.js - size 621
DELETING: /path/to/project/root/jest.config.js - size 438
All files were moved from dirs to /path/to/project/root/
ADDING: onesettings.py to dict text/plain, us-ascii
ADDING: FTP in python to dict text/x-python, utf-8
ADDING: bootstrap-4.0.0.zip to dict application/zip, binary
ADDING: work.html to dict text/html, us-ascii
ADDING: wiki_random.py to dict text/plain, us-ascii
ADDING: selectors.json to dict text/plain, us-ascii
ADDING: site_health.py to dict text/plain, us-ascii
```

It eventually gets to here, where it's actually finishing up with moving files. It's now trying to take account of what is there, and adding it to a dict for serialization.

```
Data Successfully Serialized
Files Contents Were Stored to Data /path/to/project/root/files.pickle
LOADED PICKLE: /path/to/project/root/files.pickle
>>>
```

When it's finished, it leaves you in the shell with the data loaded as a dict, `d`.

## LATEST UPDATES
I added these [bdata.py functions](https://github.com/shanerowden/bbatch/blob/master/bdata.py). Use this to play with them in the REPL:

```bash
python -i bdata.py
```

You can also do this after you have ran `bbatch` or `bbatch.py` at least once to generate either `file.json` or `file.pickle`.

Right now the main use case of that util is loading up the data and leaving you in the python interactive shell where you can do things like this: All files that contain 'html' in their MIME type; or files that did not contain `binary` encoding. 

There are other possible queries but I'm looking at moving to sqlite3 sooner than later where that will solve itself.

```py
>> htmls
[{'name': 'rsa.mp4', 'param': 'mime', 'value': 'html'}]

>> notbin
[{'name': 'files.json', 'param': 'charset', 'value': 'us-ascii'},
 {'name': 'mcf2pd.py', 'param': 'charset', 'value': 'us-ascii'},
 {'name': 'rsa.mp4', 'param': 'charset', 'value': 'us-ascii'},
 {'name': 'dsf.py', 'param': 'charset', 'value': 'us-ascii'}]
```

I determined that these were the mimes found in one of my directory datasets.

```py
>> mimes_found
{'application/CDFV2', 'video/x-matroska', 'text/plain', 'video/webm', 'text/x-python', 'video/mp4', 'video/ogg', 'text/html', 'video/x-msvideo', 'video/mpeg', 'image/gif', 'application/octet-stream'}

>>> charsets_found
{'us-ascii', 'binary'}
```

Thanks for looking at it. Open to suggestion, correction, review, etc.
Refer to [bdata.py functions](https://github.com/shanerowden/bbatch/blob/master/bdata.py) to see how I did this.
