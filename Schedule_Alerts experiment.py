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


class MainWindow(QMainWindow):
    # Setting up
    def __init__(self):
        super.__init__()

        pass
