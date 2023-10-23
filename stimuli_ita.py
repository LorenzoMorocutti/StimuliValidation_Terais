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

participant = sys.argv[1]

images_dir = "/home/cmazzola/Documents/Projects/Shared_Drawing/Stimuli Validation/Terais-main/Immagini/"

if os.path.isdir(images_dir):
    print("folder already exist")
else:
    os.mkdir(images_dir)

####### CHANGE THE PATH
now = datetime.now()
date_hour = now.strftime("_%d-%m-%Y_%H:%M:%S")
participant_dir = participant + str(date_hour)
path_folder_participant = images_dir + participant_dir
os.mkdir(path_folder_participant)

seq_strokes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
num_strokes = {'stroke_n': seq_strokes}

strokes_file = path_folder_participant+"/strokes.csv"

if os.path.isfile(strokes_file):
    print("file already exist")
else:
    f = open(strokes_file, "x")
    df_init = pd.DataFrame(num_strokes)
    df_init.to_csv(strokes_file, mode='w', index=False, header=True)

dels_file = path_folder_participant + "/dels.csv"
f = open(dels_file, "x")

seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # 0 is ambulance, 1 is owl, 2 is flower
random.shuffle(seq)
categories = ['Ambulanza', 'Trattore', 'Gufo',
              'Treno', 'Pecora', 'Lampadina',
              'Leone', 'Torta Di Compleanno',
              'Ape', 'Sirenetta', 'Fiore',
              'Ragno', 'Foglia', 'Pizza',
              'Volto', 'Bus', 'Palma']


number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
button = []

global win

####### CHANGE THE PATH
script_path = "/home/cmazzola/Documents/Projects/Shared_Drawing/Stimuli Validation/Terais-main/drawing_ita.py"
script_path_trial = "/home/cmazzola/Documents/Projects/Shared_Drawing/Stimuli Validation/Terais-main/drawing_trial.py"

drawing_enjoyment = 0
drawing_frequency = 0
drawing_percentage = 0

difficulty_ranking = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
enjoyment_ranking = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
likeability_ranking = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

