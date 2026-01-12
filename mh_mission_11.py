from utils.mh_dump_all import dump_all
from pybricks.tools import wait


async def run_4(robot):  
    robot_correction_magic_number = -2
    # dump_all(robot) + __name__)
    robot.Drive.settings(turn_rate=120)
    robot.Drive.settings(straight_speed=600)
    #robot.Drive.use_gyro(True)
    await robot.Drive.straight(275) #was -315
    #await robot.Right_attach.run_angle(180, -55)
        
    await robot.Drive.turn(90) # Turn
    print("Starting Run: n and go to mission 11")
    await robot.Drive.straight((-690+robot_correction_magic_number))
    await robot.Drive.turn(90)

    await robot.Drive.straight((65+robot_correction_magic_number)) # Go towards mission 11
    await robot.Drive.turn(-10) # turn to lock gears with mission
    await robot.Left_attach.run_angle(700, 1600) # Turn the gear to pick up artifct

    await robot.Drive.turn(25) #  turn to unlock the gears 
    await robot.Drive.straight(-200) #  driving back from mission to prepare to go back to base
    # await robot.Drive.turn(45)
    # await robot.Right_attach.run_angle(700, 1600)
    await robot.Drive.turn(65) #alligning to red base
    robot.Drive.settings(straight_speed=500)
    await robot.Drive.straight(900)# driving back to red base