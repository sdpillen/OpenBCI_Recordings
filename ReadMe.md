# CCDLUtil

## Introduction

This is a library initially set up by Darby Losey (loseydm@uw.edu) for the use in the creating and 
analysis of noninvasive BCI (EEG and TMS) experiments.  This module contains scripts
ranging from experimental setup to data analysis.

It is important that all code committed to this repository is:

    1) Heavily commented, such that it a function can be understood someone without reading the code. At minimum, 
           please provide docstrings (comments detailing what a function does) to every funtions written, no matter how basic.
    2) Well maintained - please only commit code that is predominantly PEP8 complient
           See https://www.python.org/dev/peps/pep-0008/ for details
           If commiting uncompleted or untested code, please mark it with a todo comment.
    3) Generalizeable enough that it can be used for multiple projects.
            Please do not hard code constants. Instead pass them to the funcion as a default parameter.
            Please refactor functions that "do too much work".
    4) Please include detailed commit messages when pushing code.
            Please do not commit unversionalbe items (such as .pyc files).
            Please see https://help.github.com/articles/ignoring-files/ if you are unsure how to do this.  A basic .gitignore file is included in this repo.
            

## Instructions for use

This is intended as a general library.  If using, please clone into your site-packages folder (if using Windows; an example path
C:\Python27\Lib\site_packages), or another folder that is in your working path.

I renamed this project from DLUtil to CCDLUtil.  If cloning from gitlab, you may
need to rename the folder it clones into (from DLUtil -> CCDLUtil) for imports
to work properly.

## Recommendations for Getting Started


##### Multithreading/multiprocessing:

This module (and nearly all complex programs) require multithreading/multiprocessing.

Here is a link to the api for threading:
https://docs.python.org/2/library/threading.html

Here is a quick intro to multithreading:
https://pymotw.com/2/threading/

Here is a link to the api for multiprocessing (this is intended to have
the same face as the threading module, but different 'under the hood'
characteristics -- use a multiprocessing.queue() for
communicating between processes):
https://docs.python.org/2/library/multiprocessing.html


##### Communication between threads:
Here is a link for using queues to communicate between threads/processes
https://docs.python.org/2/library/queue.html

##### Anonymous functions:
This module also abuses anonymous functions. Read more here:
http://www.secnetix.de/olli/Python/lambda_functions.hawk

## Additional Documentation
           
Please include descriptions of any new modules you create in readme files.

Additional documentation is available in the CCDL/Documentation folder.

## Dependencies
Runs with python 2.7.  Some modules many not require all dependencies. 

    numpy
    scikit-learn
    wxpython
    pygame
    scipy
    ast
    pyaml
    json

## Suggested Data Formats

#### Epoched and unepoched EEG Data

As a standard convention used in this library, all epoched data is saved in the form (epoch, sample, channel).
All unepoched data is saved (sample, channel)

### Log Files

It may be helpful to save events to file in the form: str(trial_dictionary) + \n, with the dictionary containing information relating to a single trial.
Most files have a 1st line that contains meta information.

Because data is saved in this format, each file can be parsed as such:
    
    for line in file:
        trial_dictionary = ast.literal_eval(line)

Where trial_dictionary is a python dictionary with keys such as 'start_time', which contain relevant info pertaining to that trial.
This reduces the need to write scripts to parse individual log files.

## Common Code

If there is code that is commonly used, please include it here.

##### Assert Statements:
    import CCDLUtil.Utility.AssertVal as AV

##### Pickle Files

To load pickle files, call:

    import CCDLUtil.DataManagement.FileParser as FP
    FP.load_pickle_file(pickle_file_path)

#### Git
###### How to make git ignore about previously tracked file that are added to .gitignore:


     git rm --cached -r .
     git add .

See this link for reference:
http://stackoverflow.com/questions/1274057/how-to-make-git-forget-about-a-file-that-was-tracked-but-is-now-in-gitignore

###### Pull from remote, but ignoring (and overwriting!) local changes:

    git fetch origin master
    git reset —hard FETCH_head
    git clean -df
    

## CCDL General Documentation

See the Documentation module for additional documentation.

### Open BCI

