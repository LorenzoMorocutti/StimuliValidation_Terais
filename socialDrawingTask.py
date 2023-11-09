import time
import wx
import yarp
import random
import os
from psychopy import event, visual, monitors, core
from datetime import datetime
import sys
import pandas as pd
import csv
import numpy as np
from PIL import ImageGrab
import subprocess
from screeninfo import get_monitors
import json
import ndjson



def info(msg):
    print("[INFO] {}".format(msg))

    return


class socialDrawingTask(yarp.RFModule):

    def __init__(self):
        yarp.RFModule.__init__(self)

        self.module_name = None
        self.handle_port = None
        self.output_port = None
        self.input_bottle = None

        self.code_path = None
        self.drawing_path = None
        self.drawing_trial_path = None

        self.images_dir = None
        self.experiment_dir = None
        self.date_hour = None
        self.participant_dir = None
        self.participant_path = None
        self.participant_name = None
        self.artistic_skills_path = None

        self.categories = None
        self.categories_sequence = None
        self.strokes_sequence = None
        self.strokes_number = None

        self.number_button = None

        self.drawing_enjoyment = None
        self.drawing_frequency = None
        self.drawing_percentage = None
        self.difficulty_ranking = None
        self.enjoyment_ranking = None
        self.likeability_ranking = None
        self.latency_time = None
        self.total_drawing_time = None
        self.number_of_strokes = None

        self.widthPix = None
        self.heightPix = None
        self.monitorWidth = None
        self.viewdist = None
        self.monitorname = None
        self.scrn = None
        self.mon = None
        self.win = None
        self.myMouse = None

        self.country = None
        self.condition = None
        self.timestamp = None

        self.state = None

    def configure(self, rf):

        self.module_name = rf.check("name",
                                    yarp.Value("socialDrawingTask"),
                                    "module name (string)").asString()

        self.code_path = rf.check("code_path_path",
                                     yarp.Value(
                                         "/usr/local/src/robot/cognitiveinteraction/socialDrawingTask/"),
                                     "Path to the code folder (string)").asString()

        self.drawing_path = rf.check("drawing_path",
                                          yarp.Value("/usr/local/src/robot/cognitiveinteraction/socialDrawingTask/drawing.py"),
                                          "Path to the drawing script (string)").asString()

        self.drawing_trial_path = rf.check("drawing_trial_path",
                                     yarp.Value("/usr/local/src/robot/cognitiveinteraction/socialDrawingTask/drawing_trial.py"),
                                     "Path to the drawing trial script (string)").asString()

        self.images_dir = rf.check("images_dir",
                                    yarp.Value(
                                        "/usr/local/src/robot/cognitiveinteraction/socialDrawingTask/Images/"),
                                    "Path to images directory (string)").asString()

        #print(self.saving_path)

        self.monitorWidth = rf.check("monitorWidth",
                                    yarp.Value(30.9),
                                    "monitorWidth (int)").asInt32()

        self.widthPix = rf.check("widthPix",
                                    yarp.Value(1920),
                                    "widthPix (int)").asInt32()

        self.heightPix = rf.check("heightPix",
                                    yarp.Value(1080),
                                    "heightPix (int)").asInt32()

        self.viewdist = rf.check("viewdist",
                                    yarp.Value(30),
                                    "player distance from the monitor (int)").asInt32()
        self.scrn = rf.check("screen",
                                    yarp.Value(1),
                                    "display on which the experiment is run (0: main, 1: secondary)").asInt32()

        self.participant_name = rf.check("participant",
                                         yarp.Value("unnamed"),
                                         "participant name (String)").asString()

        self.country = rf.check("country",
                                         yarp.Value("Italy"),
                                         "participant country (String)").asString()

        self.condition = rf.check("condition",
                                         yarp.Value("no_robot"),
                                         "condition of the experiment (robot/no_robot) (String)").asString()

        self.artistic_skills_path = self.code_path + "/artistic_skills.ndjson"

        self.date_hour = datetime.now().strftime("_%d-%m-%Y_%H:%M:%S")
        self.participant_dir = self.participant_name + str(self.date_hour)
        self.participant_path = self.images_dir + self.participant_dir
        #self.classes_rankings_path = self.images_dir + "/classes_rankings.ndjson"

        self.categories_sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        random.shuffle(self.categories_sequence)
        self.categories = ["Ambulance", "Tractor", "Owl", "Train", "Sheep", "Light Bulb", "Lion",
                           "Birthday Cake", "Bee", "Mermaid", "Flower", "Spider", "Leaf", "Pizza",
                           "Face", "Bus", "Palm Three"]
        self.number_button = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.button = []

        self.drawing_enjoyment = 0.0
        self.drawing_frequency = 0.0
        self.drawing_percentage = 0.0

        self.difficulty_ranking = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.enjoyment_ranking = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.likeability_ranking = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        self.latency_time = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.total_drawing_time = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.number_of_strokes = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        self.monitorname = "testMonitor"
        print(self.widthPix, self.heightPix)
        self.mon = monitors.Monitor(self.monitorname, width=self.monitorWidth, distance=self.viewdist)
        self.mon.setSizePix((self.widthPix, self.heightPix))

        self.country = "IT"

        self.state = "start"

        self.handle_port = yarp.Port()
        self.attach(self.handle_port)
        self.output_port = yarp.BufferedPortBottle()
        # Create handle port to read message
        self.handle_port.open('/' + self.module_name)
        # Create output port to send info to stateController
        self.output_port.open('/' + self.module_name + '/bottle:o')

        info("Initialization complete")

        return True

    def interruptModule(self):
        print("[INFO] Stopping the module")

        self.handle_port.interrupt()
        self.output_port.interrupt()

        return True

    def close(self):
        self.handle_port.close()
        self.output_port.close()

        return True

    def respond(self, command, reply):
        # Is the command recognized
        rec = False

        reply.clear()

        if command.get(0).asString() == "set":
            if command.get(1).asString() == "start":
                self.state = "start"

        if command.get(0).asString() == "quit":
            reply.addString("quitting")
            return False

        else:

            reply.addString("here below the possible command you might want to use: \n")
            reply.addString("set + another command: to set the state machine")
            reply.addString("\t + start: ....")

            reply.addString("or, if you want to quit the module, write quit")

        return True

    def getPeriod(self):
        """
           Module refresh rate.

           Returns : The period of the module in seconds.
        """
        return 0.05


    def updateModule(self):


        if self.state == "default":
            print(self.state)

        elif self.state == "start":
            print(self.state)
            self.switch_off_screen()
            self.create_images_folder()
            self.create_participant_folder()
            self.create_ndjson_files()
            self.configuration_window()
            self.text_and_button_screen("Welcome!\nThis is a first trial to help\n"
                                     "you understand how the drawing activity will work.")
            self.text_and_button_screen("When you are ready, press the button and\n"
                                     "a subject to be drawn will appear on the screen.")
            print("finished the questions")
            self.state = "trial_question"

        elif self.state == "trial_question":
            print(self.state)
            self.category_trial_request()
            self.text_and_button_screen("Great!\n Is everything clear? Then you can\n"
                                     "proceed with the actual experiment.")
            self.state = "welcome"

        elif self.state == "welcome":
            print(self.state)
            self.text_and_button_screen("Welcome!\nWe will ask you to draw several pictures\n"
                                     "and then answer some simple questions.\n"
                                     "Are you ready? ")
            self.state = "artistic_questions"

        elif self.state == "artistic_questions":
            print(self.state)
            self.artistic_questions()
            self.state = "drawing_task"

        elif self.state == "drawing_task":
            print(self.state)
            for i in self.categories_sequence:
                self.drawing_task(i)
                self.save_rankings(i)
            self.state = "saving_data"

        elif self.state == "saving_data":
            print(self.state)
            self.save_art()
            #self.save_times()
            self.state = "end_session"

        elif self.state == "end_session":
            print(self.state)
            print("this session is completed")
            text = visual.TextStim(self.win, text="Thank you very much!", color=(1, 1, 1), pos=(0.0, 9.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
            text.draw()
            self.win.flip()

            self.wait_touch()
            self.switch_on_screen()

        return True


    def switch_off_screen(self):
        subprocess.run(["xrandr", "--output", "eDP", "--off"])
        return

    def switch_on_screen(self):
        subprocess.run(
            ["xrandr", "--output", "eDP", "--mode", "1920x1080", "--panning", "1920x1080", "--pos", "1920x0", "--primary"])
        return


    def create_images_folder(self):
        if os.path.isdir(self.images_dir):
            print("images folder already existing")
        else:
            os.mkdir(self.images_dir)
            self.experiment_dir = self.images_dir+"/Experiments"
            os.mkdir(self.experiment_dir)
        return

    def create_participant_folder(self):
        os.mkdir(self.participant_path)

    def create_ndjson_files(self):

        if os.path.isfile(self.artistic_skills_path):
            print("file already exist")
        else:
            f = open(self.artistic_skills_path, "x")

        return

    def configuration_window(self):

        print(self.scrn, self.widthPix, self.heightPix, self.monitorWidth)
        self.win = visual.Window(
            monitor=self.mon,
            size=(self.widthPix, self.heightPix),
            color=(-0.4, -0.4, 1),
            colorSpace='rgb',
            units='deg',
            screen=self.scrn,
            allowGUI=False,
            fullscr=True
        )

        self.myMouse = event.Mouse()
        self.myMouse.setPos(newPos=(0, 0))

        return

    def blue_window(self):
        blue_poly = visual.Polygon(self.win, edges=4, fillColor=[-0.4, -0.4, 1], colorSpace='rgb', pos=[0, 0],
                                   size=[4000, 4000], units='pix', ori=0)
        blue_poly.draw()
        self.win.flip()  # show the stim
        time.sleep(0.1)

    def wait_touch(self):

        self.myMouse.clickReset()
        buttons = self.myMouse.getPressed()

        print(buttons)
        while buttons[0] == False | buttons[1] == False | buttons[2] == False:
            buttons = self.myMouse.getPressed()

        print(buttons)
        print("click")
        time.sleep(0.1)

        return


    def text_and_button_screen(self, text):

        text_stim = visual.TextStim(self.win, text=text, color=(1, 1, 1), pos=(0.0, 9.0*(self.widthPix/1920)),
                           colorSpace='rgb', bold=False, height=2.0*(self.widthPix/1920), anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))

        text_stim.draw()

        button_continue = visual.ButtonStim(self.win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                   fillColor=[-0.3, -0.3, -0.3], pos=[0, -350], size=(400, 150), units='pix')

        button_continue.draw()

        self.win.flip()  # show the stim

        touch = False

        while touch == False:
            if self.myMouse.isPressedIn(button_continue):
                touch = True

        time.sleep(0.1)

        return

    def text_multiple_buttons_screen(self, text, j):

        if j == 7:
            text_stim = visual.TextStim(self.win,
                                   text=text, color=(1, 1, 1), pos=(0.0, 9.0*(self.widthPix/1920)), colorSpace='rgb', bold=False, height=2.0*(self.widthPix/1920),
                                    anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))
            text_stim.draw()

            space = 0

            for i in range(0, 7):
                self.button.append(visual.ButtonStim(self.win, text=self.number_button[i], color=[1, 1, 1], colorSpace='rgb',
                                                fillColor=[-0.3, -0.3, -0.3], pos=[-720 + space, -350*(self.widthPix/1920)], size=(100, 100), units='pix'))
                space += 240

            for k in range(0, 7):
                self.button[k].draw()

            self.win.flip()
        elif j == 10:
            text_stim = visual.TextStim(self.win, text=text, color=(1, 1, 1), pos=(0.0, 9.0*(self.widthPix/1920)), colorSpace='rgb',
                                        bold=False, height=2.0*(self.widthPix/1920), anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))
            text_stim.draw()

            space = 0

            self.button.append(visual.ButtonStim(self.win, text="0%", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, -0.3],
                                  pos=[-800, -350*(self.widthPix/1920)], size=(100, 100), units='pix'))

            for i in range(0, 10):
                self.button.append(visual.ButtonStim(self.win, text=self.number_button[i] + "0%", color=[1, 1, 1], colorSpace='rgb',
                                                fillColor=[-0.3, -0.3, -0.3],
                                                pos=[-640 + space, -350*(self.widthPix/1920)], size=(100, 100), units='pix'))
                space += 160

            for k in range(0, 11):
                self.button[k].draw()

            self.win.flip()

        return

    def text_multiple_buttons_and_image_screen(self, text, j, n):

        text_stim = visual.TextStim(self.win, text=text, color=(1, 1, 1), pos=(0.0, 9.0*(self.widthPix/1920)), colorSpace='rgb', bold=False, height=2.0*(self.widthPix/1920),
                                anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))
        text_stim.draw()

        image = visual.ImageStim(self.win, image=self.participant_path + "/" + self.categories[n] + ".png", size=(600*(self.widthPix/1920), 337*(self.widthPix/1920)),
                                 units='pix', pos=(0.0, -5.0*(2*self.widthPix/1920)))
        image.draw()

        space = 0

        for i in range(0, j):
            self.button.append(visual.ButtonStim(self.win, text=self.number_button[i], color=[1, 1, 1], colorSpace='rgb',
                                            fillColor=[-0.3, -0.3, -0.3], pos=[-720 + space, -350*(self.widthPix/1920)], size=(100, 100), units='pix'))
            space += 240

        for k in range(0, j):
            self.button[k].draw()

        self.win.flip()


        return


    def category_request(self, n):

        text_stim = visual.TextStim(self.win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 9.0*(self.widthPix/1920)),
                               colorSpace='rgb', bold=False, height=2.0*(self.widthPix/1920), anchorHoriz="center", wrapWidth=500)
        text_stim2 = visual.TextStim(self.win, text=self.categories[n],  color=(1, -0.7, -0.7), pos=(0.0, -1.0*(self.widthPix/1920)),
                                colorSpace='rgb', bold=True, height=3.5*(self.widthPix/1920), anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))
        text_stim.draw()
        text_stim2.draw()
        self.win.flip()

        time.sleep(4)

        return

    def category_trial_request(self):

        text_stim = visual.TextStim(self.win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 9.0*(self.widthPix/1920)),
                               colorSpace='rgb', bold=False, height=2.0*(self.widthPix/1920), anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))
        text_stim2 = visual.TextStim(self.win, text="Scissors",  color=(1, -0.7, -0.7), pos=(0.0, -1.0*(self.widthPix/1920)),
                                colorSpace='rgb', bold=True, height=3.5*(self.widthPix/1920), anchorHoriz="center", wrapWidth=350*(self.widthPix/1920))
        text_stim.draw()
        text_stim2.draw()
        self.win.flip()

        time.sleep(4)

        self.launch_drawing_trial()

        return


    def launch_drawing_trial(self):

        self.win.close()

        if self.output_port.getOutputCount():
            info_out = self.output_port.prepare()
            info_out.clear()
            info_out.addString("start")
        self.output_port.write()

        print("I'VE WRITTEN START ON THE PORT")

        p = subprocess.Popen(["python3", self.drawing_trial_path, str(self.widthPix), str(self.heightPix)])
        p.wait()

        if self.output_port.getOutputCount():
            info_out = self.output_port.prepare()
            info_out.clear()
            info_out.addString("stop")
        self.output_port.write()

        print("I'VE WRITTEN STOP ON THE PORT")

        self.configuration_window()
        return


    def artistic_questions(self):

        self.text_multiple_buttons_screen("How much do you enjoy free-hand drawing? \n (1 - extremely little, 7 - extremely much)", 7)

        touch = False

        while touch == False:
            for k in range(0, 7):
                if self.myMouse.isPressedIn(self.button[k]):
                    self.drawing_enjoyment = k + 1
                    touch = True

        self.button.clear()
        time.sleep(0.5)
        buttons = self.myMouse.getPressed()
        self.myMouse.clickReset(buttons)

        self.blue_window()


        self.text_multiple_buttons_screen("How often do you draw sketches? \n (1 - extremely little, 7 - extremely much)", 7)

        touch = False

        while touch == False:
            for k in range(0, 7):
                if self.myMouse.isPressedIn(self.button[k]):
                    self.drawing_frequency = k + 1
                    touch = True

        self.button.clear()
        time.sleep(0.5)
        buttons = self.myMouse.getPressed()
        self.myMouse.clickReset(buttons)

        self.blue_window()


        self.text_multiple_buttons_screen("Imagine other 100 people drawing the same sketches as yours: \n"
                                     " how many of them do you think will draw better than you? \n "
                                     "(0% - almost no one, 100% - almost everyone)", 10)

        touch = False

        while touch == False:
            for k in range(0, 11):
                if self.myMouse.isPressedIn(self.button[k]):
                    self.drawing_percentage = k*10
                    touch = True

        self.button.clear()
        time.sleep(0.5)
        buttons = self.myMouse.getPressed()
        self.myMouse.clickReset(buttons)

        return


    def drawing_task(self, n):

        self.text_and_button_screen("Are you ready to draw?")
        self.category_request(n)
        self.drawing_activity(n)

        return

    def drawing_activity(self, n):

        self.win.close()
        print("window closed, ready to open drawing")

        if self.output_port.getOutputCount():
            info_out = self.output_port.prepare()
            info_out.clear()
            info_out.addString("start")
        self.output_port.write()

        print("I'VE WRITTEN START ON THE PORT")

        p = subprocess.Popen(["python3", self.drawing_path, self.categories[n], self.participant_path, str(self.widthPix), str(self.heightPix), self.condition, self.country, self.experiment_dir], stdout=subprocess.PIPE)
        p.wait()

        if self.output_port.getOutputCount():
            info_out = self.output_port.prepare()
            info_out.clear()
            info_out.addString("stop")
        self.output_port.write()

        print("I'VE WRITTEN STOP ON THE PORT")

        output = []
        output = p.stdout.read()

        array = np.fromstring(output.decode(), dtype=float, sep=',')

        print(n)

        self.latency_time[n] = array[0]
        self.total_drawing_time[n] = array[1]
        self.number_of_strokes[n] = array[2]

        self.configuration_window()

        self.text_and_button_screen("Now please answer to some questions.")

        self.drawing_questions(n)

        return

    def drawing_questions(self, n):

        self.text_multiple_buttons_screen("How difficult it was to draw the " + self.categories[n] + "? \n"
                            "(1 - not difficult, 7 - extremely difficult)", 7)

        touch = False

        while touch == False:
            for k in range(0, 7):
                if self.myMouse.isPressedIn(self.button[k]):
                    self.difficulty_ranking[n] = k + 1
                    touch = True

        self.button.clear()
        time.sleep(0.5)
        buttons = self.myMouse.getPressed()
        self.myMouse.clickReset(buttons)
        self.blue_window()


        self.text_multiple_buttons_screen("How much did you enjoy drawing the " + self.categories[n] + "? \n"
                            "(1 - not enjoyed, 7 - extremely enjoyed)", 7)

        touch = False

        while touch == False:
            for k in range(0, 7):
                if self.myMouse.isPressedIn(self.button[k]):
                    self.enjoyment_ranking[n] = k + 1
                    touch = True

        self.button.clear()
        time.sleep(0.5)
        buttons = self.myMouse.getPressed()
        self.myMouse.clickReset(buttons)
        self.blue_window()

        self.text_multiple_buttons_and_image_screen("How much do you like your drawing of the " + self.categories[n] + "? \n"
                            "(1 - not liked, 7 - liked a lot)", 7, n)

        touch = False

        while touch == False:
            for k in range(0, 7):
                if self.myMouse.isPressedIn(self.button[k]):
                    self.likeability_ranking[n] = k + 1
                    touch = True

        self.button.clear()
        time.sleep(0.5)
        buttons = self.myMouse.getPressed()
        self.myMouse.clickReset(buttons)

        self.blue_window()

        return

    def save_art(self):

        artistic_data = {
                            'Participant_ID': self.participant_name,
                            'Country': self.country,
                            'Condition': self.condition,
                            'Artistic_enjoyment': self.drawing_enjoyment,
                            'Artistic_frequency': self.drawing_frequency,
                            'Artistic_percentage': self.drawing_percentage,
                            'Average_latency_time': np.mean(self.latency_time),
                            'Average_total_time': np.mean(self.total_drawing_time),
                            'Average_number_strokes': np.mean(self.number_of_strokes),
                            'Average_enjoyment_ranking': np.mean(self.enjoyment_ranking),
                            'Average_difficulty_ranking': np.mean(self.difficulty_ranking),
                            'Average_likeability_ranking': np.mean(self.likeability_ranking)
                        }

        if os.path.isfile(self.artistic_skills_path):
            with open(self.artistic_skills_path) as f:
                data = []
                reader = ndjson.reader(f)
                for i in reader:
                    data.append(i)
            data.append(artistic_data)

            # Writing items to a ndjson file
            with open(self.artistic_skills_path, 'w') as f:
                writer = ndjson.writer(f, ensure_ascii=False)
                for d in data:
                    writer.writerow(d)

        else:
            open(self.code_path, "x")
            with open(self.artistic_skills_path, "w") as file:
                ndjson.dump(artistic_data, file)

        return

    def save_rankings(self, n):

        path_var = self.images_dir+"/"+str(self.categories[n])+"_quantitative_data.ndjson"

        ranking_data = {
            'Participant_ID': self.participant_name,
            'Country': self.country,
            'Condition': self.condition,
            'Latency_time': self.latency_time[n],
            'Total_time': self.total_drawing_time[n],
            'Number_of_Strokes': self.number_of_strokes[n],
            'Enjoyment_ranking': self.enjoyment_ranking[n],
            'Difficulty_ranking': self.difficulty_ranking[n],
            'Likeability_ranking': self.likeability_ranking[n]
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
                ndjson.dump(ranking_data, file)
        return

if __name__ == '__main__':

    # Initialise YARP
    if not yarp.Network.checkNetwork():
        info("Unable to find a yarp server exiting ...")
        sys.exit(1)

    yarp.Network.init()

    sdt = socialDrawingTask()

    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('socialDrawingTask')
    rf.setDefaultConfigFile('socialDrawingTask.ini')

    if rf.configure(sys.argv):
        sdt.runModule(rf)

    sdt.close()
    sys.exit()
