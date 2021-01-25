from flask import Flask
from flask import request
from flask import render_template
import os
import json
import datetime
import mido

#Functions

def get_sessions(daycontent):
    sessions = []
    current_session = 0
    insession = False
    for item in daycontent:
        if len(item) == 2 and type(item) == list and item[0]=="unplugged":
            if insession:
                insession = False
                current_session+=1
        else:
            if insession == False:
                sessions.append([item[0],[]])
                insession = True
            sessions[current_session][1].append(item)
    return sessions


#App
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',days=os.listdir("savefiles"))
@app.route('/viewday/')
def viewday():
    day=request.args.get("day")
    sessions=[]
    for session in get_sessions(json.loads(open("savefiles/"+day,"rb").read().decode())):
        sessions.append(datetime.datetime.fromtimestamp(int(session[0])).strftime("%I:%M:%S %p"))
    return render_template('viewday.html',sessions=sessions,day=day)
@app.route('/viewsession/')
def viewsession():
    session_requested=request.args.get("session")
    day=request.args.get("day")
    sessions=[]
    sessions_retreived=get_sessions(json.loads(open("savefiles/"+day,"rb").read().decode()))
    for session in sessions_retreived:
        sessions.append(datetime.datetime.fromtimestamp(int(session[0])).strftime("%I:%M:%S %p"))
    notes=sessions_retreived[sessions.index(session_requested)][1]
    notes_pretty = []
    note_times = []
    last_note_time = -1
    for note_group in notes:
        for note in note_group[1]:
            note_times.append(note[1]+(note_group[0]*1000))
    for note_group in notes:
        for note in note_group[1]:
            if (note[1]+(note_group[0]*1000))-min(note_times) >= last_note_time:
                notes_pretty.append([(note[1]+(note_group[0]*1000))-min(note_times),note[0]])
                last_note_time = (note[1]+(note_group[0]*1000))-min(note_times)
    return render_template('viewsession.html',session=session_requested,notes=notes_pretty,day=day)
@app.route('/tomidi/')
def tomidi():
    session_requested=request.args.get("session")
    day=request.args.get("day")
    sessions=[]
    sessions_retreived=get_sessions(json.loads(open("savefiles/"+day,"rb").read().decode()))
    for session in sessions_retreived:
        sessions.append(datetime.datetime.fromtimestamp(int(session[0])).strftime("%I:%M:%S %p"))
    notes=sessions_retreived[sessions.index(session_requested)][1]
    notes_pretty = []
    note_times = []
    last_note_time = -1
    for note_group in notes:
        for note in note_group[1]:
            note_times.append(note[1]+(note_group[0]*1000))
    for note_group in notes:
        for note in note_group[1]:
            if (note[1]+(note_group[0]*1000))-min(note_times) >= last_note_time:
                notes_pretty.append([(note[1]+(note_group[0]*1000))-min(note_times),note[0]])
                last_note_time = (note[1]+(note_group[0]*1000))-min(note_times)

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    for event in notes_pretty:
        current_message = mido.parse(event[1][0:3])
        track.append(current_message.copy(time=round(mido.second2tick((event[0])/1000,480,120))))
    mid.save(datetime.datetime.strftime(datetime.datetime.strptime(session_requested+day,"%I:%M:%S %p%Y-%m-%d.json"),"%Y-%m-%d-%H-%M-%S")+'.mid')
    return ""
