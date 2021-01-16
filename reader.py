import json
import pygame.midi
import time
import os

devicedata=[]

pygame.midi.init()
device_id=pygame.midi.get_default_input_id()
mididevice=pygame.midi.Input(device_id,100)

wait_end=time.time()+10

while True:
    if time.time()>wait_end:
        wait_end=time.time()+10
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if current_date+".json" in os.listdir("savefiles"):
            oldlog = 
            json.dumps(devicedata)
    devicedata+=mididevice.read(100)
