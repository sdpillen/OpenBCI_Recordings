import sys
sys.path.insert(0, 'C:\Users\Experimenter\PycharmProjects\MagStimInterface')  # This is a hack and should probably be fixed at some point.
from datetime import datetime
import web
from Magstim.MagstimInterface import Rapid2
import time
import requests
from threading import Lock, Thread

# Separate thread that keeps the TMS awake (unneeded if server is running)
class MaintainCommunication(Thread):
    def run(self):
        while True:
            web.STIMULATOR_LOCK.acquire()
            web.STIMULATOR.remocon = True
            web.STIMULATOR_LOCK.release()
            time.sleep(0.5)

#  Arms, fires, and disarms TMS TMS using old MagStim (fires at specified value instead of range)
#  Returns a string of the time that the TMS was fired.
class TMS():
    def __init__(self):
        web.STIMULATOR = Rapid2(port='COM2')
        web.STIMULATOR_LOCK = Lock()

        # The TMS gets sleepy and needs to be woken up every half second
        poller = MaintainCommunication()
        poller.daemon = True
        poller.start()

    def tms_arm(self):
        web.STIMULATOR.disable_safety()
        web.STIMULATOR.armed = True

    def is_armed(self):
        return web.STIMULATOR.armed

    # returns epoc
    def tms_fire(self, i):
        assert type(i) is int
        assert 0 < i <= 100
        web.STIMULATOR.disable_safety()
        web.STIMULATOR.intensity = i
        time.sleep(1.5)
        web.STIMULATOR.trigger()
        return time.time()

    def tms_disarm(self):
        web.STIMULATOR.armed = False

    def set_intensity(self, intensity):
        time.sleep(2)
        intensity = int(intensity)
        assert 0 < intensity <= 100
        web.STIMULATOR.intensity = intensity


if __name__ == '__main__':
    fire_twice = False
    tms = TMS()
    tms.tms_arm()
    if fire_twice:
        time.sleep(0.5)
        tms.tms_fire(10)
        time.sleep(2)
        tms.tms_fire(20)
        time.sleep(0.5)
    else:
        time.sleep(2.5)
        tms.tms_fire(20)
    time.sleep(0.5)
    tms.tms_disarm()
