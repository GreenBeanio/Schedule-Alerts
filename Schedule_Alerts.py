#!/usr/bin/env python3
# region Imports
from datetime import datetime
from genericpath import exists
import sys
import simpleaudio as sa
from PyQt6.QtCore import Qt, QTimer
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
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
import os
import json

# endregion
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
# endregion


# region Main GUI Setup


class MainWindow(QMainWindow):
    # Setting up
    def __init__(self):
        super().__init__()
        # Setting up application and window
        self.setWindowTitle("Schedule Alerts")
        # Setting up a label and button
        self.Pomodoro_Label = QLabel("<h1>Schedule</h1>", parent=self)  # Static

        self.Current_Category_Text_Label = QLabel(
            "Current Category:", parent=self
        )  # Static
        self.Current_Category_Label = QLabel("Category", parent=self)  # Dynamic
        self.Current_Activity_Text_Label = QLabel(
            "Current Activity:", parent=self
        )  # Static
        self.Current_Activity_Label = QLabel("Activity", parent=self)  # Dynamic
        self.Current_Step_Text_Label = QLabel("Current Step:", parent=self)  # Static
        self.Current_Step_Label = QLabel("Curent Step", parent=self)  # Dynamic
        self.Next_Category_Text_Label = QLabel("Next Category:", parent=self)  # Static
        self.Next_Category_Label = QLabel("Next Category", parent=self)  # Dynamic
        self.Elapsed_Time_Text_Label = QLabel("Elapsed Time:", parent=self)  # Static
        self.Elapsed_Time_Label = QLabel("Elapsed Time", parent=self)  # Dynamic
        self.Remaining_Time_Text_Label = QLabel(
            "Remaining Time:", parent=self
        )  # Static
        self.Remaining_Time_Label = QLabel("Remaining Time", parent=self)  # Dynamic
        self.Total_Steps_Text_Label = QLabel("Total Steps:", parent=self)  # Static
        self.Total_Steps_Label = QLabel("Total Steps", parent=self)  # Dynamic
        self.Next_Activity_Text_Label = QLabel("Next Activity:", parent=self)  # Static
        self.Next_Activity_Label = QLabel("Next", parent=self)  # Dynamic
        self.Stop_Button = QPushButton("Stop", parent=self)  # Static
        self.Statistics_Button = QPushButton("Statistics", parent=self)  # Static
        self.Options_Button = QPushButton("Options", parent=self)  # Static
        self.Schedule_Button = QPushButton("Schedule", parent=self)  # Static
        self.Schedule_Combo = QComboBox(parent=self)  # Static
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
        self.Schedule_Combo.setCurrentIndex(0)

        # Temporary Button
        Start_Button = QPushButton("Start", parent=self)  # Static

        # Laying it all out
        layout = QGridLayout()
        # Temprary location
        layout.addWidget(
            self.Schedule_Combo, 0, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(Start_Button, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        # Final?
        layout.addWidget(
            self.Pomodoro_Label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Current_Category_Text_Label,
            1,
            0,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addWidget(
            self.Current_Category_Label, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Remaining_Time_Text_Label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Remaining_Time_Label, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Next_Category_Text_Label, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Next_Category_Label, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Current_Step_Text_Label, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Current_Step_Label, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Current_Activity_Text_Label,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addWidget(
            self.Current_Activity_Label, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Elapsed_Time_Text_Label, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Elapsed_Time_Label, 2, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Next_Activity_Text_Label, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Next_Activity_Label, 3, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Total_Steps_Text_Label, 4, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Total_Steps_Label, 4, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Schedule_Button, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Statistics_Button, 5, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.Options_Button, 5, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(self.Stop_Button, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        ### Button Events ###
        # Toggling Pomodoro
        self.Stop_Button.clicked.connect(self.Open_Stop)
        self.Statistics_Button.clicked.connect(self.Open_Statistics)
        self.Options_Button.clicked.connect(self.Open_Options)
        self.Schedule_Button.clicked.connect(self.Open_Schedule)

        Start_Button.clicked.connect(self.Start_Schedule)

        self.setWindowIcon(QIcon(path_to_icon))
        self.window = QWidget()
        self.window.setLayout(layout)
        self.setCentralWidget(self.window)
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.sizeHint())

        self.timer = QTimer()
        self.timer.timeout.connect(self.Timing)

    # Loading the schedule from JSON files
    def Load_Schedule(self):
        path_to_use = ""
        # Getting path from Schedule Type
        if Schedule_Type == "Work":
            path_to_use = path_to_Work
        elif Schedule_Type == "School":
            path_to_use = path_to_School
        elif Schedule_Type == "Hobby":
            path_to_use = path_to_Hobby
        elif Schedule_Type == "Lesiure":
            path_to_use = path_to_Lesiure
        elif Schedule_Type == "Vacation":
            path_to_use = path_to_Vacation
        elif Schedule_Type == "Sick":
            path_to_use = path_to_Sick
        elif Schedule_Type == "Work (School)":
            path_to_use = path_to_Work_p0Schoolp0
        elif Schedule_Type == "Hobby (School)":
            path_to_use = path_to_Hobby_p0Schoolp0
        elif Schedule_Type == "Leisure (School)":
            path_to_use = path_to_Leisure_p0Schoolp0
        elif Schedule_Type == "Work & School":
            path_to_use = path_to_Work_a0_School
        elif Schedule_Type == "Hobby & Leisure":
            path_to_use = path_to_Hobby_a0_Leisure
        # Loading the schedule
        with open(path_to_use) as temp_file:
            loaded_time = json.load(temp_file)
        return loaded_time

    # Formating the schedule from the raw JSON file
    def Format_Schedule(self):
        # Getting schedule from JSON in a dictionary
        unformatted = self.Load_Schedule()
        # Variables (Seconds)
        total_work = 0
        total_education = 0
        total_hobby = 0
        total_essential = 0
        total_productive = 0
        total_leisure = 0
        total_social = 0
        total_nothing = 0
        # Dictionary for formatted result
        formatted = {}
        # Get information from each part of the schedule
        for x in unformatted:
            # Loading Data
            load_step = int(x)
            load_category = unformatted[x]["Category"]
            load_activity = unformatted[x]["Activity"]
            load_duration = (
                int(unformatted[x]["Duration"]) * 60
            )  # Multiply by 60 because we need the time in seconds and the schedule is in minutes because I'm a person not a computer
            load_start = int(unformatted[x]["Start"]) * 60  # Get seconds
            load_end = int(unformatted[x]["End"]) * 60  # Get seconds
            # Getting category times
            if load_category == "Work":
                total_work += load_duration
            elif load_category == "Education":
                total_education += load_duration
            elif load_category == "Hobby":
                total_hobby += load_duration
            elif load_category == "Essential":
                total_essential += load_duration
            elif load_category == "Productive":
                total_productive += load_duration
            elif load_category == "Leisure":
                total_leisure += load_duration
            elif load_category == "Social":
                total_social += load_duration
            elif load_category == "Nothing":
                total_nothing += load_duration
            # Write to dictionary
            formatted[load_step] = {
                "Category": load_category,
                "Activity": load_activity,
                "Duration": load_duration,
                "Start": load_start,
                "End": load_end,
            }
        # Saving the total times to a global dictionary
        global total_schedule
        total_schedule["Work"] = total_work
        total_schedule["Education"] = total_education
        total_schedule["Hobby"] = total_hobby
        total_schedule["Essential"] = total_essential
        total_schedule["Productive"] = total_productive
        total_schedule["Lesiure"] = total_leisure
        total_schedule["Social"] = total_social
        total_schedule["Nothing"] = total_nothing
        # Saving variables
        global total_steps
        total_steps = len(formatted)
        # Returning schedule results
        return formatted

    # Initializing Everything
    def Init(self):
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

    # Starting Schedule
    def Start_Schedule(self):
        # Initializing Everything
        self.Init()
        # Getting the current schedule type
        global Schedule_Type
        Schedule_Type = self.Schedule_Combo.currentText()
        global schedule_data
        schedule_data = self.Format_Schedule()
        # Start the timer
        self.timer.start(1000)

    # Stopping Schedule
    def Stop_Schedule(self, button):
        # If the yes button is pressed stop, if not continue
        if button.text() == "&Yes":
            # Stop the timer
            self.timer.stop()
            # Initializing Everything
            self.Init()

    # Getting current time
    def get_time(self):
        # Getting current time
        now = datetime.now()
        # Getting time at midnight
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # Getting seconds today
        seconds_today = (now - midnight).seconds
        return seconds_today

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

    # Getting initial step
    def get_step(self, time):
        # Iterating through the schedule to find the right activity for the time
        for x in schedule_data:
            # Getting the start and end time
            start_time = schedule_data[x]["Start"]
            end_time = schedule_data[x]["End"]
            schedule_category = schedule_data[x]["Category"]
            # Returning when the current time falls between the start and end times
            if time >= start_time and time <= end_time:
                # Getting the amount of passed time from the current activity
                schedule_duration = time - start_time
                self.save_to_elapsed(schedule_category, schedule_duration)
                # Returning the step
                return x
            else:
                # Adding the elapsed time to the elapsed dictionary
                schedule_duration = schedule_data[x]["Duration"]
                self.save_to_elapsed(schedule_category, schedule_duration)

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

    # Play chime, possibly could have more types in the future for each category
    def Play_Chime(self):
        chime_sound.play()

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
        # Play chime
        self.Play_Chime()

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
                self.Stop_Schedule()  # Stopping when day ends, probably have some kind of screen pop up in the future
        # Math to find elapsed and remainting time per activity
        current_elapsed_time = seconds_today - begin_time
        current_remaining_time = next_time - seconds_today
        # Advancing time
        seconds_today += 1
        self.save_to_elapsed(current_category, 1)
        # Updating short labels
        self.update_short_labels()

    ###### Main Timer Logic ######
    def Timing(self):
        self.Check_Time()

    def Open_Statistics(self):
        statistics_window = QWidget()
        statistics_window.setWindowTitle("Statistics")

    def Open_Options(self):
        # Setting up gui
        options_window = QWidget()
        options_window.setWindowTitle("Options")

    def Open_Stop(self):
        # Setting up gui
        dialog = QMessageBox(
            text="This will stop the schedule. Are you sure?", parent=self
        )
        dialog.setWindowTitle("Confirmation")
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        # Checking the answer of the window
        dialog.buttonClicked.connect(self.Stop_Schedule)
        # Closing the window
        dialog.exec()

    def Open_Schedule(self):
        # Setting up gui
        schedule_window = QTableWidget()
        schedule_window.setWindowTitle("Schedule")
        schedule_window.setRowCount(len(schedule_data))
        schedule_window.setColumnCount(6)
        schedule_window.setHorizontalHeaderLabels(
            ["Step", "Category", "Activity", "Duration", "Start", "End"]
        )
        # Writing labels for each schedule entry
        for x in schedule_data:
            step_text = QTableWidgetItem(x)
            category_text = QTableWidgetItem(schedule_data[x]["Category"])
            activity_text = QTableWidgetItem(str(schedule_data[x]["Activity"]))
            duration_text = QTableWidgetItem(
                datetime.utcfromtimestamp(schedule_data[x]["Duration"]).strftime(
                    "%H:%M:%S"
                )
            )
            start_text = QTableWidgetItem(
                datetime.utcfromtimestamp(schedule_data[x]["Start"]).strftime(
                    "%H:%M:%S"
                )
            )
            end_text = QTableWidgetItem(
                datetime.utcfromtimestamp(schedule_data[x]["End"]).strftime("%H:%M:%S")
            )
            schedule_window.setItem(x, 0, step_text)
            schedule_window.setItem(x, 1, category_text)
            schedule_window.setItem(x, 2, activity_text)
            schedule_window.setItem(x, 3, duration_text)
            schedule_window.setItem(x, 4, start_text)
            schedule_window.setItem(x, 4, end_text)
            schedule_window.show()

    ### Timer for Repeated Events & Running This###
    timer = QTimer()
    timer.timeout.connect(Timing)


# endregion Main Gui


# region Initializing Everything

# APP?
### Showing the application and window ###
app = QApplication([])
w = MainWindow()
w.show()
sys.exit(app.exec())
# endregion
