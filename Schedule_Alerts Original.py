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

# Loading the schedule from JSON files
def Load_Schedule():
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
def Format_Schedule():
    # Getting schedule from JSON in a dictionary
    unformatted = Load_Schedule()
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
def Init():
    # Setting text
    Current_Category_Label.setText("Not Started")
    Current_Activity_Label.setText("Not Started")
    Current_Step_Label.setText("Not Started")
    Next_Category_Label.setText("Not Started")
    Elapsed_Time_Label.setText("Not Started")
    Remaining_Time_Label.setText("Not Started")
    Total_Steps_Label.setText("Not Started")
    Next_Activity_Label.setText("Not Started")
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


# Play chime, possibly could have more types in the future for each category
def Play_Chime():
    chime_sound.play()


# Starting Schedule
def Start_Schedule():
    # Initializing Everything
    Init()
    # Getting the current schedule type
    global Schedule_Type
    Schedule_Type = Schedule_Combo.currentText()
    global schedule_data
    schedule_data = Format_Schedule()
    # Start the timer
    timer.start(1000)


# Stopping Schedule
def Stop_Schedule(button):
    # If the yes button is pressed stop, if not continue
    if button.text() == "&Yes":
        # Stop the timer
        timer.stop()
        # Initializing Everything
        Init()


