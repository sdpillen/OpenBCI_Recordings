__author__ = 'Darby Losey'
import sys
from datetime import datetime
import web
from Magstim.MagstimInterface import Rapid2
import time
import requests
from threading import Lock, Thread

####
# Methods to fire TMS using server (Unrecommended to use because of latency in server). Must run server to use.
####
def set_and_fire_high_server(intensity):
    if 0 < intensity <= 100:
        requests.post("http://localhost:25000/web.STIMULATOR/power/high/" + str(intensity))
        time.sleep(2)
        requests.post("http://localhost:25000/web.STIMULATOR/fire/high")


def set_and_fire_low_server(intensity):
    if 0 < intensity <= 100:
        requests.post("http://localhost:25000/web.STIMULATOR/power/low/" + str(intensity))
        time.sleep(2)
        requests.post("http://localhost:25000/web.STIMULATOR/fire/low")


def set_high_server(intensity):
    if 0 < intensity <= 100:
        requests.post("http://localhost:25000/web.STIMULATOR/power/high/" + str(intensity))


def set_low_server(intensity):
    if 0 < intensity <= 100:
        requests.post("http://localhost:25000/web.STIMULATOR/power/low/" + str(intensity))


def fire_high_server():
    requests.post("http://localhost:25000/web.STIMULATOR/fire/high")


def fire_low_server():
    requests.post("http://localhost:25000/web.STIMULATOR/fire/low")


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
        web.STIMULATOR = Rapid2(port='COM1')
        web.STIMULATOR_LOCK = Lock()

        # The TMS gets sleepy and needs to be woken up every half second
        poller = MaintainCommunication()
        poller.daemon = True
        poller.start()

    def tms_arm(self):
        web.STIMULATOR.disable_safety()
        web.STIMULATOR.armed = True
        time.sleep(2.5)

    def tms_set_intensity(self, intensity):
        if 0 < intensity <= 100 and isinstance(intensity, int):
            web.STIMULATOR.disable_safety()
            web.STIMULATOR.intensity = intensity
            time.sleep(2.5)
        else:
            raise ValueError("Intensity provided out of range: TMS can only fire with 0 < intensity <= 100")

    def tms_fire(self):
        assert 0 < web.STIMULATOR.intensity <= 100
        web.STIMULATOR.trigger()
        fire_time = str(datetime.now()).replace(" ", "_") + " "
        return fire_time

    def tms_disarm(self):
        web.STIMULATOR.armed = False

if __name__ == '__main__':
    fire_twice = True
    tms = TMS()
    tms.tms_arm()
    if fire_twice:
        tms.tms_set_intensity(10)
        tms.tms_fire()
        time.sleep(2)
        tms.tms_set_intensity(10)
        time.sleep(0.5)
    else:
        tms.tms_set_intensity(40)
        tms.tms_fire()
    time.sleep(1.0)
    tms.tms_disarm()
