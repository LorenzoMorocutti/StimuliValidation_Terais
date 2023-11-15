#!/usr/bin/env python3

import os
import time
import pandas as pd
import random
import wx
from psychopy import event, visual, monitors, core
import datetime
import sys
import numpy as np
import subprocess
#from statemachine import StateMachine, State
import csv
from datetime import datetime
import json
import ndjson
from nico.main import startup, setmode, shutdown
from nico.speak import speak


participant = sys.argv[1]
country = sys.argv[2]
condition = sys.argv[3]

startup()

input("Press Enter to continue...")


code_path = "/usr/local/src/robot/cognitiveinteraction/stimuli_validation/"
images_dir = code_path+"Images/"
experiment_dir = images_dir + "Experiments/"
script_path = code_path + "drawing.py"
script_path_trial = code_path + "drawing_trial.py"

if os.path.isdir(images_dir):
    print("folder already exist")
else:
    os.mkdir(images_dir)
    os.mkdir(experiment_dir)

####### CHANGE THE PATH
now = datetime.now()
date_hour = now.strftime("_%d-%m-%Y_%H-%M-%S")
participant_dir = participant + str(date_hour)
path_folder_participant = images_dir + participant_dir
os.mkdir(path_folder_participant)

dels_file = path_folder_participant + "/dels.csv"
f = open(dels_file, "x")

art_data_path = code_path + "art_data.csv"
rank_data_path = code_path + "rank_data.csv"
time_data_path = code_path + "time_data.csv"

if os.path.isfile(art_data_path):
    print("already exist")
else:
    f = open(art_data_path, "x")

if os.path.isfile(rank_data_path):
    print("already exist")
else:
    f = open(rank_data_path, "x")

if os.path.isfile(time_data_path):
    print("already exist")
else:
    f = open(time_data_path, "x")



seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # 0 is ambulance, 1 is owl, 2 is flower
random.shuffle(seq)
categories = ['Ambulance', 'Tractor', 'Owl',
              'Train', 'Sheep', 'Light Bulb',
              'Lion', 'Birthday Cake',
              'Bee', 'Mermaid', 'Flower',
              'Spider', 'Leaf', 'Pizza',
              'Face', 'Bus', 'Palm Three']


number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
button = []

global win

####### CHANGE THE PATH

drawing_enjoyment = 0.0
drawing_frequency = 0.0
drawing_percentage = 0.0

difficulty_ranking = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
enjoyment_ranking = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
likeability_ranking = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

latency_time = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
total_drawing_time = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
number_of_strokes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



