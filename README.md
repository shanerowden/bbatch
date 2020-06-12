# bbatch v0.2
This is the Basis for An Attempt to Make Big Batch Moves and Write Data on Some of My Files...

*This Script Works But the Code is an Absolute Mess, I am Aware...*

+ version 0.2 -- added bdata.py
+ version 0.1 -- started with the mess of bbatch.py

### UTILITY: 
To get the most use out of this tool right now, you should have a directory full of other directories with many files inside of them that you would like to pull out and organize in the project root.
Right now it will not walk subdirs inside of subdirs -- it's active pulling files to the project root from only one level of directory depth


#### TODO: needs an example dataset useage...
I'm going to work on assembling an example at some point to demonstrate what the program does that isn't a masse of unorganized stuff on my computer that I'm not going to just share as an exmaple on here. But... it works if you can figure it out.

### PREREQUISITES
1. Install python3 -- `apt install python3 python3-pip`
2. Be Using Linux -- `python3 -m pip install virtualenv`

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


### LATEST UPDATES

I added these [bdata.py functions](https://github.com/shanerowden/bbatch/blob/master/bdata.py)

```bash
python -i bdata.py
```

You can also do this after you have ran `bbatch` or `bbatch.py` at least once and serialized a `file.json` or `file.pickle` dataset:

The main functions of use there are loading up the data and leaving you in the python interactive shell where you can (in my case and examples) `pp(htmls)` or `pp(mimes)` to see what kind of files you have mixed in there.

This was the result of using the functions in `bdata.py` on some example files on my machine, searching for files that contained 'html' in their MIME type as well as files that did not contain `binary`

```py
>> html
[{'name': 'ripresa.mp4', 'param': 'mime', 'value': 'html'}]

>> notbin
[{'name': 'files.json', 'param': 'charset', 'value': 'us-ascii'},
 {'name': 'mcf2pd.py', 'param': 'charset', 'value': 'us-ascii'},
 {'name': 'ripresa.mp4', 'param': 'charset', 'value': 'us-ascii'},
 {'name': 'dsf.py', 'param': 'charset', 'value': 'us-ascii'}]
```

I determined that these were the mimes found in one of my directory datasets.

```py
>> mimes_found
{'application/CDFV2', 'video/x-matroska', 'text/plain', 'video/webm', 'text/x-python', 'video/mp4', 'video/ogg', 'text/html', 'video/x-msvideo', 'video/mpeg', 'image/gif', 'application/octet-stream'}

>>> charsets_found
{'us-ascii', 'binary'}
```

Thanks for lookig at it. Open to suggestion, correction, review, etc.
Refer to [bdata.py functions](https://github.com/shanerowden/bbatch/blob/master/bdata.py) to see how I did this.
