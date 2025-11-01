from pybricks.tools import multitask, run_task
from pybricks.tools import wait
from mh_robot import Robot

from mh_loader import loader
#from mh_media import MY_SONGS
from mh_config import CONFIG


#make sure to have the wheel calibrations done. Go to configs to check. The numbers are listed there.

#Create Robot Object
robot = Robot(CONFIG)


#Uncomment line below for STARWARS THEME!!!
#robot.speaker.play_notes(MY_SONGS['STAR_WARS_1'], tempo=150)

#Runs
#blue side code
from mh_mission_09_10 import run_1
from mh_mission_7 import run_2 
from mh_mission_05_06_09 import run_3
# from mh_mission_11 import run_6
#red side code
from mh_mission_12 import run_4
from mh_mission_01_02 import run_5
from mh_mission_03_04 import run_6
from mh_mission_09 import run_7   #this is to test mission 9 (what's on sale)


#Remote Control
#from mh_run_remote import run_remote

#Run Loader Menu
async def main():
    #full run loader

    await multitask(loader(robot,[run_1,run_2,run_3,run_4,run_5,run_6,run_7]))

   # await multitask(loader(robot,[run_5])) red side code

run_task(main())


#robot.display.number(1)
#wait(100000000)
#Finish Main Sequence
#robot.speaker.play_notes(MY_SONGS['STAR_WARS_1'], tempo=120)
#robot.speaker.play_notes(MY_SONGS['STAR_WARS_2'], tempo=120)

