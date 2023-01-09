#!/usr/bin/env python3
# region Imports
from datetime import datetime
from genericpath import exists
import sys
import simpleaudio as sa
from PyQt6.QtCore import Qt, QTimer, QObject
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QMainWindow,
)
from PyQt6.QtGui import QIcon, QFont
import os
import json

# endregion Imports
# region Variables
##### Variables #####
Schedule_Type = ""  # The Type of schedule
current_elapsed_time = 0  # How long has the current acitvity been going on for
current_remaining_time = 0  # How long left in the current acitvity
seconds_today = 0
current_step = 0
total_steps = 0
current_category = ""
begin_time = 0
next_time = 0
# toggles
toggle_color = False
toggle_mute = False
# Directories
directory_path = os.path.dirname(os.path.realpath(__file__))
path_to_Work = directory_path + "/Data/Work.json"
path_to_School = directory_path + "/Data/School.json"
path_to_Hobby = directory_path + "/Data/Hobby.json"
path_to_Lesiure = directory_path + "/Data/Lesiure.json"
path_to_Vacation = directory_path + "/Data/Vacation.json"
path_to_Sick = directory_path + "/Data/Sick.json"
path_to_Work_p0Schoolp0 = directory_path + "/Data/Work_p0Schoolp0.json"
path_to_Hobby_p0Schoolp0 = directory_path + "/Data/Hobby_p0Schoolp0.json"
path_to_Leisure_p0Schoolp0 = directory_path + "/Data/Leisure_p0Schoolp0.json"
path_to_Work_a0_School = directory_path + "/Data/Work_a0_School.json"
path_to_Hobby_a0_Leisure = directory_path + "/Data/Hobby_a0_Leisure.json"
path_to_icon = directory_path + "/Data/icon.ico"
path_to_chime = directory_path + "/Data/Chime.wav"  # Need to make a custom sound
path_to_save = directory_path + "/Export/"
path_to_save_file = directory_path + "/Export/Save_Data.json"
# Audio Clips
chime_sound = sa.WaveObject.from_wave_file(path_to_chime)
# Data
schedule_data = {}  # For holding schedule information
elapsed_schedule = {
    "Work": 0,
    "Education": 0,
    "Hobby": 0,
    "Essential": 0,
    "Productive": 0,
    "Lesiure": 0,
    "Social": 0,
    "Nothing": 0,
}  # For holding the information about the elapsed time
total_schedule = {
    "Work": 0,
    "Education": 0,
    "Hobby": 0,
    "Essential": 0,
    "Productive": 0,
    "Lesiure": 0,
    "Social": 0,
    "Nothing": 0,
}  # For holding the totals from the schedule
remaining_schedule = {
    "Work": 0,
    "Education": 0,
    "Hobby": 0,
    "Essential": 0,
    "Productive": 0,
    "Lesiure": 0,
    "Social": 0,
    "Nothing": 0,
}  # For holding the remaining time from the schedule
General_Font = QFont("Times", 12)
# endregion Variables

