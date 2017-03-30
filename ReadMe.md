# DLUtil

## Introduction

This is a library initially set up by Darby Losey (loseydm@uw.edu) for the use in the creating and 
analysis of noninvasive BCI (EEG and TMS) experiments.  This module contains scripts
ranging from experimental setup to data analysis.

It is important that all code committed to this repository is:
    
    1) Heavily commented, such that it a function can be understood someone without reading the code. At minimum, 
           please provide docstrings (comments detailing what a function does) to every funtions written, no matter how basic.
    2) Well maintained - please only commit code that is predominantly PEP8 complient
           See https://www.python.org/dev/peps/pep-0008/ for details
    3) Generalizeable enough that it can be used for multiple projects.
            Please do not hard code constants. Instead pass them to the funcion as a default parameter.
            Please refactor functions that "do too much work".
    4) Please include detailed commit messages when pushing code.
            Please do not commit unversionalbe items (such as .pyc files).
            Please see https://help.github.com/articles/ignoring-files/ if you are unsure how to do this.  A basic .gitignore file is included in this repo.
            

### Instructions for use

This is intended as a general library.  If using, please clone into your site-packages folder (if using Windows; an example path
C:\Python27\Lib\site_packages), or another folder that is in your working path.

            
### Additional Documentation
           
Please include descriptions of any new modules you create in readme files. 

### Dependencies
Runs with python 2.7.  Some modules many not require all dependencies. 

    numpy
    scikit-learn
    wxpython
    pygame
    scipy
    ast
    pyaml
    json

### Data Formats

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
    import DLUtil.Utility.AssertVal as AV

##### Pickle Files

To load pickle files, call:

    import DLUtil.DataManagement.FileParser as FP
    FP.load_pickle_file(pickle_file_path)

#### Git
###### How to make git ignore about previously tracked file that are added to .gitignore:


     git rm --cached -r .
     git add .

See this link for reference:
http://stackoverflow.com/questions/1274057/how-to-make-git-forget-about-a-file-that-was-tracked-but-is-now-in-gitignore

 
    

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


### Common  Error Messages

1. This error means that you are accessing a wxpython object in an unsafe manner. Make sure to use locks, even if you are running everything in the same thread.
wxpython does some threading automatically and they did not make their code thread safe.


    1. Pango:ERROR:/build/pango1.0-_EsyGA/pango1.0-1.40.1/./pango/pango-layout.c:3925:pango_layout_check_lines: assertion failed: (!layout->log_attrs)

2. This error likely comes from specifying the directory and not the specific file for loading a TF object.
This provides a very long, complicated error message.  The portion shown below is the last segement.


    2. DataLossError (see above for traceback): Unable to open table file /media/darby/ExtraDrive1/PycharmProjects/DataInterface/data/Ninja/Subject3/Subject3_TF: Failed precondition: /media/darby/ExtraDrive1/PycharmProjects/DataInterface/data/Ninja/Subject3/Subject3_TF: perhaps your file is in a different file format and you need to use a different restore operator?
	 [[Node: save/restore_slice = RestoreSlice[dt=DT_FLOAT, preferred_shard=-1, _device="/job:localhost/replica:0/task:0/cpu:0"](_recv_save/Const_0, save/restore_slice/tensor_name, save/restore_slice/shape_and_slice)]]

3. This error likely comes about from not stripping off a trailing comma in some versions of data collected from the brain amp system.
    ** The new method takes care of this.


    3.File "/DataInterface/Utility/FileParser.py", line 118, in iter_func
    yield dtype(item)
    ValueError: could not convert string to float:


4. OpenBCI Disconnect


    WARNING:root:Skipped 46 bytes before start found
    Warning: Skipped 46 bytes before start found
    WARNING:root:ID:<15> <Unexpected END_BYTE found <0> instead of <192>
    Warning: ID:<15> <Unexpected END_BYTE found <0> instead of <192>
    WARNING:root:Skipped 466 bytes before start found
    'NoneType' object has no attribute 'channel_data' 'NoneType' object has no attribute 'channel_data'
