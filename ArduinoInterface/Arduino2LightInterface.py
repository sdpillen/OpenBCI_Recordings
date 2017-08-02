"""
This file is for communicating with the LED lights.

Note that some methods may take on the order of seconds to run.

The assumption is that this is run with the code in the SSVEP_2_LED/SSVEP_2_LED.ino script
loaded on the ardunio uno baord.

"""

import serial
import time


class Arduino2LightInterface(object):

    NO_MSG = '0'
    BOTH_ON_MSG = '1'
    BOTH_OFF_MSG = '2'
    LIGHT_3_ACTIVATE_MSG = '3'
    LIGHT_4_ACTIVATE_MSG = '4'
    LIGHT_3_DEACTIVATE_MSG = '5'
    LIGHT_4_DEACTIVATE_MSG = '6'

    VALID_ARDUINO_MESSAGES = set(map(str, range(0, 7)))

    CLOSE_PORT = 'close_port'

    def __init__(self, com_port, default_on=False):
        """
        Initializes the arduino board to the given comport.  If default_on, a message
        will be sent to the board that turns on both lights, else both lights start off.

        This method takes serial_init_post_delay to create the serial port.
        If default_on, this initialization will take an additional default_on_delay seconds.
        :param com_port: The port to connect to
        :param default_on: Will turn on lights if true and take an additional default_on_delay seconds
                            to set up.
        :param serial_init_post_delay: Time to wait after creating the serial port, defaults to 2
        :param default_on_delay: Time to wait after sending the initial command to turn on the lights
                                    defaults to 0.0.  Only relevant if default_on is True.
        """

        if type(com_port) is int:
            com_port = 'COM%d' % com_port
        self.ser = serial.Serial(com_port, 9600)
        time.sleep(2.0)
        if default_on:
            self.write(self.LIGHT_3_DEACTIVATE_MSG)
            time.sleep(2.0)

    def write(self, msg, predelay=0.0, post_delay=0.0, run_post_check=False):
        """
        Sends a message to the board.  This method takes time post_delay to run.
        If messages are sent too quickly, they may not be properly communicated to the board.
        In practice this delay is about 2 seconds, which should be fine for most purposes.

        No values are returned.

        :param msg: msg must be an str(int) between 0 and 6. For a message key use the fields of the current class
        :param predelay: Delay to wait prior to sending the message, defaults to zero
        :param post_delay: Delay to wait post sending the message, defaults to zero
        :param run_post_check: If True, will read a return message from the arduino confirming
                                communication took place.  If it didn't, it will attempt to resend
                                the message with a pre and post delay of 2 seconds.
        """
        def send_msg(to_send, delay1, delay2):
            """
            Sends the message with the given delays
            """
            time.sleep(delay1)
            self.ser.write(to_send)
            time.sleep(delay2)
            return_msg = self.ser.read(self.ser.inWaiting())  # read all characters in buffer
            return return_msg
        if msg not in self.VALID_ARDUINO_MESSAGES:
            raise ValueError('The message must be valid')
        msg = bytearray(msg, 'ascii')

        ret_msg = send_msg(to_send=msg, delay1=predelay, delay2=post_delay)
        if run_post_check and ret_msg != msg:
            print msg, " - Arduino message not delivered with delays ", predelay, post_delay,
            print "Retrying..."
            ret_msg = send_msg(to_send=msg, delay1=2, delay2=2)
            if ret_msg == msg:
                print "Arduino Message delivered"
            else:
                raise RuntimeError('Arduino communication disrupted.')

    def read_from_queue(self, queue):
        """
        Runs infinitely, taking messages from a queue for what to write to the arduino board.
        If passes a close port message, it will close the port and cease running.
        :param queue: queue to read messages from
        """

        while True:
            message = queue.get()
            if message == self.CLOSE_PORT:
                self.close_port()
                return
            else:
                self.write(msg=message)

    def close_port(self):
        """
        Closes the Arduino serial port
        """
        self.ser.close()

if __name__ == '__main__':
    "Example Use Case"
    ard = Arduino2LightInterface(com_port=10, default_on=True)
    ard.write(Arduino2LightInterface.BOTH_ON_MSG)
    time.sleep(2)
    ard.write(Arduino2LightInterface.BOTH_OFF_MSG)
    time.sleep(2)
    ard.write(Arduino2LightInterface.BOTH_ON_MSG)
    time.sleep(2)
    ard.write(Arduino2LightInterface.BOTH_OFF_MSG)
    time.sleep(2)
    ard.close_port()