##### Equipment Instructions
The dongle and board also have different settings.  For standard data collection, insure that the
switches on the side are set properly:

    Dongle: Switch toward computer
    Board: Switch toward PC.

##### Known Errors
The OpenBCI board will not run properly the second time it starts unless
it is physically reset between runs.  Therefore, every time the program is run you must:


        1. Unplug the dongle and turn off the board
        2. Plug in the dongle
        3. Turn on the board.

See the "Error Messages" section below to see markers of this error.

#### Problems with the touch screen

    Occasionally on restart, the touchscreen mapping will be wrong.
    To fix:
        1) Search and select "Tablet PC Settings"
        2) At the top, hit configure your pent and touch displays setup
        3) Select the correct touchscreen


## Common Error Messages / Troubleshooting
[C:\Python27\Lib\site-packages\CCDLUtil\DataManagement](C:%5CPython27%5CLib%5Csite-packages%5CCCDLUtil%5CDataManagement)
* Problems Importing
This should be resolved, but if there is a problem with some of the scripts in this module failing to import,
change the scripts to import from CCDLUtil.Module.Script.  As all of the CCDLUtil repo was in the working path when first developed,
there may be some remaining import Module.Script commands, which will fail if imported from another working
path.  As said before, this should be fixed already, but if I missed it in a few spots, please let me know

Other importing problems - This module was originally named DLUtil. Because of this, it is possible
that when cloning the module, it will clone into a folder called DLUtil. This needs to be CCDLUtil 
in order to work.



* This error means that you are accessing a wxpython object in an unsafe manner. Make sure to use locks, even if you are running everything in the same thread.
wxpython does some threading automatically and they did not make their code thread safe.


            1. Pango:ERROR:/build/pango1.0-_EsyGA/pango1.0-1.40.1/./pango/pango-layout.c:3925:pango_layout_check_lines: assertion failed: (!layout->log_attrs)


* This error likely comes from specifying the directory and not the specific file for loading a TF object.
This provides a very long, complicated error message.  The portion shown below is the last segment.


            2. DataLossError (see above for traceback): Unable to open table file
            /data/Subject3/Subject3_TF: Failed precondition: Subject3/Subject3_TF: perhaps your file is in a
            different file format and you need to use a different restore operator?
             [[Node: save/restore_slice = RestoreSlice[dt=DT_FLOAT, preferred_shard=-1,
             _device="/job:localhost/replica:0/task:0/cpu:0"](_recv_save/Const_0, save/restore_slice/tensor_name, save/restore_slice/shape_and_slice)]]

* This error likely comes about from not stripping off a trailing comma in some versions of data collected from the brain amp system.
    ** The new method takes care of this.

        3.File "/DataInterface/Utility/FileParser.py", line 118, in iter_func
        yield dtype(item)
        ValueError: could not convert string to float:


* OpenBCI Disconnect


        WARNING:root:Skipped 46 bytes before start found
        Warning: Skipped 46 bytes before start found
        WARNING:root:ID:<15> <Unexpected END_BYTE found <0> instead of <192>
        Warning: ID:<15> <Unexpected END_BYTE found <0> instead of <192>
        WARNING:root:Skipped 466 bytes before start found
        'NoneType' object has no attribute 'channel_data' 'NoneType' object has no attribute 'channel_data'

* OpenBCI - Communication Problems

    WARNING:root:No Message

    This means there is a communication problem between the dongle and
    the board. Make sure both are on and that the dongle actually belongs
    to the board (ie, they didn't get mixed up)

    This could also mean that the COM port was entered incorrectly and my
    script autodetect the wrong one (not sure why this happens sometimes,
    please do fix it if you figure out why).


* BrainAmp Disconnect/Software not on
    
    Ensure that the proprietary BrainAmp software is running and the BrainAmp system is fully conenected (see Documentation folder for more details)
    Otherwise, this is the common error message:
    

        No connection could be made because the target machine actively refused it

# Running 20 Questions

Please see Documentation/gUSBAmp for how to set up the hardware.

Use ActiCap software to monitor impedance.  However, impedences cannot
be monitored concurrently with data recording.

Please see Documentation/Projects/20Questions for instructions on how to run this project.

# Other / Misc.
* Zero based indexing versus 1 based indexing: 
http://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html