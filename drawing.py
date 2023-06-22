import tkinter as tk
import sys
import time
import numpy as np
from psychopy import event, visual, monitors, core
from PIL import Image, ImageTk, ImageGrab
import pandas as pd
import os
import csv

n = int(sys.argv[1])
participant = sys.argv[2]

start = time.time()

path_images_folder = "/home/cmazzola/Documents/Projects/Shared_Drawing/Stimuli Validation/Terais-main/Images/"
strokes_file_path = path_images_folder + participant + "/strokes.csv"


x_coor = []
y_coor = []

xy_coordinates_0 = []
xy_coordinates_1 = []
xy_coordinates_2 = []
xy_coordinates_3 = []
xy_coordinates_4 = []
xy_coordinates_5 = []
xy_coordinates_6 = []
xy_coordinates_7 = []
xy_coordinates_8 = []
xy_coordinates_9 = []
xy_coordinates_10 = []
xy_coordinates_11 = []
xy_coordinates_12 = []
xy_coordinates_13 = []
xy_coordinates_14 = []
xy_coordinates_15 = []
xy_coordinates_16 = []
xy_coordinates_17 = []
xy_coordinates_18 = []
xy_coordinates_19 = []
xy_coordinates_20 = []
xy_coordinates_21 = []
xy_coordinates_22 = []
xy_coordinates_23 = []
xy_coordinates_24 = []
xy_coordinates_25 = []
xy_coordinates_26 = []
xy_coordinates_27 = []
xy_coordinates_28 = []

# Initialize Tkinter
root = tk.Tk()

######### CONFIGURATION OF THE GLOBAL VARIABLES OF THE CANVAS AND SCREENSHOTS ###########

# Set dimensions of the screenshot
savelocation = ["Ambulance.png", "Tractor.png",
                "Owl.png", "Train.png",
                "Sheep.png", "Light Bulb.png",
                "Lion.png", "Birthday Cake.png",
                "Bee.png", "Mermaid.png",
                "Flower.png", "Spider.png",
                "Leaf.png", "Pizza.png", "Face.png",
                "Bus.png", "Palm Three.png"]




# Set the dimensions of the drawing window
window_width = 1920
window_height = 950

# Create the drawing canvas
canvas = tk.Canvas(root, width=window_width, height=window_height, bg='white')
canvas.pack()

button = tk.Button(text="If you finished, press the button", command=lambda: quit_program(), height=4)
button.pack()

# Set the color and size for drawing
draw_color = 'black'
draw_size = 5

# Store the coordinates of the previous point
prev_x = None
prev_y = None

# Keep track of the number of strokes
stroke_count = 0

do_one_time = True
total_drawing_time = 0.0
latency = 0.0
temp = 0.0
margin = 0.0

############################### END OF THE CONFIGURATION ################################

 


############ FUNCTIONS TO DRAW AND TO SAVE THE FINAL DRAWINGS #############
# Define the event handler for mouse movements
def on_mouse_move(event):
    global prev_x, prev_y, stroke_count, do_one_time, latency

    while do_one_time:
        latency = time.time() - start
        do_one_time = False
        #print(latency)
        root.after(10000, lambda: alert_window())
        root.after(15000, lambda: quit_program())


    x = event.x
    y = event.y

    coor = (x, y)
    
    if stroke_count==0:
        xy_coordinates_0.append(coor)
    elif stroke_count==1:
        xy_coordinates_1.append(coor)
    elif stroke_count==2:
        xy_coordinates_2.append(coor)
    elif stroke_count==3:
        xy_coordinates_3.append(coor)
    elif stroke_count==4:
        xy_coordinates_4.append(coor)
    elif stroke_count==5:
        xy_coordinates_5.append(coor)
    elif stroke_count==6:
        xy_coordinates_6.append(coor)
    elif stroke_count==7:
        xy_coordinates_7.append(coor)
    elif stroke_count==8:
        xy_coordinates_8.append(coor)
    elif stroke_count==9:
        xy_coordinates_9.append(coor)
    elif stroke_count==10:
        xy_coordinates_10.append(coor)
    elif stroke_count==11:
        xy_coordinates_11.append(coor)
    elif stroke_count==12:
        xy_coordinates_12.append(coor)
    elif stroke_count==13:
        xy_coordinates_13.append(coor)
    elif stroke_count==14:
        xy_coordinates_14.append(coor)
    elif stroke_count==15:
        xy_coordinates_15.append(coor)
    elif stroke_count==16:
        xy_coordinates_16.append(coor)
    elif stroke_count==17:
        xy_coordinates_17.append(coor)
    elif stroke_count==18:
        xy_coordinates_18.append(coor)
    elif stroke_count==19:
        xy_coordinates_19.append(coor)
    elif stroke_count==20:
        xy_coordinates_20.append(coor)
    elif stroke_count==21:
        xy_coordinates_20.append(coor)
    elif stroke_count==22:
        xy_coordinates_20.append(coor)
    elif stroke_count==23:
        xy_coordinates_20.append(coor)
    elif stroke_count==24:
        xy_coordinates_20.append(coor)
    elif stroke_count==25:
        xy_coordinates_20.append(coor)
    elif stroke_count==26:
        xy_coordinates_20.append(coor)
    elif stroke_count==27:
        xy_coordinates_20.append(coor)
    elif stroke_count==28:
        xy_coordinates_20.append(coor)

    if prev_x is not None and prev_y is not None:
        canvas.create_line(prev_x, prev_y, x, y, fill=draw_color, width=draw_size, tags=('stroke', stroke_count))
    prev_x = x
    prev_y = y


