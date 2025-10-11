from pybricks.tools import multitask, run_task
from mh_robot import Robot
from mh_loader import loader
from mh_swerve import swerve
from mh_media import MY_SONGS
from mh_config import CONFIG


#make sure to have the wheel calibrations done. Go to configs to check. The numbers are listed there.

#Create Robot Object
robot = Robot(CONFIG)
#Uncomment line below for STARWARS THEME!!!
#robot.speaker.play_notes(MY_SONGS['STAR_WARS_1'], tempo=150)

#Runs
from mh_mission_02 import run_1
from mh_run_wheelclean import wheelclean

#Remote Control
#from mh_run_remote import run_remote

#Run Loader Menu
async def main():
    #testing loader
    #await multitask(loader(robot,[run_9]), swerve(robot))
    #full run loader
    await multitask(loader(robot,[run_1]), swerve(robot))
    #cleaning loader
    #await multitask(loader(robot,[wheelclean]), swerve(robot))
run_task(main())

#Finish Main Sequence
robot.speaker.play_notes(MY_SONGS['STAR_WARS_1'], tempo=120)
robot.speaker.play_notes(MY_SONGS['STAR_WARS_2'], tempo=120)