latency_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
total_drawing_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
number_of_strokes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def drawing_questions(n):
    text = visual.TextStim(win, text="Quanto è stato difficile disegnare la categoria: \n" + categories[n] + "? \n\n"
                            "(1 - per nulla difficile, 7 - estremamente difficile)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
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
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()


    text = visual.TextStim(win, text="Quanto ti è piaciuto disegnare la categoria: \n" + categories[n] + "? \n\n"
                            "(1 - per niente piaciuto, 7 - estremamente piaciuto)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
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
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()


    text = visual.TextStim(win, text="Quanto ti piace il disegno che hai realizzato della categoria: \n" + categories[n] + "? \n"
                            "(1 - per niente, 7 - estremamente)",
                           color=(1, 1, 1), pos=(0.0, 20.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()


    image = visual.ImageStim(win, image=path_folder_participant + "/" + categories[n] + ".png", size=(600, 400),
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
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()


    return


def drawing_activity(i):

    win.close()
    print("window closed, ready to open drawing")

    p = subprocess.Popen(["python3", script_path, str(i), participant_dir], stdout=subprocess.PIPE)
    p.wait()

    output = []
    output = p.stdout.read()

    array = []

    array = np.fromstring(output.decode(), dtype=float, sep=',')

    print(i)
    print(array)

    latency_time[i] = array[0]
    print(latency_time[i])
    total_drawing_time[i] = array[1]
    print(total_drawing_time[i])
    number_of_strokes[i] = array[2]
    print(number_of_strokes[i])

    configure()

    text = visual.TextStim(win, text="Ora rispondi ad alcune domande, per favore.", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    
    button = visual.ButtonStim(win, text="Premi per continuare", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[0, -250], size=(400, 150), units='pix')
    button.draw()
    
    win.flip()

    touch=False
    
    while touch==False:
    	if myMouse.isPressedIn(button):
    		touch=True
    win.flip()

    drawing_questions(i)

    return


def drawing_task(n):

    text = visual.TextStim(win, text="Sei pronto/a per disegnare?", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    
    button = visual.ButtonStim(win, text="Premi per continuare", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[0, -250], size=(400, 150), units='pix')
    button.draw()
    
    win.flip()

    touch=False
    
    while touch==False:
    	if myMouse.isPressedIn(button):
    		touch=True


    time.sleep(0.5)


    text = visual.TextStim(win, text="Per favore, attendi che il foglio bianco si apra \n e disegna con il tuo dito la categoria...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)

    text2 = visual.TextStim(win, text=categories[n], color=(1, -0.7, -0.7), pos=(0.0, -2.0),
                           colorSpace='rgb', bold=True, height=5, anchorHoriz="center", wrapWidth=500)

    text.draw()
    text2.draw()
    
    print(categories[n])

    win.flip()

    time.sleep(5)

    drawing_activity(n)

    return




def artistic_questions():
    global drawing_enjoyment, drawing_frequency, drawing_percentage

    text = visual.TextStim(win, text="Quanto ti piace disegnare a mano libera?\n(1 - estremamente poco, 7 - estremamente tanto)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
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
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()

    text = visual.TextStim(win, text="Quanto spesso realizzi disegni a mano libera?\n(1 - estremamente poco, 7 - estremamente tanto)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
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
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)
    
    blue_window()

    text = visual.TextStim(win, text="Immagina altre 100 persone disegnare le tue stesse immagini:\n"
                                     "quante di loro pensi che potrebbero realizzarle meglio di te?\n "
                                     "(0% - praticamente nessuno, 100% - praticamente tutti)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()

    space = 0

    button.append(visual.ButtonStim(win, text="0%", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                                    pos=[-800, -250], size=(100, 100), units='pix'))

    for i in range(0, 10):

        button.append(visual.ButtonStim(win, text=number[i]+"0%", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[-640 + space, -250], size=(100, 100), units='pix'))
        space += 160

    for j in range(0, 11):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 11):
            if myMouse.isPressedIn(button[k]):
                drawing_percentage = k*10
                touch = True


    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)


    return


def blue_window():
    blue_poly = visual.Polygon(win, edges=4, fillColor=[-0.4, -0.4, 1], colorSpace='rgb', pos=[0, 0], size=[4000, 4000], units='pix', ori=0)
    blue_poly.draw()
    win.flip()  # show the stim
    time.sleep(0.001)

    return


# function to wait for the touch of the mouse
def wait_touch():
    myMouse.clickReset
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
    viewdist = 25.4
    monitorname = 'testMonitor'
    scrn = 0
    mon = monitors.Monitor(monitorname, width=monitorWidth, distance=viewdist)
    mon.setSizePix((widthPix, heightPix))

    win = visual.Window(
        monitor=mon,
        size=(widthPix, heightPix),
        color=(-0.4, -0.4, 1),
        colorSpace='rgb',
        units='deg',
        screen=scrn,
        allowGUI=False,
        fullscr=True
    )

    myMouse = event.Mouse(win)
    myMouse.setPos(newPos=(0, 0))

    return


def main():

    subprocess.run(["xrandr", "--output", "eDP-1", "--off"])
    
    configure()

    text = visual.TextStim(win, text="Benvenuto/a!\nQuesta è una prova per aiutarti\n"
                                     "a capire come si svolgerà l'attività di disegno."
                           , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    button = visual.ButtonStim(win, text="Clicca per continuare", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    text = visual.TextStim(win, text="Quando sei pronto/a, premi il bottone e apparirà,\n"
                                     "sullo schermo, un soggetto che dovrai disegnare."
                           , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    button = visual.ButtonStim(win, text="Clicca per continuare", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    text = visual.TextStim(win, text="Per favore disegna con il dito un paio di...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)

    text2 = visual.TextStim(win, text="Forbici", color=(1, -0.7, -0.7), pos=(0.0, -1.0),
                            colorSpace='rgb', bold=True, height=5, anchorHoriz="center", wrapWidth=500)

    text.draw()
    text2.draw()

    win.flip()

    time.sleep(4)

    win.close()

    p = subprocess.Popen(["python3", script_path_trial])
    p.wait()

    configure()

    text = visual.TextStim(win, text="Perfetto!\n E' tutto chiaro? Allora puoi\n"
                                     "procedere con il vero esperimento."
                           , color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    button = visual.ButtonStim(win, text="Clicca per continuare", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3],
                               pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    text = visual.TextStim(win, text="Benvenuto/a!\nTi chiederemo di disegnare diverse immagini \n"
                                     "e poi di rispondere ad alcune semplici domande.\n"
                                     "Sei pronto/a? "
                                     " \n\nClicca per continuare", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    
    button = visual.ButtonStim(win, text="Premi per continuare", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                              pos=[0, -250], size=(400, 150), units='pix')
    button.draw()
    
    win.flip()

    touch=False
    
    while touch==False:
    	if myMouse.isPressedIn(button):
    		touch=True
    

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

    df_art.to_csv('art_data.csv', mode='a', header=True)



    # Create a data frame from the results
    df_rank = pd.DataFrame(rank_results, index=[participant])

    df_rank.to_csv('rank_data.csv', mode='a', header=True)



    # Create a data frame from the results
    df_time = pd.DataFrame(time_stroke_results, index=[participant])

    df_time.to_csv('time_data.csv', mode='a', header=True)


    # Create a data frame with all the info about difficulty, enjoyment etc.
    df_dels = pd.DataFrame(dels_data)

    df_dels.to_csv(dels_file, mode='w', header=True)



    text = visual.TextStim(win, text="Grazie mille per il tuo contributo!", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    win.flip()

    wait_touch()
    
    subprocess.run(["xrandr", "--output", "eDP-1", "--mode", "1920x1080", "--panning", "1920x1080", "--pos", "1920x0", "--primary"])

if __name__ == '__main__':
    main()

    sys.exit()