# Class for the Starting Window
class Opening_Window(QWidget):
    # Init Function
    def __init__(self):
        super().__init__()
        # region GUI Items
        self.Main_Label = QLabel("<h1>Select Schedule</h1>", parent=self)
        self.Category_Label = QLabel("Schedule:", parent=self)
        self.Schedule_Combo = QComboBox(parent=self)
        self.Schedule_Combo.addItems(
            [
                "Work",
                "School",
                "Hobby",
                "Lesiure",
                "Vacation",
                "Sick",
                "Work (School)",
                "Hobby (School)",
                "Leisure (School)",
                "Work & School",
                "Hobby & Leisure",
            ]
        )
        self.Start_Button = QPushButton("Start", parent=self)
        # Setting up the layout
        Open_Layout = QGridLayout()
        self.Main_Label.setMinimumSize(100, 0)
        self.Main_Label.setFont(General_Font)
        Open_Layout.addWidget(
            self.Main_Label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Category_Label.setMinimumSize(0, 0)
        self.Category_Label.setFont(General_Font)
        Open_Layout.addWidget(
            self.Category_Label, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Schedule_Combo.setMinimumSize(0, 0)
        self.Schedule_Combo.setFont(General_Font)
        Open_Layout.addWidget(
            self.Schedule_Combo, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Start_Button.setMinimumSize(250, 0)
        self.Start_Button.setFont(General_Font)
        Open_Layout.addWidget(
            self.Start_Button, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # Setting up window
        self.setWindowIcon(QIcon(path_to_icon))
        self.setWindowTitle("Schedule Alerts")
        self.setLayout(Open_Layout)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())
        # endregion GUI Items
        # Button Event
        self.Start_Button.clicked.connect(self.Open_Schedule)

    # Opening the Main Schedule Window
    def Open_Schedule(self):
        # Getting the schedule type
        global Schedule_Type
        Schedule_Type = self.Schedule_Combo.currentText()
        # Making and showing a new window
        self.w = MainWindow()
        self.w.show()
        # Closing the current window
        self.close()


# Class for the Main Window
class MainWindow(QMainWindow):
    # Init Function
    def __init__(self):
        super().__init__()
        # region GUI Items
        # Setting up application and window
        self.setWindowTitle("Schedule Alerts")
        # Setting up a label and button
        self.Schedule_Label = QLabel(f"<h1>{Schedule_Type}</h1>", parent=self)
        self.Schedule_Label.setMinimumSize(0, 0)
        self.Schedule_Label.setFont(General_Font)
        self.Current_Category_Text_Label = QLabel("Current Category:", parent=self)
        self.Current_Category_Text_Label.setMinimumSize(0, 0)
        self.Current_Category_Text_Label.setFont(General_Font)
        self.Current_Category_Label = QLabel("Category", parent=self)
        self.Current_Category_Label.setMinimumSize(0, 0)
        self.Current_Category_Label.setFont(General_Font)
        self.Current_Activity_Text_Label = QLabel("Current Activity:", parent=self)
        self.Current_Activity_Text_Label.setMinimumSize(0, 0)
        self.Current_Activity_Text_Label.setFont(General_Font)
        self.Current_Activity_Label = QLabel("Activity", parent=self)
        self.Current_Activity_Label.setMinimumSize(0, 0)
        self.Current_Activity_Label.setFont(General_Font)
        self.Current_Step_Text_Label = QLabel("Current Step:", parent=self)
        self.Current_Step_Text_Label.setMinimumSize(0, 0)
        self.Current_Step_Text_Label.setFont(General_Font)
        self.Current_Step_Label = QLabel("Curent Step", parent=self)
        self.Current_Step_Label.setMinimumSize(0, 0)
        self.Current_Step_Label.setFont(General_Font)
        self.Next_Category_Text_Label = QLabel("Next Category:", parent=self)
        self.Next_Category_Text_Label.setMinimumSize(0, 0)
        self.Next_Category_Text_Label.setFont(General_Font)
        self.Next_Category_Label = QLabel("Next Category", parent=self)
        self.Next_Category_Label.setMinimumSize(0, 0)
        self.Next_Category_Label.setFont(General_Font)
        self.Elapsed_Time_Text_Label = QLabel("Elapsed Time:", parent=self)
        self.Elapsed_Time_Text_Label.setMinimumSize(0, 0)
        self.Elapsed_Time_Text_Label.setFont(General_Font)
        self.Elapsed_Time_Label = QLabel("Elapsed Time", parent=self)
        self.Elapsed_Time_Label.setMinimumSize(0, 0)
        self.Elapsed_Time_Label.setFont(General_Font)
        self.Remaining_Time_Text_Label = QLabel("Remaining Time:", parent=self)
        self.Remaining_Time_Text_Label.setMinimumSize(0, 0)
        self.Remaining_Time_Text_Label.setFont(General_Font)
        self.Remaining_Time_Label = QLabel("Remaining Time", parent=self)
        self.Remaining_Time_Label.setMinimumSize(0, 0)
        self.Remaining_Time_Label.setFont(General_Font)
        self.Total_Steps_Text_Label = QLabel("Total Steps:", parent=self)
        self.Total_Steps_Text_Label.setMinimumSize(0, 0)
        self.Total_Steps_Text_Label.setFont(General_Font)
        self.Total_Steps_Label = QLabel("Total Steps", parent=self)
        self.Total_Steps_Label.setMinimumSize(0, 0)
        self.Total_Steps_Label.setFont(General_Font)
        self.Next_Activity_Text_Label = QLabel("Next Activity:", parent=self)
        self.Next_Activity_Text_Label.setMinimumSize(0, 0)
        self.Next_Activity_Text_Label.setFont(General_Font)
        self.Next_Activity_Label = QLabel("Next", parent=self)
        self.Next_Activity_Label.setMinimumSize(0, 0)
        self.Next_Activity_Label.setFont(General_Font)
        self.Stop_Button = QPushButton("Stop", parent=self)
        self.Stop_Button.setMinimumSize(100, 0)
        self.Stop_Button.setFont(General_Font)
        self.Statistics_Button = QPushButton("Statistics", parent=self)
        self.Statistics_Button.setMinimumSize(100, 0)
        self.Statistics_Button.setFont(General_Font)
        self.Options_Button = QPushButton("Options", parent=self)
        self.Options_Button.setMinimumSize(100, 0)
        self.Options_Button.setFont(General_Font)
        self.Schedule_Button = QPushButton("Schedule", parent=self)
        self.Schedule_Button.setMinimumSize(100, 0)
        self.Schedule_Button.setFont(General_Font)
        # Laying it all out
        self.layout = QGridLayout()
        self.layout.addWidget(
            self.Schedule_Label, 0, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Current_Category_Text_Label,
            1,
            0,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(
            self.Current_Category_Label, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Remaining_Time_Text_Label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Remaining_Time_Label, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Next_Category_Text_Label, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Next_Category_Label, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Current_Step_Text_Label, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Current_Step_Label, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Current_Activity_Text_Label,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(
            self.Current_Activity_Label, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Elapsed_Time_Text_Label, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Elapsed_Time_Label, 2, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Next_Activity_Text_Label, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Next_Activity_Label, 3, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Total_Steps_Text_Label, 4, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Total_Steps_Label, 4, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Schedule_Button, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Statistics_Button, 5, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Options_Button, 5, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addWidget(
            self.Stop_Button, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # Finalizing Window Parameters
        self.setWindowIcon(QIcon(path_to_icon))
        self.main_window = QWidget()
        self.main_window.setLayout(self.layout)
        self.setCentralWidget(self.main_window)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())
        # endregion GUI Items
        # Button Events
        self.Stop_Button.clicked.connect(self.Open_Stop)
        self.Statistics_Button.clicked.connect(self.Open_Statistics)
        self.Options_Button.clicked.connect(self.Open_Options)
        self.Schedule_Button.clicked.connect(self.Open_Schedule)
        # Setting up the timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.Timing)
        # Doing an initial clear
        self.Start_Schedule()

    # Starting Schedule
    def Start_Schedule(self):
        # Initializing Everything
        self.Reset(False)
        # Self Data
        global schedule_data
        schedule_data = self.Format_Schedule()
        # Start the timer
        self.timer.start(1000)

    # Formating the schedule from the raw JSON file
    def Format_Schedule(self):
        # Getting schedule from JSON in a dictionary
        self.unformatted = self.Load_Schedule()
        # Variables (Seconds)
        self.total_work = 0
        self.total_education = 0
        self.total_hobby = 0
        self.total_essential = 0
        self.total_productive = 0
        self.total_leisure = 0
        self.total_social = 0
        self.total_nothing = 0
        # Dictionary for formatted result
        self.formatted = {}
        # Get information from each part of the schedule
        for x in self.unformatted:
            # Loading Data
            self.load_step = int(x)
            self.load_category = self.unformatted[x]["Category"]
            self.load_activity = self.unformatted[x]["Activity"]
            self.load_duration = (
                int(self.unformatted[x]["Duration"]) * 60
            )  # Multiply by 60 because we need the time in seconds and the schedule is in minutes because I'm a person not a computer
            self.load_start = int(self.unformatted[x]["Start"]) * 60  # Get seconds
            self.load_end = int(self.unformatted[x]["End"]) * 60  # Get seconds
            # Getting category times
            if self.load_category == "Work":
                self.total_work += self.load_duration
            elif self.load_category == "Education":
                self.total_education += self.load_duration
            elif self.load_category == "Hobby":
                self.total_hobby += self.load_duration
            elif self.load_category == "Essential":
                self.total_essential += self.load_duration
            elif self.load_category == "Productive":
                self.total_productive += self.load_duration
            elif self.load_category == "Leisure":
                self.total_leisure += self.load_duration
            elif self.load_category == "Social":
                self.total_social += self.load_duration
            elif self.load_category == "Nothing":
                self.total_nothing += self.load_duration
            # Write to dictionary
            self.formatted[self.load_step] = {
                "Category": self.load_category,
                "Activity": self.load_activity,
                "Duration": self.load_duration,
                "Start": self.load_start,
                "End": self.load_end,
            }
        # Saving the total times to a global dictionary
        global total_schedule
        total_schedule["Work"] = self.total_work
        total_schedule["Education"] = self.total_education
        total_schedule["Hobby"] = self.total_hobby
        total_schedule["Essential"] = self.total_essential
        total_schedule["Productive"] = self.total_productive
        total_schedule["Lesiure"] = self.total_leisure
        total_schedule["Social"] = self.total_social
        total_schedule["Nothing"] = self.total_nothing
        # Copying over the total times to begin the remaining
        global remaining_schedule
        remaining_schedule = total_schedule.copy()
        # Saving variables
        global total_steps
        total_steps = len(self.formatted)
        # Returning schedule results
        return self.formatted

    # Loading the schedule from JSON files
    def Load_Schedule(self):
        self.path_to_use = ""
        # Getting path from Schedule Type
        if Schedule_Type == "Work":
            self.path_to_use = path_to_Work
        elif Schedule_Type == "School":
            self.path_to_use = path_to_School
        elif Schedule_Type == "Hobby":
            self.path_to_use = path_to_Hobby
        elif Schedule_Type == "Lesiure":
            self.path_to_use = path_to_Lesiure
        elif Schedule_Type == "Vacation":
            self.path_to_use = path_to_Vacation
        elif Schedule_Type == "Sick":
            self.path_to_use = path_to_Sick
        elif Schedule_Type == "Work (School)":
            self.path_to_use = path_to_Work_p0Schoolp0
        elif Schedule_Type == "Hobby (School)":
            self.path_to_use = path_to_Hobby_p0Schoolp0
        elif Schedule_Type == "Leisure (School)":
            self.path_to_use = path_to_Leisure_p0Schoolp0
        elif Schedule_Type == "Work & School":
            self.path_to_use = path_to_Work_a0_School
        elif Schedule_Type == "Hobby & Leisure":
            self.path_to_use = path_to_Hobby_a0_Leisure
        # Loading the schedule
        with open(self.path_to_use) as temp_file:
            self.loaded_time = json.load(temp_file)
        return self.loaded_time

    # Main Timer Logic
    def Timing(self):
        self.Check_Time()

    ### Checking Time ###
    def Check_Time(self):
        # Global vairablse
        global current_step
        # Getting time in seconds from midnight
        global seconds_today
        # Times for tracking
        global current_elapsed_time
        global current_remaining_time
        # Getting current step and time initiallty
        if current_step == 0:
            # Getting actual time initially
            seconds_today = self.get_time()
            # Getting initial step based on the time
            current_step = self.get_step(seconds_today)
            # Getting the next time
            self.get_next_time()
            # Updating labels
            self.update_long_labels()
        elif current_step > 0 and current_step < total_steps:
            if seconds_today >= next_time:
                self.advance_step()
        elif current_step == total_steps:
            if seconds_today >= next_time:
                self.Stop_Schedule()  # Stopping when day ends
        # Math to find elapsed and remainting time per activity
        current_elapsed_time = seconds_today - begin_time
        current_remaining_time = next_time - seconds_today
        # Advancing time
        seconds_today += 1
        self.save_to_elapsed(current_category, 1)
        self.save_to_remaining(current_category, 1)
        # Updating short labels
        self.update_short_labels()

    # Getting current time
    def get_time(self):
        # Getting current time
        self.now = datetime.now()
        # Getting time at midnight
        self.midnight = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        # Getting seconds today
        self.seconds_today = (self.now - self.midnight).seconds
        return self.seconds_today

    # Getting initial step
    def get_step(self, time):
        # Iterating through the schedule to find the right activity for the time
        for x in schedule_data:
            # Getting the start and end time
            self.start_time = schedule_data[x]["Start"]
            self.end_time = schedule_data[x]["End"]
            self.schedule_category = schedule_data[x]["Category"]
            # Returning when the current time falls between the start and end times
            if time >= self.start_time and time <= self.end_time:
                # Getting the amount of passed time from the current activity
                self.schedule_duration = time - self.start_time
                self.save_to_elapsed(self.schedule_category, self.schedule_duration)
                self.save_to_remaining(self.schedule_category, self.schedule_duration)
                # Returning the step
                return x
            else:
                # Adding the elapsed time to the elapsed dictionary
                self.schedule_duration = schedule_data[x]["Duration"]
                self.save_to_elapsed(self.schedule_category, self.schedule_duration)
                self.save_to_remaining(self.schedule_category, self.schedule_duration)

    # Save to elapsed dictionary
    def save_to_elapsed(self, Elapsed_Category, Elapsed_Time):
        # Global Dictionary
        global elapsed_schedule
        # Math to put in the right category
        if Elapsed_Category == "Work":
            elapsed_schedule["Work"] += Elapsed_Time
        elif Elapsed_Category == "Education":
            elapsed_schedule["Education"] += Elapsed_Time
        elif Elapsed_Category == "Hobby":
            elapsed_schedule["Hobby"] += Elapsed_Time
        elif Elapsed_Category == "Essential":
            elapsed_schedule["Essential"] += Elapsed_Time
        elif Elapsed_Category == "Productive":
            elapsed_schedule["Productive"] += Elapsed_Time
        elif Elapsed_Category == "Leisure":
            elapsed_schedule["Lesiure"] += Elapsed_Time
        elif Elapsed_Category == "Social":
            elapsed_schedule["Social"] += Elapsed_Time
        elif Elapsed_Category == "Nothing":
            elapsed_schedule["Nothing"] += Elapsed_Time

    # Save to the remaining dictionary
    def save_to_remaining(self, Elapsed_Category, Elapsed_Time):
        # Global Dictionary
        global remaining_schedule
        # Math to put it in the right category
        if Elapsed_Category == "Work":
            remaining_schedule["Work"] -= Elapsed_Time
        elif Elapsed_Category == "Education":
            remaining_schedule["Education"] -= Elapsed_Time
        elif Elapsed_Category == "Hobby":
            remaining_schedule["Hobby"] -= Elapsed_Time
        elif Elapsed_Category == "Essential":
            remaining_schedule["Essential"] -= Elapsed_Time
        elif Elapsed_Category == "Productive":
            remaining_schedule["Productive"] -= Elapsed_Time
        elif Elapsed_Category == "Leisure":
            remaining_schedule["Lesiure"] -= Elapsed_Time
        elif Elapsed_Category == "Social":
            remaining_schedule["Social"] -= Elapsed_Time
        elif Elapsed_Category == "Nothing":
            remaining_schedule["Nothing"] -= Elapsed_Time

    # Getting the next time
    def get_next_time(self):
        # Global variable
        global next_time
        global begin_time
        global current_category
        # Getting the next time
        next_time = schedule_data[current_step]["End"]
        begin_time = schedule_data[current_step]["Start"]
        # Getting the next category
        current_category = schedule_data[current_step]["Category"]
        # Play chime
        if toggle_mute == False:
            self.Play_Chime()
        # Change color
        if toggle_color == False:
            self.Change_Color(False)

    # Updating labels that stay unchanged for long periods of time
    def update_long_labels(self):
        self.Current_Category_Label.setText(current_category)
        self.Current_Activity_Label.setText(schedule_data[current_step]["Activity"])
        self.Current_Step_Label.setText(str(current_step))
        self.Total_Steps_Label.setText(str(total_steps))
        if current_step < total_steps:
            self.Next_Category_Label.setText(
                schedule_data[current_step + 1]["Category"]
            )
            self.Next_Activity_Label.setText(
                schedule_data[current_step + 1]["Activity"]
            )
        else:
            self.Next_Category_Label.setText("End")
            self.Next_Activity_Label.setText("End")

    # Advancing to the next step
    def advance_step(self):
        # Global variables
        global current_step
        # Advancing the step
        current_step += 1
        # Getting the new next time
        self.get_next_time()
        # Updating long labels
        self.update_long_labels()

    # Play chime, possibly could have more types in the future for each category
    def Play_Chime(self):
        if current_category == "Work":
            chime_sound.play()
        elif current_category == "Education":
            chime_sound.play()
        elif current_category == "Hobby":
            chime_sound.play()
        elif current_category == "Essential":
            chime_sound.play()
        elif current_category == "Productive":
            chime_sound.play()
        elif current_category == "Leisure":
            chime_sound.play()
        elif current_category == "Social":
            chime_sound.play()
        elif current_category == "Nothing":
            chime_sound.play()

    # Change the color of the window
    def Change_Color(self, clearing):
        if clearing == False:
            if current_category == "Work":
                self.current_color = "lightgreen"
            elif current_category == "Education":
                self.current_color = "lightskyblue"
            elif current_category == "Hobby":
                self.current_color = "paleturquoise"
            elif current_category == "Essential":
                self.current_color = "peachpuff"
            elif current_category == "Productive":
                self.current_color = "lemonchiffon"
            elif current_category == "Leisure":
                self.current_color = "plum"
            elif current_category == "Social":
                self.current_color = "lightsalmon"
            elif current_category == "Nothing":
                self.current_color = "lightcoral"
        else:
            self.current_color = " "
        self.main_window.setStyleSheet(f"background-color: {self.current_color}")

    # Stopping Schedule
    def Stop_Schedule(self):
        # Stop the timer
        self.timer.stop()
        # Initializing Everything
        self.Reset(True)
        # Open a new opening window
        self.w = Opening_Window()
        self.w.show()
        # Closing main window
        self.close()

    # Resets Everything
    def Reset(self, Clear_Type):
        # Setting text
        self.Current_Category_Label.setText("Not Started")
        self.Current_Activity_Label.setText("Not Started")
        self.Current_Step_Label.setText("Not Started")
        self.Next_Category_Label.setText("Not Started")
        self.Elapsed_Time_Label.setText("Not Started")
        self.Remaining_Time_Label.setText("Not Started")
        self.Total_Steps_Label.setText("Not Started")
        self.Next_Activity_Label.setText("Not Started")
        # Resetting variables
        if Clear_Type == True:
            # If stopping the schedule clear the schedule type
            global Schedule_Type
            Schedule_Type = ""
        global schedule_data
        schedule_data = {}
        global elapsed_schedule
        elapsed_schedule = {
            "Work": 0,
            "Education": 0,
            "Hobby": 0,
            "Essential": 0,
            "Productive": 0,
            "Lesiure": 0,
            "Social": 0,
            "Nothing": 0,
        }
        global total_schedule
        total_schedule = {
            "Work": 0,
            "Education": 0,
            "Hobby": 0,
            "Essential": 0,
            "Productive": 0,
            "Lesiure": 0,
            "Social": 0,
            "Nothing": 0,
        }
        global remaining_schedule
        remaining_schedule = {
            "Work": 0,
            "Education": 0,
            "Hobby": 0,
            "Essential": 0,
            "Productive": 0,
            "Lesiure": 0,
            "Social": 0,
            "Nothing": 0,
        }
        global seconds_today
        seconds_today = 0
        global current_step
        current_step = 0
        global total_steps
        total_steps = 0
        global current_category
        current_category = ""
        global next_time
        next_time = 0
        global begin_time
        begin_time = 0

    # Updating labels that change often
    def update_short_labels(self):
        # Changing times to time format
        display_elapsed = datetime.utcfromtimestamp(current_elapsed_time).strftime(
            "%H:%M:%S"
        )
        display_remaining = datetime.utcfromtimestamp(current_remaining_time).strftime(
            "%H:%M:%S"
        )
        # Changing labels
        self.Elapsed_Time_Label.setText(display_elapsed)
        self.Remaining_Time_Label.setText(display_remaining)

    # Button Functions

    def Open_Statistics(self):
        # Making and showing a new window. Sending over the timer as well so that it's synchronized.
        self.w = Statistics_View(self.timer)
        self.w.show()

    def Open_Options(self):
        # Making and showing a new window. Send over this main window as well
        self.w = Options_Window(self)
        self.w.show()

    def Open_Stop(self):
        # Making and showing a new window. Send over this main window with it so that it can send back calls
        self.w = Stop_Window(self)
        self.w.show()

    def Open_Schedule(self):
        # Making and showing a new window
        self.w = Schedule_View()
        self.w.show()


# Class for the Schedule View
class Schedule_View(QWidget):
    # Init Function
    def __init__(self):
        super().__init__()
        # region GUI Items
        self.Main_Label = QLabel(f"<h1>{Schedule_Type} Schedule</h1>", parent=self)
        # Setting up Table
        self.schedule_table = QTableWidget()
        self.schedule_table.setRowCount(len(schedule_data))
        self.schedule_table.setColumnCount(6)
        self.schedule_table.setHorizontalHeaderLabels(
            ["Step", "Category", "Activity", "Duration", "Start", "End"]
        )
        self.schedule_table.setEditTriggers(
            QTableWidget.EditTrigger(0)
        )  # Disables editing
        # Writing labels for each schedule entry
        for x in schedule_data:
            self.step_text = QTableWidgetItem(str(x))
            self.category_text = QTableWidgetItem(schedule_data[x]["Category"])
            self.activity_text = QTableWidgetItem(str(schedule_data[x]["Activity"]))
            self.duration_text = QTableWidgetItem(
                datetime.utcfromtimestamp(schedule_data[x]["Duration"]).strftime(
                    "%H:%M:%S"
                )
            )
            self.start_text = QTableWidgetItem(
                datetime.utcfromtimestamp(schedule_data[x]["Start"]).strftime(
                    "%H:%M:%S"
                )
            )
            self.end_text = QTableWidgetItem(
                datetime.utcfromtimestamp(schedule_data[x]["End"]).strftime("%H:%M:%S")
            )
            self.schedule_table.setItem(x - 1, 0, self.step_text)
            self.schedule_table.setItem(x - 1, 1, self.category_text)
            self.schedule_table.setItem(x - 1, 2, self.activity_text)
            self.schedule_table.setItem(x - 1, 3, self.duration_text)
            self.schedule_table.setItem(x - 1, 4, self.start_text)
            self.schedule_table.setItem(x - 1, 5, self.end_text)
        # Setting up the layout
        self.Schedule_Layout = QGridLayout()
        self.Main_Label.setMinimumSize(100, 0)
        self.Main_Label.setFont(General_Font)
        self.Schedule_Layout.addWidget(
            self.Main_Label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.schedule_table.setColumnWidth(0, 25)
        self.schedule_table.setColumnWidth(1, 85)
        self.schedule_table.setColumnWidth(2, 275)
        self.schedule_table.setColumnWidth(3, 75)
        self.schedule_table.setColumnWidth(4, 75)
        self.schedule_table.setColumnWidth(5, 75)
        self.schedule_table.setMinimumSize(665, 400)
        self.schedule_table.setFont(General_Font)
        self.Schedule_Layout.addWidget(
            self.schedule_table, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # endregion GUI Items
        # Setting up window
        self.setWindowIcon(QIcon(path_to_icon))
        self.setWindowTitle("Schedule")
        self.setLayout(self.Schedule_Layout)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())


# Class for the Statistics View
class Statistics_View(QWidget):
    # Init Function
    def __init__(self, main_timer):
        super().__init__()
        # region GUI Items
        self.Main_Label = QLabel(f"<h1>{Schedule_Type} Statitsics</h1>", parent=self)
        # Setting up Table
        self.statistics_table = QTableWidget()
        self.statistics_table.setRowCount(len(elapsed_schedule))
        self.statistics_table.setColumnCount(4)
        self.statistics_table.setHorizontalHeaderLabels(
            ["Category", "Elapsed", "Remaining", "Total"]
        )
        self.statistics_table.setEditTriggers(
            QTableWidget.EditTrigger(0)
        )  # Disables editing
        for x in elapsed_schedule:
            self.index_position = list(elapsed_schedule.keys()).index(x)
            self.category = QTableWidgetItem(str(x))
            self.elapsed_time = QTableWidgetItem(
                datetime.utcfromtimestamp(elapsed_schedule[x]).strftime("%H:%M:%S")
            )
            self.remaining_time = QTableWidgetItem(
                datetime.utcfromtimestamp(remaining_schedule[x]).strftime("%H:%M:%S")
            )
            self.total_time = QTableWidgetItem(
                datetime.utcfromtimestamp(total_schedule[x]).strftime("%H:%M:%S")
            )
            self.statistics_table.setItem(self.index_position, 0, self.category)
            self.statistics_table.setItem(self.index_position, 1, self.elapsed_time)
            self.statistics_table.setItem(self.index_position, 2, self.remaining_time)
            self.statistics_table.setItem(self.index_position, 3, self.total_time)
        # Setting up the layout
        self.Statistics_Layout = QGridLayout()
        self.Main_Label.setMinimumSize(100, 0)
        self.Main_Label.setFont(General_Font)
        self.Statistics_Layout.addWidget(
            self.Main_Label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.statistics_table.setColumnWidth(0, 90)
        self.statistics_table.setColumnWidth(1, 90)
        self.statistics_table.setColumnWidth(2, 90)
        self.statistics_table.setColumnWidth(3, 90)
        self.statistics_table.setMinimumSize(380, 270)
        self.statistics_table.setFont(General_Font)
        self.Statistics_Layout.addWidget(
            self.statistics_table, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # endregion GUI Items
        # Setting up window
        self.setWindowIcon(QIcon(path_to_icon))
        self.setWindowTitle("Schedule")
        self.setLayout(self.Statistics_Layout)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())
        # Setting up a timer event based off of main timer
        main_timer.timeout.connect(self.Timing)

    # Timing Logic
    def Timing(self):
        # Updating table entries
        for x in elapsed_schedule:
            self.index_position = list(elapsed_schedule.keys()).index(x)
            self.category = QTableWidgetItem(str(x))
            self.elapsed_time = QTableWidgetItem(
                datetime.utcfromtimestamp(elapsed_schedule[x]).strftime("%H:%M:%S")
            )
            self.remaining_time = QTableWidgetItem(
                datetime.utcfromtimestamp(remaining_schedule[x]).strftime("%H:%M:%S")
            )
            self.total_time = QTableWidgetItem(
                datetime.utcfromtimestamp(total_schedule[x]).strftime("%H:%M:%S")
            )
            self.statistics_table.setItem(self.index_position, 0, self.category)
            self.statistics_table.setItem(self.index_position, 1, self.elapsed_time)
            self.statistics_table.setItem(self.index_position, 2, self.remaining_time)
            self.statistics_table.setItem(self.index_position, 3, self.total_time)


# Class for the Stopping Prompt
class Stop_Window(QWidget):
    # Init Function with the main window being carried over
    def __init__(self, main_window):
        super().__init__()
        # region GUI Items
        self.Main_Label = QLabel(
            "This will stop the schedule. Are you sure?", parent=self
        )
        self.Yes_Button = QPushButton("Yes", parent=self)
        self.No_Button = QPushButton("No", parent=self)
        # Setting up the layout
        self.Options_Layout = QGridLayout()
        self.Main_Label.setMinimumSize(150, 0)
        self.Main_Label.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Main_Label, 0, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Yes_Button.setMinimumSize(100, 0)
        self.Yes_Button.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Yes_Button, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.No_Button.setMinimumSize(100, 0)
        self.No_Button.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.No_Button, 1, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # Setting up window
        self.setWindowIcon(QIcon(path_to_icon))
        self.setWindowTitle("Confirmation")
        self.setLayout(self.Options_Layout)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())
        # endregion GUI Items
        # Button Events. Have to use lambda to pass arguments through the connect
        self.Yes_Button.clicked.connect(lambda: self.User_Answer("Yes", main_window))
        self.No_Button.clicked.connect(lambda: self.User_Answer("No", main_window))

    # Return answer to main window
    def User_Answer(self, result, main_window):
        # If yes stop the main window
        if result == "Yes":
            main_window.Stop_Schedule()
        # Close this window
        self.close()


# Class for the Options Prompt
class Options_Window(QWidget):
    # Init Function with the main window attached
    def __init__(self, main_window):
        super().__init__()
        # region GUI Items
        self.Main_Label = QLabel("<h1>Options</h1>", parent=self)
        self.Mute_Label = QLabel("Mute:", parent=self)
        self.Color_Label = QLabel("Colors:", parent=self)
        self.Mute_Button = QPushButton("Mute", parent=self)
        self.Color_Button = QPushButton("Color", parent=self)
        # Setting up the layout
        self.Options_Layout = QGridLayout()
        self.Main_Label.setMinimumSize(100, 0)
        self.Main_Label.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Main_Label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Mute_Label.setMinimumSize(100, 0)
        self.Mute_Label.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Mute_Label, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Mute_Button.setMinimumSize(100, 0)
        self.Mute_Button.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Mute_Button, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Color_Label.setMinimumSize(100, 0)
        self.Color_Label.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Color_Label, 2, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.Color_Button.setMinimumSize(100, 0)
        self.Color_Button.setFont(General_Font)
        self.Options_Layout.addWidget(
            self.Color_Button, 2, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # Changing button text depending on the variable
        if toggle_mute == False:
            self.Mute_Button.setText("Mute")
        else:
            self.Mute_Button.setText("Un-Mute")
        if toggle_color == False:
            self.Color_Button.setText("Color")
        else:
            self.Color_Button.setText("No Color")
        # Setting up window
        self.setWindowIcon(QIcon(path_to_icon))
        self.setWindowTitle("Schedule Alerts")
        self.setLayout(self.Options_Layout)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())
        # endregion GUI Items
        # Button Events
        self.Mute_Button.clicked.connect(self.Toggle_Mute)
        # Running the input though lambda because you can't pass argument through connect or something
        self.Color_Button.clicked.connect(lambda: self.Toggle_Color(main_window))

    # Toggling Mute of the chime
    def Toggle_Mute(self):
        global toggle_mute
        if toggle_mute == False:
            toggle_mute = True
            self.Mute_Button.setText("Un-Mute")
        else:
            toggle_mute = False
            self.Mute_Button.setText("Mute")

    # Toggling Mute of the color (with the main window carried over)
    def Toggle_Color(self, main_window):
        global toggle_color
        if toggle_color == False:
            toggle_color = True
            self.Color_Button.setText("No Color")
            # Running the function in the main window
            main_window.Change_Color(True)
        else:
            toggle_color = False
            self.Color_Button.setText("Color")
            # Running the function in the main window
            main_window.Change_Color(False)


# Starting Program
app = QApplication([])
w = Opening_Window()
w.show()
sys.exit(app.exec())
