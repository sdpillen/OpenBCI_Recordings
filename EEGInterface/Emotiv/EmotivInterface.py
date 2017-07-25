import CCDLUtil.EEGInterface.EEGInterfaceParent as EEGParent
import Constants
import ctypes as ct
import sys
import time
import numpy as np


class EmotivStreamer(EEGParent.EEGInterfaceParent):

    def __init__(self, out_buffer_queue, eeg_file_path, lib_path, channels_for_live='All', put_data_on_out_queue_flag=False, data_save_queue=None, subject_name=None, subject_tracking_number=None,
                 experiment_number=None):
        # call parent constructor
        super(EmotivStreamer, self).__init__(channels_for_live=channels_for_live, out_buffer_queue=out_buffer_queue, data_save_queue=data_save_queue, put_data_on_out_queue_flag=put_data_on_out_queue_flag,
                                              subject_name=subject_name, subject_tracking_number=subject_tracking_number, experiment_number=experiment_number)
        sys.path.append(Constants.LIB_PATH)
        # load Emotiv library for streamer
        self.lib_path = lib_path
        print self.lib_path
        self.libEDK = ct.cdll.LoadLibrary(self.lib_path)
        self.eeg_file_path = eeg_file_path

    def setup_var(self):
        return self.libEDK.EE_EmoEngineEventCreate(), self.libEDK.EE_EmoStateCreate(), ct.c_uint(0), ct.c_uint(0), ct.c_uint(0), ct.c_uint(1726), ct.c_float(1), ct.c_int(0)


    def start_recording(self):
        self.start_recording_and_saving_data(self.eeg_file_path)


    def start_recording_and_saving_data(self, eeg_file_path):
        '''
        Start saving the recorded 
        :param eeg_file_path: 
        :return: 
        '''
        # set up variables
        e_event, e_state, user_id, n_samples, n_sam, composer_port, secs, state = self.setup_var()
        # pointers
        n_samples_taken = ct.pointer(n_samples)
        data = ct.pointer(ct.c_double(0))
        user = ct.pointer(user_id)
        ready_to_collect = False
        # start connection
        print "Connecting..."
        if self.libEDK.EE_EngineConnect("Emotiv Systems-5") != 0: # connection failed
            print "Emotiv Engine start up failed."
            self.stop_connection(e_event=e_event, e_state=e_state)
            sys.exit(1)
        print "Connected! Start receiving data..."
        # write data to file
        f = open(eeg_file_path, 'w')
        # write header
        print >>f, Constants.HEADER
        h_data = self.libEDK.EE_DataCreate()
        self.libEDK.EE_DataSetBufferSizeInSec(secs)
        # start recording
        while True:
            state = self.libEDK.EE_EngineGetNextEvent(e_event)
            if state == 0:
                event_type = self.libEDK.EE_EmoEngineEventGetType(e_event)
                self.libEDK.EE_EmoEngineEventGetUserId(e_event, user)
                # add user
                if event_type == 16:
                    print "User added"
                    self.libEDK.EE_DataAcquisitionEnable(user_id, True)
                    ready_to_collect = True
            if ready_to_collect:
                self.libEDK.EE_DataUpdateHandle(0, h_data)
                self.libEDK.EE_DataGetNumberOfSample(h_data,n_samples_taken)
                # print "Updated :", n_samples_taken[0]
                if n_samples_taken[0] != 0:
                    n_sam = n_samples_taken[0]
                    arr = (ct.c_double*n_samples_taken[0])()
                    ct.cast(arr, ct.POINTER(ct.c_double))
                    #self.libEDK.EE_DataGet(h_data, 3,byref(arr), nSam)
                    data = np.array('d') # zeros(n_samples_taken[0],double)
                    for sampleIdx in range(n_samples_taken[0]):
                        for i in range(22):
                            self.libEDK.EE_DataGet(h_data, Constants.TARGET_CHANNEL_LIST[i], ct.byref(arr), n_sam)
                            print >>f,arr[sampleIdx],",",
                        # write our own time stamp
                        print >>f, time.time(),
                        # switch line
                        print >>f,'\n'
            time.sleep(0.2)
        # not sure the use of this in the original program...
        libEDK.EE_DataFree(h_data)


    def stop_connection(self, e_event, e_state):
        self.libEDK.EE_EngineDisconnect()
        self.libEDK.EE_EmoStateFree(e_state)
        self.libEDK.EE_EmoEngineEventFree(e_event)



