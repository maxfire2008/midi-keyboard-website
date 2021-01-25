import json
import pickle
import pygame.midi
import time
import os
import datetime

while True:
    try:
        print("Initilising -",time.time())
        devicedata=[]

        device_init_time = time.time()
        pygame.midi.init()
        device_id=pygame.midi.get_default_input_id()
        mididevice=pygame.midi.Input(device_id,100)

        wait_end=time.time()+10
        reset_pushover=time.time()
        print("Ready -",time.time())
        while True:
            if time.time()>wait_end:
                wait_end=time.time()+2
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                if current_date+".json" in os.listdir("savefiles"):
                    oldlog = pickle.load(open("savefiles/"+current_date+".pickle","rb"))
                    pickle.dump(oldlog+devicedata,open("savefiles/"+current_date+".json","wb"))
                else:
                    pickle.dump(oldlog+devicedata,open("savefiles/"+current_date+".json","wb+"))
            midi_device_latest_output=mididevice.read(100)
            if len(midi_device_latest_output)>0:
                for msg in port.iter_pending():
                    devicedata.append([time.time(),msg])
            if len(midi_device_latest_output) > 0:
                reset_pushover=time.time()
            if reset_pushover+5 < time.time():
                print("Reseting -",time.time())
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                if current_date+".json" in os.listdir("savefiles"):
                    oldlog = pickle.load(open("savefiles/"+current_date+".pickle","rb"))
                    pickle.dump(oldlog+devicedata,open("savefiles/"+current_date+".json","wb"))
                else:
                    pickle.dump(oldlog+devicedata,open("savefiles/"+current_date+".json","wb+"))
                break
        pygame.midi.quit()
    except Exception as e:
        print(e,"-",time.time())
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if current_date+".json" in os.listdir("savefiles"):
            oldlog = pickle.load(open("savefiles/"+current_date+".pickle","rb"))
            pickle.dump(oldlog+devicedata,open("savefiles/"+current_date+".json","wb"))
        else:
            pickle.dump(oldlog+devicedata,open("savefiles/"+current_date+".json","wb+"))
        pygame.midi.quit()
        time.sleep(5)