# region Schedule GUI
def Open_Schedule():
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
            datetime.utcfromtimestamp(schedule_data[x]["Duration"]).strftime("%H:%M:%S")
        )
        start_text = QTableWidgetItem(
            datetime.utcfromtimestamp(schedule_data[x]["Start"]).strftime("%H:%M:%S")
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


# endregion

# region Statistics GUI
def Open_Statistics():
    statistics_window = QWidget()
    statistics_window.setWindowTitle("Statistics")


# endregion

# region Options GUI
def Open_Options():
    # Setting up gui
    options_window = QWidget()
    options_window.setWindowTitle("Options")


# endregion

# region Stop GUI
def Open_Stop():
    # Setting up gui
    dialog = QMessageBox(
        text="This will stop the schedule. Are you sure?", parent=window
    )
    dialog.setWindowTitle("Confirmation")
    dialog.setIcon(QMessageBox.Icon.Question)
    dialog.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    # Checking the answer of the window
    dialog.buttonClicked.connect(Stop_Schedule)
    # Closing the window
    dialog.exec()


# endregion

# region Main GUI Setup
# Setting up application and window
app = QApplication([])
window = QWidget()
window.setWindowTitle("Schedule Alerts")
# Setting up a label and button
Pomodoro_Label = QLabel("<h1>Schedule</h1>", parent=window)  # Static

Current_Category_Text_Label = QLabel("Current Category:", parent=window)  # Static
Current_Category_Label = QLabel("Category", parent=window)  # Dynamic
Current_Activity_Text_Label = QLabel("Current Activity:", parent=window)  # Static
Current_Activity_Label = QLabel("Activity", parent=window)  # Dynamic
Current_Step_Text_Label = QLabel("Current Step:", parent=window)  # Static
Current_Step_Label = QLabel("Curent Step", parent=window)  # Dynamic
Next_Category_Text_Label = QLabel("Next Category:", parent=window)  # Static
Next_Category_Label = QLabel("Next Category", parent=window)  # Dynamic
Elapsed_Time_Text_Label = QLabel("Elapsed Time:", parent=window)  # Static
Elapsed_Time_Label = QLabel("Elapsed Time", parent=window)  # Dynamic
Remaining_Time_Text_Label = QLabel("Remaining Time:", parent=window)  # Static
Remaining_Time_Label = QLabel("Remaining Time", parent=window)  # Dynamic
Total_Steps_Text_Label = QLabel("Total Steps:", parent=window)  # Static
Total_Steps_Label = QLabel("Total Steps", parent=window)  # Dynamic
Next_Activity_Text_Label = QLabel("Next Activity:", parent=window)  # Static
Next_Activity_Label = QLabel("Next", parent=window)  # Dynamic
Stop_Button = QPushButton("Stop", parent=window)  # Static
Statistics_Button = QPushButton("Statistics", parent=window)  # Static
Options_Button = QPushButton("Options", parent=window)  # Static
Schedule_Button = QPushButton("Schedule", parent=window)  # Static
Schedule_Combo = QComboBox(parent=window)  # Static
Schedule_Combo.addItems(
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
Schedule_Combo.setCurrentIndex(0)

# Temporary Button
Start_Button = QPushButton("Start", parent=window)  # Static

# Laying it all out
layout = QGridLayout()
# Temprary location
layout.addWidget(Schedule_Combo, 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Start_Button, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
# Final?
layout.addWidget(Pomodoro_Label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(
    Current_Category_Text_Label, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter
)
layout.addWidget(Current_Category_Label, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(
    Remaining_Time_Text_Label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter
)
layout.addWidget(Remaining_Time_Label, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Category_Text_Label, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Category_Label, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Current_Step_Text_Label, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Current_Step_Label, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(
    Current_Activity_Text_Label, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
)
layout.addWidget(Current_Activity_Label, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Time_Text_Label, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Time_Label, 2, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Activity_Text_Label, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Activity_Label, 3, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Total_Steps_Text_Label, 4, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Total_Steps_Label, 4, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Schedule_Button, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Statistics_Button, 5, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Options_Button, 5, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Stop_Button, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter)

### Button Events ###
# Toggling Pomodoro
Stop_Button.clicked.connect(Open_Stop)
Statistics_Button.clicked.connect(Open_Statistics)
Options_Button.clicked.connect(Open_Options)
Schedule_Button.clicked.connect(Open_Schedule)

Start_Button.clicked.connect(Start_Schedule)
# endregion

# Getting current time
def get_time():
    # Getting current time
    now = datetime.now()
    # Getting time at midnight
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # Getting seconds today
    seconds_today = (now - midnight).seconds
    return seconds_today


# Save to elapsed dictionary
def save_to_elapsed(Elapsed_Category, Elapsed_Time):
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
def get_step(time):
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
            save_to_elapsed(schedule_category, schedule_duration)
            # Returning the step
            return x
        else:
            # Adding the elapsed time to the elapsed dictionary
            schedule_duration = schedule_data[x]["Duration"]
            save_to_elapsed(schedule_category, schedule_duration)


# Getting the next time
def get_next_time():
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
def update_long_labels():
    Current_Category_Label.setText(current_category)
    Current_Activity_Label.setText(schedule_data[current_step]["Activity"])
    Current_Step_Label.setText(str(current_step))
    Total_Steps_Label.setText(str(total_steps))
    if current_step < total_steps:
        Next_Category_Label.setText(schedule_data[current_step + 1]["Category"])
        Next_Activity_Label.setText(schedule_data[current_step + 1]["Activity"])
    else:
        Next_Category_Label.setText("End")
        Next_Activity_Label.setText("End")


# Updating labels that change often
def update_short_labels():
    # Changing times to time format
    display_elapsed = datetime.utcfromtimestamp(current_elapsed_time).strftime(
        "%H:%M:%S"
    )
    display_remaining = datetime.utcfromtimestamp(current_remaining_time).strftime(
        "%H:%M:%S"
    )
    # Changing labels
    Elapsed_Time_Label.setText(display_elapsed)
    Remaining_Time_Label.setText(display_remaining)


# Advancing to the next step
def advance_step():
    # Global variables
    global current_step
    # Advancing the step
    current_step += 1
    # Getting the new next time
    get_next_time()
    # Updating long labels
    update_long_labels()
    # Play chime
    Play_Chime()


### Checking Time ###
def Check_Time():
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
        seconds_today = get_time()
        # Getting initial step based on the time
        current_step = get_step(seconds_today)
        # Getting the next time
        get_next_time()
        # Updating labels
        update_long_labels()
    elif current_step > 0 and current_step < total_steps:
        if seconds_today >= next_time:
            advance_step()
    elif current_step == total_steps:
        if seconds_today >= next_time:
            Stop_Schedule()  # Stopping when day ends, probably have some kind of screen pop up in the future
    # Math to find elapsed and remainting time per activity
    current_elapsed_time = seconds_today - begin_time
    current_remaining_time = next_time - seconds_today
    # Advancing time
    seconds_today += 1
    save_to_elapsed(current_category, 1)
    # Updating short labels
    update_short_labels()


###### Main Timer Logic ######
def Timing():
    Check_Time()


# region Initializing Everything
Init()
### Timer for Repeated Events & Running This###
timer = QTimer()
timer.timeout.connect(Timing)
window.setWindowIcon(QIcon(path_to_icon))
### Showing the application and window ###
window.setLayout(layout)
window.setMinimumSize(window.minimumSizeHint())
window.setMaximumSize(window.sizeHint())
window.show()
sys.exit(app.exec())
# endregion
