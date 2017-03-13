# DLUtil

## Introduction

This is a library initially set up by Darby Losey (loseydm@uw.edu) for the use in the creating and analysis of noninvasive BCI (EEG and TMS) experiments.  This module contains scripts
related to signal processing, visualization, stimuli display, tms triggering and various other utility functions.

## Standard Data Saving format

Files saved using this module will obey the format:

     SubjectX_condition

     Condition:
       _log.txt
       _OpenBCIData.csv
       _BrainAmpData.csv


## Open BCI

Dongle: Switch toward computer
Board: Switch toward PC.

Every time the program is run you must:

    1. Unplug the dongle and turn off the board
    2. Plug in the dongle
    3. Turn on the board.


## Open BCI Data montage

    Chan1 - Oz
    Chan2 - P4
    Chan3 - Pz
    Chan4 - P3
    Chan5 - Cz
    Chan6 - F4
    Chan7 - Fz
    Chan8 - F3

## Data Format

### Epoched Data
With the exception of the SentComp data (which has an nonuniform structure), all data is saved as a python pickle file.
Data is a numpy array of the format (epoch, sample, channel). Epoched data is saved in the format described in the FilePlayback
section below. This is not the only standard I have used (but it is the final standard I decided on).  Because of this,
there are other pickle files saved in various other formats.  **Files that contain FilePlayback in their name should be considered the
'final draft' of the epoched data.**

To load pickle files, call:

    Utility.FileParser.load_pickle_file(pickle_file_path)

### Raw Data

All log files are saved in the format: str(trial_dictionary) + \n, with the dictionary containing information relating to a single trial.
Most files have a 1st line that contains meta information.

Because data is saved in this format, each file can be parsed as such:
    for line in file:
        trial_dictionary = ast.literal_eval(line)

Where trial_dictionary is a python dictionary with keys such as 'start_time', which contain relevant info pertaining to that trial.
This is done so there is no need to write scripts to parse each individual file.

### File Playback Data Format.
For file playback, all data must be a pickle file the following format:

    dict -> meta, data, labels

    meta -> fs, task, data_origin, subject_num, task_type, channel_cols
        * task_type -> {Nback, Ninja}
        * data_origin -> {OpenBCI, BrainAmp}
        * fs -> sampling rate
        * channel_cols -> channel_colums for data such that data[:, channel_cols[0]:channel_cols[1], :]
                removes all auxiliary data.
        * notes -> Other notes about the trials.
        * trials to remove.

    data -> [epoch, sample, channel]
        * Note that data epochs must be the same length
        * Data that doesn't fit this criteria will be handled in a future
          version of this software

    labels ->
        [old version]
        list of dicts of len num_epochs
            labels['raw_labels'] -> list of raw labels.

This is the standard data formatting for all uniform data. The scripts to create these files are in the
preprocessing folder.

Not all files have all keys listed.



## Online Classification

Online classification works by collecting data offline and building a model on that data. This model is used
in an online platform to make predictions about mental state.

## Naming Conventions


    data_dur_path = path data is stored
    subject_dur_path = path to subject folder (in data folder)
    ..._file_path = path to file

## Utility

##### Assert Statements:
    import Utility.AssertVal as AV

## Error Messages

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

## Dependencies
Runs with python 2.7

    Numpy
    scikit-learn
    wxpython
    pygame
    scipy
    ast
    pyaml
    json
    (others...)