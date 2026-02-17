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
from mh_mission_7 import run_5   #Heavy lifting
from mh_mission_08_05_06_09 import run_6  #Boulder and Who Lives There
from mh_mission_08_09 import run_7  #Whats on Sale Back Attachment
from mh_mission_01_02 import run_2 # Map Reveal and Topsoil Pickup
#from mh_mission_12 import run_1  # Mission Model Mission 12
from mh_mission_12 import run_1  # Mission Model Mission 12
from mh_mission_03_13_04_Sai import run_3  # Mission Model Mission 3 and 13
from mh_mission_11 import run_4
from mh_mission_04 import run_8
from mh_mission_14 import run_7
from mh_mission_03_13_axle import run_11
from mh_mission_reset_03_04_13 import run_12


#Gamma Runs (Uncomment if using sigma robot)
# from gamma_robot_runs.mh_mission_12_gamma import run_1  # Mission Model Mission 12
# from gamma_robot_runs.mh_mission_7_gamma import run_5   #Heavy lifting
# from gamma_robot_runs.mh_mission_11_gamma import run_4

#Remote Control
#from utils.mh_run_remote import run_remote
#Run Loader Menu
async def main():
    #full run loader

    await multitask(loader(robot,[run_6, run_5, run_4,run_12, run_3, run_2,run_1 , run_7 ,run_8, run_11]))     

run_task(main())