# Define the event handler for releasing the mouse button
def on_mouse_release(event):
    global prev_x, prev_y, stroke_count, total_drawing_time
    prev_x = None
    prev_y = None   
    
    stroke_count += 1



def alert_window():
    global temp, margin, prev_x, prev_y

    ### PSYCHOPY
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
        color=(1, 1, 1),
        colorSpace='rgb',
        units='deg',
        screen=scrn,
        allowGUI=False,
        fullscr=True
    )

    ###

    temp = time.time() - start

    text = visual.TextStim(win, text="Time to finish your drawing...", color=(-1, -1, -1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    win.flip()
    time.sleep(3)
    win.close()

    margin = time.time()

    prev_x = None
    prev_y = None

def quit_program():
    global total_drawing_time, latency, stroke_count, temp, margin

    data = []

    time.sleep(0.5)


    ImageGrab.grab().crop((65, 65, 1920, 1015)).save(path_images_folder + participant + "/" + savelocation[n])

    if temp > 0:
        temp2 = time.time() - margin
        total_drawing_time = temp + temp2
    else:
        total_drawing_time = time.time() - start

    data = np.array([latency, total_drawing_time, stroke_count])

    print(','.join(map(str, data)))
    #print(data)


    df_strokes = pd.read_csv(strokes_file_path)


    if n==0:
        new_df_strokes = df_strokes.assign(Ambulance_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3, xy_coordinates_4,
                               xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8, xy_coordinates_9,
                               xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                               xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                               xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                               xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                               xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==1:
        new_df_strokes = df_strokes.assign(Tractor_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==2:
        new_df_strokes = df_strokes.assign(Owl_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==3:
        new_df_strokes = df_strokes.assign(Train_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==4:
        new_df_strokes = df_strokes.assign(Sheep_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==5:
        new_df_strokes = df_strokes.assign(IghtBulb_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==6:
        new_df_strokes = df_strokes.assign(Lion_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==7:
        new_df_strokes = df_strokes.assign(BirthdayCake_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==8:
        new_df_strokes = df_strokes.assign(Bee_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==9:
        new_df_strokes = df_strokes.assign(Mermaid_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==10:
        new_df_strokes = df_strokes.assign(Flower_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==11:
        new_df_strokes = df_strokes.assign(Spider_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==12:
        new_df_strokes = df_strokes.assign(Leaf_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==13:
        new_df_strokes = df_strokes.assign(Pizza_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==14:
        new_df_strokes = df_strokes.assign(Face_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==15:
        new_df_strokes = df_strokes.assign(Bus_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)
    elif n==16:
        new_df_strokes = df_strokes.assign(PalmThree_coordinates=[xy_coordinates_0, xy_coordinates_1, xy_coordinates_2, xy_coordinates_3,
                                   xy_coordinates_4, xy_coordinates_5, xy_coordinates_6, xy_coordinates_7, xy_coordinates_8,
                                   xy_coordinates_9, xy_coordinates_10, xy_coordinates_11, xy_coordinates_12, xy_coordinates_13,
                                   xy_coordinates_14, xy_coordinates_15, xy_coordinates_16, xy_coordinates_17,
                                   xy_coordinates_18, xy_coordinates_19, xy_coordinates_20, xy_coordinates_21,
                                   xy_coordinates_22, xy_coordinates_23, xy_coordinates_24, xy_coordinates_25,
                                   xy_coordinates_26, xy_coordinates_27, xy_coordinates_28])

        new_df_strokes.to_csv(strokes_file_path, mode='w', index=False, header=True)

    root.destroy()

    



######################### END OF THE FUNCTIONS #############################

# Bind the mouse movement event to the canvas
canvas.bind('<B1-Motion>', on_mouse_move)

# Bind the mouse release event to the canvas
canvas.bind('<ButtonRelease-1>', on_mouse_release)


# Start the main Tkinter event loop
root.mainloop()