def save_rankings(n):

    path_var = images_dir + "/" + str(categories[n]) + "_quantitative_data.ndjson"

    ranking_data = {
        'Participant_ID': participant,
        'Country': country,
        'Condition': condition,
        'Latency_time': latency_time[n],
        'Total_time': total_drawing_time[n],
        'Number_of_Strokes': number_of_strokes[n],
        'Enjoyment_ranking': enjoyment_ranking[n],
        'Difficulty_ranking': difficulty_ranking[n],
        'Likeability_ranking': likeability_ranking[n]
    }

    if os.path.isfile(path_var):
        with open(path_var) as f:
            data = []
            reader = ndjson.reader(f)
            for i in reader:
                data.append(i)
        data.append(ranking_data)

        # Writing items to a ndjson file
        with open(path_var, 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for d in data:
                writer.writerow(d)

    else:
        open(path_var, "x")
        with open(path_var, "w") as file:
            json.dump(ranking_data, file)

    return
def drawing_questions(n):
    text = visual.TextStim(win, text="How difficult it was to draw the " + categories[n] + "? \n"
                            "(1 - not difficult, 7 - extremely difficult)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                difficulty_ranking[n] = k + 1
                touch = True

    button.clear()
    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()


    text = visual.TextStim(win, text="How much did you enjoy drawing the " + categories[n] + "? \n"
                            "(1 - not enjoyed, 7 - extremely enjoyed)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                enjoyment_ranking[n] = k + 1
                touch = True

    button.clear()
    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()


    text = visual.TextStim(win, text="How much do you like your drawing of the " + categories[n] + "? \n"
                            "(1 - not liked, 7 - liked a lot)",
                           color=(1, 1, 1), pos=(0.0, 15.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()


    image = visual.ImageStim(win, image=path_folder_participant + "/" + categories[n] + ".png", size=(600, 337),
                             units='pix', pos=(0.0, -5.0))
    image.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[-720 + space, -300], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                likeability_ranking[n] = k + 1
                touch = True

    button.clear()
    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()
    save_rankings(n)


    return


def drawing_activity(i):

    setmode(0)

    win.close()
    print("window closed, ready to open drawing")

    p = subprocess.Popen(["python3", script_path, categories[i], path_folder_participant, condition, country, experiment_dir], stdout=subprocess.PIPE)
    p.wait()

    output = []
    output = p.stdout.read()

    array = np.fromstring(output.decode(), dtype=float, sep=',')

    print(i)

    latency_time[i] = array[0]    	
    total_drawing_time[i] = array[1]
    number_of_strokes[i] = array[2]

    setmode(2)

    configure()

    text = visual.TextStim(win, text="Now please answer to some questions.", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()
    
    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[0, -250], size=(400, 150), units='pix')
    button.draw()
    
    win.flip()
    
    touch=False
    
    while touch==False:
        if myMouse.isPressedIn(button):
            touch=True

    drawing_questions(i)

    return


def drawing_task(n):

    setmode(1)

    text = visual.TextStim(win, text="Are you ready to draw?", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()
    
    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[0, -250], size=(400, 150), units='pix')
    button.draw()
    
    win.flip()
    
    touch=False
    
    while touch==False:
        if myMouse.isPressedIn(button):
            touch=True

    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)


    text = visual.TextStim(win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)

    text2 = visual.TextStim(win, text=categories[n], color=(1, -0.7, -0.7), pos=(0.0, -1.0),
                           colorSpace='rgb', bold=True, height=4.5, anchorHoriz="center", wrapWidth=400)

    text.draw()
    text2.draw()

    win.flip()

    time.sleep(4)

    drawing_activity(n)

    return




def artistic_questions():
    global drawing_enjoyment, drawing_frequency, drawing_percentage

    text = visual.TextStim(win, text="How much do you enjoy free-hand drawing? \n (1 - extremely little, 7 - extremely much)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                        pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                drawing_enjoyment = k+1
                touch = True

    button.clear()
    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()

    text = visual.TextStim(win, text="How often do you draw sketches? \n (1 - extremely little, 7 - extremely much)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                        pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                drawing_frequency = k+1
                touch = True

    button.clear()
    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()

    text = visual.TextStim(win, text="Imagine other 100 people drawing the same sketches as yours: \n"
                                     " how many of them do you think will draw better than you? \n "
                                     "(click on the slider and then drag the marker)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -350], size=(400, 150), units='pix')
    button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 100), labels=(0, 100), granularity=0.1, pos=(0, -100), size=(1000, 50),
                           units='pix')

    print(slider.markerPos)
    slider.setMarkerPos(200)
    slider.getMouseResponses()
    # slider.getRating()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button):
            drawing_percentage = rating
            touch = True

    return


def blue_window():
    blue_poly = visual.Polygon(win, edges=4, fillColor=[-0.4, -0.4, 1], colorSpace='rgb', pos=[0, 0], size=[4000, 4000], units='pix', ori=0)
    blue_poly.draw()
    win.flip()  # show the stim
    time.sleep(0.1)

    return


# function to wait for the touch of the mouse
def wait_touch():
    myMouse.clickReset()
    buttons = myMouse.getPressed()
    print(buttons)
    while buttons[0] == False | buttons[1] == False | buttons[2] == False:
        buttons = myMouse.getPressed()

    print(buttons)
    print("click")
    time.sleep(1)

    return


def configure():
    global win, widthPix, heightPix, monitorWidth, viewdist, monitorname, scrn, mon, myMouse, myKey

    widthPix = 1920
    heightPix = 1080
    monitorWidth = 50.2
    #monitorWidth = 30.9
    viewdist = 25.4
    monitorname = 'testMonitor'
    scrn = 1

    mon = monitors.Monitor(monitorname, width=monitorWidth, distance=viewdist)
    mon.setSizePix((widthPix, heightPix))

    win = visual.Window(
        monitor=mon,
        size=(widthPix, heightPix),
        color=(-0.4, -0.4, 1),
        colorSpace='rgb',
        units='deg',
        screen=scrn,
        allowGUI=True,
        fullscr=True
    )

    myMouse = event.Mouse(win)
    #myMouse.setPos(newPos=(300, 300))

    return



def main():

    #subprocess.run(["xrandr", "--output", "eDP", "--off"])
    
    configure()

    setmode(1)

    text = visual.TextStim(win, text="Welcome!\nThis is a first trial to help\n"
                                     "you understand how the drawing activity will work."
                                     , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()


    touch = False

    while touch == False:
        #print(myMouse.isPressedIn(button))

        if myMouse.isPressedIn(button):
            print(myMouse.isPressedIn(button))
            touch = True

    text = visual.TextStim(win, text="When you are ready, press the button and\n"
                                     "a subject to be drawn will appear on the screen."
                                     , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True


    text = visual.TextStim(win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)

    text2 = visual.TextStim(win, text="Scissors", color=(1, -0.7, -0.7), pos=(0.0, -1.0),
                            colorSpace='rgb', bold=True, height=4.5, anchorHoriz="center", wrapWidth=400)

    text.draw()
    text2.draw()

    win.flip()

    time.sleep(4)

    setmode(0)

    win.close()

    p = subprocess.Popen(["python3", script_path_trial])
    p.wait()

    setmode(1)

    configure()

    text = visual.TextStim(win, text="Great!\n Is everything clear? Then you can\n"
                                     "proceed with the actual experiment."
                           , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True



    text = visual.TextStim(win, text="Welcome!\nWe will ask you to draw several pictures\n"
                                     "and then answer some simple questions.\n"
                                     "Are you ready? "
                                     , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()
    
    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[0, -250], size=(400, 150), units='pix')
    button.draw()
    
    win.flip()

    touch=False
    
    while touch==False:
        if myMouse.isPressedIn(button):
            touch=True

    setmode(2)

    artistic_questions()

    for i in seq:
        drawing_task(i)




    art_results = {
        'art_enjoyment': drawing_enjoyment,
        'art_frequency': drawing_frequency,
        'art_percentage': drawing_percentage
    }

    rank_results = {
        'Ambulance_difficulty': difficulty_ranking[0],
        'Tractor_difficulty': difficulty_ranking[1],
        'Owl_difficulty': difficulty_ranking[2],
        'Train_difficulty': difficulty_ranking[3],
        'Sheep_difficulty': difficulty_ranking[4],
        'LightBulb_difficulty': difficulty_ranking[5],
        'Lion_difficulty': difficulty_ranking[6],
        'BirthdayCake_difficulty': difficulty_ranking[7],
        'Bee_difficulty': difficulty_ranking[8],
        'Mermaid_difficulty': difficulty_ranking[9],
        'Flower_difficulty': difficulty_ranking[10],
        'Spider_difficulty': difficulty_ranking[11],
        'Leaf_difficulty': difficulty_ranking[12],
        'Pizza_difficulty': difficulty_ranking[13],
        'Face_difficulty': difficulty_ranking[14],
        'Bus_difficulty': difficulty_ranking[15],
        'PalmThree_difficulty': difficulty_ranking[16],


        'Ambulance_enjoyment': enjoyment_ranking[0],
        'Tractor_enjoyment': enjoyment_ranking[1],
        'Owl_enjoyment': enjoyment_ranking[2],
        'Train_enjoyment': enjoyment_ranking[3],
        'Sheep_enjoyment': enjoyment_ranking[4],
        'LightBulb_enjoyment': enjoyment_ranking[5],
        'Lion_enjoyment': enjoyment_ranking[6],
        'BirthdayCake_enjoyment': enjoyment_ranking[7],
        'Bee_enjoyment': enjoyment_ranking[8],
        'Mermaid_enjoyment': enjoyment_ranking[9],
        'Flower_enjoyment': enjoyment_ranking[10],
        'Spider_enjoyment': enjoyment_ranking[11],
        'Leaf_enjoyment': enjoyment_ranking[12],
        'Pizza_enjoyment': enjoyment_ranking[13],
        'Face_enjoyment': enjoyment_ranking[14],
        'Bus_enjoyment': enjoyment_ranking[15],
        'PalmThree_enjoyment': enjoyment_ranking[16],

        'Ambulance_likeability': likeability_ranking[0],
        'Tractor_likeability': likeability_ranking[1],
        'Owl_likeability': likeability_ranking[2],
        'Train_likeability': likeability_ranking[3],
        'Sheep_likeability': likeability_ranking[4],
        'LightBulb_likeability': likeability_ranking[5],
        'Lion_likeability': likeability_ranking[6],
        'BirthdayCake_likeability': likeability_ranking[7],
        'Bee_likeability': likeability_ranking[8],
        'Mermaid_likeability': likeability_ranking[9],
        'Flower_likeability': likeability_ranking[10],
        'Spider_likeability': likeability_ranking[11],
        'Leaf_likeability': likeability_ranking[12],
        'Pizza_likeability': likeability_ranking[13],
        'Face_likeability': likeability_ranking[14],
        'Bus_likeability': likeability_ranking[15],
        'PalmThree_likeability': likeability_ranking[16]
    }

    time_stroke_results = {
        'Ambulance_latency': latency_time[0],
        'Tractor_latency': latency_time[1],
        'Owl_latency': latency_time[2],
        'Train_latency': latency_time[3],
        'Sheep_latency': latency_time[4],
        'LightBulb_latency': latency_time[5],
        'Lion_latency': latency_time[6],
        'BirthdayCake_latency': latency_time[7],
        'Bee_latency': latency_time[8],
        'Mermaid_latency': latency_time[9],
        'Flower latency': latency_time[10],
        'Spider_latency': latency_time[11],
        'Leaf_latency': latency_time[12],
        'Pizza_latency': latency_time[13],
        'Face_latency': latency_time[14],
        'Bus_latency': latency_time[15],
        'PalmThree_latency': latency_time[16],

        'Ambulance_total_time': total_drawing_time[0],
        'Tractor_total_time': total_drawing_time[1],
        'Owl_total_time': total_drawing_time[2],
        'Train_total_time': total_drawing_time[3],
        'Sheep_total_time': total_drawing_time[4],
        'LightBulb_total_time': total_drawing_time[5],
        'Lion_total_time': total_drawing_time[6],
        'BirthdayCake_total_time': total_drawing_time[7],
        'Bee_total_time': total_drawing_time[8],
        'Mermaid_total_time': total_drawing_time[9],
        'Flower_total_time': total_drawing_time[10],
        'Spider_total_time': total_drawing_time[11],
        'Leaf_total_time': total_drawing_time[12],
        'Pizza_total_time': total_drawing_time[13],
        'Face_total_time': total_drawing_time[14],
        'Bus_total_time': total_drawing_time[15],
        'PalmThree_total_time': total_drawing_time[16],

        'Ambulance_total_strokes': number_of_strokes[0],
        'Tractor_total_strokes': number_of_strokes[1],
        'Owl_total_strokes': number_of_strokes[2],
        'Train_total_strokes': number_of_strokes[3],
        'Sheep_total_strokes': number_of_strokes[4],
        'LightBulb_total_strokes': number_of_strokes[5],
        'Lion_total_strokes': number_of_strokes[6],
        'BirthdayCake_total_strokes': number_of_strokes[7],
        'Bee_total_strokes': number_of_strokes[8],
        'Mermaid_total_strokes': number_of_strokes[9],
        'Flower_total_strokes': number_of_strokes[10],
        'Spider_total_strokes': number_of_strokes[11],
        'Leaf_total_strokes': number_of_strokes[12],
        'Pizza_total_strokes': number_of_strokes[13],
        'Face_total_strokes': number_of_strokes[14],
        'Bus_total_strokes': number_of_strokes[15],
        'PalmThree_total_strokes': number_of_strokes[16]
    }

    dels_data={
        'Ambulance': [[difficulty_ranking[0], enjoyment_ranking[0], likeability_ranking[0], number_of_strokes[0]]],
        'Tractor': [[difficulty_ranking[1], enjoyment_ranking[1], likeability_ranking[1], number_of_strokes[1]]],
        'Owl': [[difficulty_ranking[2], enjoyment_ranking[2], likeability_ranking[2], number_of_strokes[2]]],
        'Train': [[difficulty_ranking[3], enjoyment_ranking[3], likeability_ranking[3], number_of_strokes[3]]],
        'Sheep': [[difficulty_ranking[4], enjoyment_ranking[4], likeability_ranking[4], number_of_strokes[4]]],
        'LightBulb': [[difficulty_ranking[5], enjoyment_ranking[5], likeability_ranking[5], number_of_strokes[5]]],
        'Lion': [[difficulty_ranking[6], enjoyment_ranking[6], likeability_ranking[6], number_of_strokes[6]]],
        'BirthdayCake': [[difficulty_ranking[7], enjoyment_ranking[7], likeability_ranking[7], number_of_strokes[7]]],
        'Bee': [[difficulty_ranking[8], enjoyment_ranking[8], likeability_ranking[8], number_of_strokes[8]]],
        'Mermaid': [[difficulty_ranking[9], enjoyment_ranking[9], likeability_ranking[9], number_of_strokes[9]]],
        'Flower': [[difficulty_ranking[10], enjoyment_ranking[10], likeability_ranking[10], number_of_strokes[10]]],
        'Spider': [[difficulty_ranking[11], enjoyment_ranking[11], likeability_ranking[11], number_of_strokes[11]]],
        'Leaf': [[difficulty_ranking[12], enjoyment_ranking[12], likeability_ranking[12], number_of_strokes[12]]],
        'Pizza': [[difficulty_ranking[13], enjoyment_ranking[13], likeability_ranking[13], number_of_strokes[13]]],
        'Face': [[difficulty_ranking[14], enjoyment_ranking[14], likeability_ranking[14], number_of_strokes[14]]],
        'Bus': [[difficulty_ranking[15], enjoyment_ranking[15], likeability_ranking[15], number_of_strokes[15]]],
        'PalmThree': [[difficulty_ranking[16], enjoyment_ranking[16], likeability_ranking[16], number_of_strokes[16]]]
    }


    # Create a data frame from the results
    df_art = pd.DataFrame(art_results, index=[participant])

    df_art.to_csv(art_data_path, mode='a', header=True)

    # Create a data frame from the results
    df_rank = pd.DataFrame(rank_results, index=[participant])

    df_rank.to_csv(rank_data_path, mode='a', header=True)

    # Create a data frame from the results
    df_time = pd.DataFrame(time_stroke_results, index=[participant])

    df_time.to_csv(time_data_path, mode='a', header=True)

    # Create a data frame with all the info about difficulty, enjoyment etc.
    df_dels = pd.DataFrame(dels_data)

    df_dels.to_csv(dels_file, mode='w', header=True)

    path_var = code_path + "/artistic_skills.ndjson"

    artistic_data = {
        'Participant_ID': participant,
        'Country': country,
        'Condition': condition,
        'Artistic_enjoyment': drawing_enjoyment,
        'Artistic_frequency': drawing_frequency,
        'Artistic_percentage': drawing_percentage,
        'Average_latency_time': np.mean(latency_time),
        'Average_total_time': np.mean(total_drawing_time),
        'Average_number_strokes': np.mean(number_of_strokes),
        'Average_enjoyment_ranking': np.mean(enjoyment_ranking),
        'Average_difficulty_ranking': np.mean(difficulty_ranking),
        'Average_likeability_ranking': np.mean(likeability_ranking)
    }

    if os.path.isfile(path_var):
        with open(path_var) as f:
            data = []
            reader = ndjson.reader(f)
            for i in reader:
                data.append(i)
        data.append(artistic_data)

        # Writing items to a ndjson file
        with open(path_var, 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for d in data:
                writer.writerow(d)

    else:
        open(path_var, "x")
        with open(path_var, "w") as file:
            json.dump(artistic_data, file)



    #setmode(1)

    text = visual.TextStim(win, text="Thank you very much!", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()
    win.flip()

    wait_touch()
    
    #subprocess.run(["xrandr", "--output", "eDP", "--mode", "1920x1080", "--panning", "1920x1080", "--pos", "1920x0", "--primary"])

if __name__ == '__main__':
    main()

    sys.exit()
