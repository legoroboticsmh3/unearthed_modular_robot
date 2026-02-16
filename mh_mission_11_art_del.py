from utils.mh_dump_all import dump_all
from pybricks.tools import wait, multitask


async def run_4(robot):  
    await multitask(robot.Right_attach.run_angle(100,90), wait(500), race=True)

    robot_correction_magic_number = -2
    # dump_all(robot) + __name__)
    robot.Drive.settings(turn_rate=120)
    robot.Drive.settings(straight_speed=600)
    #robot.Drive.use_gyro(True)
    await robot.Drive.straight(275) #was -315
        
    await robot.Drive.turn(90) # Turn
    print("Starting Run: n and go to mission 11")
    await robot.Drive.straight((-690+robot_correction_magic_number))
    await robot.Drive.turn(90)

    await robot.Drive.straight((65+robot_correction_magic_number)) # Go towards mission 11
    await robot.Drive.turn(-11) # turn to lock gears with mission
    await robot.Left_attach.run_angle(700, 1600) # Turn the gear to pick up artifct

    await robot.Drive.turn(20) #  turn to unlock the gears 
    await robot.Drive.straight(-180) #  driving back from mission to prepare to go to forum
    await robot.Drive.turn(90) #alligning to forum
    robot.Drive.settings(straight_speed=500)
    await robot.Drive.straight(250) #moving to forum to drop off artifacts
    await multitask(robot.Right_attach.run_angle(200, -200),wait(1000), race=True) #dropping artifacts

    await robot.Drive.straight(-150) # Drive back
    await robot.Right_attach.run_angle(600, 200) #lifting arm

    await robot.Drive.turn(-30) #alignging towards base
    await robot.Drive.straight(750)# driving back to red base