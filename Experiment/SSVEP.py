import random
import time
import numpy as np
import CCDLUtil.SignalProcessing.Fourier as Fourier
import CCDLUtil.DataManagement.QueueManagement as QueueManagement
import CCDLUtil.Utility.Constants as Constants
import CCDLUtil.EEGInterface.BrainAmp.BrainAmpInterface as BrainAmp
import CCDLUtil.EEGInterface.OpenBCI.OpenBCIInterface as OpenBCI
from CCDLUtil.Graphics.CursorTask.CursorTask import CursorTask

# some constants for the SSVEP demo
STEP = 100
CURSOR_RADIUS = 60
ROTATE = 'rotate'
DONT_ROTATE = 'dont_rotate'
EEG_COLLECT_TIME_SECONDS = 30
WINDOW_SIZE_SECONDS = 2
EEG = None
# EEG = Constants.EEGSystemNames.BRAIN_AMP 


def initialize_eeg(live_channels, subject_name='Default', openbci_port=5):
    """
    :param live_channels: the channels to take live data
    :param subject_name: the name of the subject
    :param openbci_port: the communication with OpenBCI devices 
    :return eeg_system: the eeg data streamer object
    """
    eeg_system = None
    if EEG == Constants.EEGSystemNames.BRAIN_AMP:
        eeg_system = BrainAmp.BrainAmpStreamer(channels_for_live=live_channels, live=True, save_data=True, subject_name=subject_name)
    elif EEG == Constants.EEGSystemNames.OpenBCI:
        eeg_system = OpenBCI.OpenBCIStreamer(channels_for_live=live_channels, live=True, save_data=True, subject_name=subject_name, port=openbci_port)
    return eeg_system


def initialize_graphics(width=1920, height=1080):
    """
    :param width: the width (pixels) of the screen
    :param height: the height (pixels) of the screen
    :return CursorTask object
    """
    return CursorTask(screen_size_width=width, screen_size_height=height, window_x_pos=1920)


def trial_logic(eeg_system, out_buffer_queue, cursor_task, fs, high_freq, low_freq, prompt, window_width,
                sleep_time_if_not_ran=2):
    """
    Run a full trial of SSVEP experiment.

    :param eeg_system: Used EEG system (or None)
    :param out_buffer_queue: the queue to retrieve live data
    :param bgm: graphics task object (BlockGameManager)
    :param fs: sampling rate
    :param high_freq: the high frequency density we need
    :param low_freq: the low frequency density we need
    :param prompt: the prompt sentence to show on SSVEP screen
    :param window_width: the pixel width of the window
    :param sleep_time_if_not_ran: time to sleep if eeg_system == None
    :return: the answer, stop early or late
    """
    # start graphics
    cursor_task.show_all()
    cursor_task.hide_tb_flags()
    cursor_task.hide_crosshair()
    cursor_task.reset_cursor()
    # set the prompt
    cursor_task.set_text_dictionary_list({'text': prompt, 'pos': (None, 150), 'color': (255, 0, 0)})
    # graphic related constants
    cursor_x = window_width // 2
    boundary_left = 200
    boundary_right = window_width - 200
    # mark start time
    start_time = time.time()
    # If our EEG system is None, we'll sleep for a bit and then return a random result
    if eeg_system is None:
        time.sleep(sleep_time_if_not_ran)
        steps = 10
        packet_index = 0
        while packet_index < steps:
            x = random.randint(0, 1)
            # compare densities of 17Hz and 15Hz frequencies
            time.sleep(2)
            if x == 0:
                cursor_x += STEP
                cursor_task.move_cursor_delta_x(STEP)
            else:
                cursor_x -= STEP
                cursor_task.move_cursor_delta_x(-STEP)
            # if we reach left boundary
            if cursor_x - CURSOR_RADIUS <= boundary_left:
                cursor_task.collide_left()
                time.sleep(2)
                return ROTATE, start_time, time.time()
            # right boundary
            if cursor_x + CURSOR_RADIUS >= boundary_right:
                cursor_task.collide_right()
                time.sleep(2)
                return DONT_ROTATE, start_time, time.time()
            packet_index += 1
    else:
        # Else we run the system for real
        QueueManagement.clear_queue(out_buffer_queue)
        # shape of sample is : (sample, channel)
        packet = np.asarray(out_buffer_queue.get())
        # print "received packet: ", packet
        samples_per_packet = packet.shape[0]

        # get constants for full trial
        single_trial_duration_samples = EEG_COLLECT_TIME_SECONDS * fs
        single_trial_duration_packets = int(single_trial_duration_samples / samples_per_packet)

        # get constants for single window
        window_size_samples = WINDOW_SIZE_SECONDS * fs
        window_size_packets = window_size_samples / samples_per_packet

        # b is the np array to hold all data in single trial
        b = np.zeros(shape=(single_trial_duration_samples,))
        packet_index = 0
        while packet_index < single_trial_duration_packets:
            # insert the visualizer here
            packet = out_buffer_queue.get()  # Gives us a (10, 1) matrix.
            # print "received packet: ", packet
            # get the sample
            samples = np.squeeze(packet)      # Gives us a (10,) array
            sample_index = packet_index * samples_per_packet
            b[sample_index: sample_index + samples_per_packet] = samples
            packet_index += 1
            # if we have enough samples, perform FFT on a single window
            if packet_index != 0 and packet_index % window_size_packets == 0:
                # print "packet index: ", packet_index, ", do FFT"
                window = b[packet_index * samples_per_packet - window_size_samples:packet_index * samples_per_packet]
                # perform FFT
                freq, density = Fourier.get_fft_all_channels(data=np.expand_dims(np.expand_dims(window, axis=0), axis=2),
                                                             fs=fs, noverlap=fs // 2, nperseg=fs)
                # compare densities of 17Hz and 15Hz frequencies
                # print density.shape
                if density[0][high_freq][0] <= density[0][low_freq][0]:
                    cursor_x += STEP
                    cursor_task.move_cursor_delta_x(STEP)
                else:
                    cursor_x -= STEP
                    cursor_task.move_cursor_delta_x(STEP)
                # if we reach left boundary
                if cursor_x - CURSOR_RADIUS <= boundary_left:
                    cursor_task.collide_left()
                    return ROTATE, start_time, time.time()
                # right boundary
                if cursor_x + CURSOR_RADIUS >= boundary_right:
                    cursor_task.collide_right()
                    return DONT_ROTATE, start_time, time.time()

    # if time runs out, find which side cursor is closest to
    if cursor_x <= window_width // 2:
        cursor_task.collide_left()
        time.sleep(2)
        cursor_task.hide_all()
        cursor_task.show_crosshair()
        return ROTATE, start_time, time.time()
    else:
        cursor_task.collide_right()
        time.sleep(2)
        cursor_task.hide_all()
        cursor_task.show_crosshair()
        return DONT_ROTATE, start_time, time.time()


if __name__ == '__main__':
    eeg = initialize_eeg(None)
    out_buffer_queue = None if eeg is None else eeg.out_buffer_queue
    cursor_task = initialize_graphics(width=1680, height=1050)
    # some questions
    prompt_lst = ['Are dogs animals?', 'Do you like cheesecakes?', 'Is beef edible?']
    # start
    for prompt in prompt_lst:
        trial_logic(eeg, out_buffer_queue, cursor_task, 500, 17, 15, prompt, cursor_task.screen_width)
