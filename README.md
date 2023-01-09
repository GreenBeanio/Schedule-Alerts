# Schedule-Alert

## What Does It Do?

The program shows information about a loaded schedule. It loads a schedule from a json file (explained below). It will then look through the schedule and the current time to determine what you should be doing currently. It will display the time elapsed and remaining time of each activity. It also displays what the next upcoming activity is, as well as the current step and total steps in the schedule. There is also an option to load a table with all the schedule information. Another option is to load the statistics of the schedule, including the total elapsed time, remaining time, and total time per category in the schedule.

When a schedule is loaded it will calculate the elapsed and remaining time based on the assumption that the schedule had been followed up until that point. In the future further variants of the program may be developed to not make this assumption and only use the true elapsed time since the program has been running.

---
## Schedules

The schedule system in use is a schedule system that I developed to track how I'm spending my time.

***Step*** is simply the number of activities in order starting with 1. This is used to analyze the schedule easier as well as telling the order of activities at a glance.

The schedule system uses 8 ***Categories*** in order of their importance.

The 8 categories are:
1. Work
    - Work related activities.
        - Examples: Working, Meeting, Break
2. Education
    - Education related activities.
        - Examples: School, Course, Research
3. Hobby
    - Hobbies are personal activities that lead to the creation of something.
        - Examples: Art, Music, Writing, Programming, Video Production
4. Essential
    - Activities that must be done for survival.
        - Examples: Sleeping, Eating, Bathroom, Exercise, Meditation
5. Productive
    - Activies that need to be done.
        - Examples: Driving, Cooking, Cleaning
5. Leisure
    - Activities that lead to the consumption of something.
        - Examples: Shows, Movies, Reading, Video games, Sports
7. Social
    - Activities that involve socializing.
        - Examples: Talking, Hanging out, Party
8. Nothing
    - Time spent doing nothing.
        - Examples: Lying in bed, Waiting, Zoning out

There are also ***Activities*** which can be anything you actually want to do in that category.

Then there are 3 different times: Duration, Start, & End. All of the times are in minutes.

***Duration*** is the amount of time that the activity will take.

***Start*** is the time at which the activity starts.

***End*** is the time at which the activity ends.

Yes, the duration could be found by subtracting the start and the end. Yes, the start and end could be calculated using the duration and the assumption that the first activity starts at midnight. I am using all 3 in hopes of some form of redundancy. It also makes it easier to read and modify the schedules as a human. I assume that you are a human... maybe not.

Feel free to modify the schedules to fit your needs. I have made them to fit mine. There should be no limit to how many steps you can put in. Just make sure to start it with 0 for midnight and end it at 1440. As well as having all time times in between. It will crash if not every minute is accounted for at some point. I'm not sure what will happen during day lights savings shenanigans, it will probably crash ¯\\\_(ツ)_/¯. You will have to keep the file names the same or change them in the python script. Maybe I'll implement a way for it to read all the json files in a directory/folder in the future just for you :^).

---
## Reason For Creation

This program was created in hopes that it will assist me in following a schedule. I have grown tired of wasting my time not doing what I want to do. Hopefully this program can help me stick to schedules I want to follow.

---

## Running The Python Script
### Windows
- Initial Run
    - cd /your/folder
    - python3 -m venv env
    - call env/Scripts/activate.bat
    - python3 -m pip install -r requirements.txt
    - python3 Schedule_Alerts.py
- Running After
    - cd /your/folder
    - call env/Scripts/activate.bat && python3 Schedule_Alerts.py
- Running Without Terminal Staying Around
    - Change the file type from py to pyw
    - You should just be able to click the file to launch it
    - May need to also change python3 to just python if it doesn't work after the change
        - In the first line of the code change python3 to python
### Linux
- Initial Run
    - cd /your/folder
    - python3 -m venv env
    - source env/bin/activate
    - python3 -m pip install -r requirements.txt
    - python3 Schedule_Alerts.py
- Running After
    - cd /your/folder
    - source env/bin/activate && python3 Schedule_Alerts.py
- Running Without Terminal Staying Around
    - Run the file with nohup
    - May have to set executable if it's not already
        - chmod +x Schedule_Alerts.py