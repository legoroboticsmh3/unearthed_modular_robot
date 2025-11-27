from utils.mh_dump_all import dump_all
from pybricks.tools import wait


async def run_4(robot):  
    robot_correction_magic_number = -2
    # dump_all(robot)
    print("Starting Run: " + __name__)
    robot.Drive.settings(turn_rate=120)
    robot.Drive.settings(straight_speed=300)
    #robot.Drive.use_gyro(True)
    await robot.Drive.straight(-300) #was -315
    await robot.Right_attach.run_angle(180, -55)
        
    await robot.Drive.turn(90) # Turn and go to mission 11
    await robot.Drive.straight(-(950+robot_correction_magic_number)) 
    await robot.Drive.turn(90)

    await robot.Drive.straight(-(158+robot_correction_magic_number)) # Go towards mission 11
    await robot.Drive.turn(-18)
    await robot.Left_attach.run_angle(300, -520) # Turn the lever.

    # Move back towards Mission 10
    await robot.Drive.turn(45)
    await robot.Drive.straight(60)
    await robot.Drive.turn(-20)
    await robot.Drive.straight(120)
 
    # For the force move forward the arm and then back
    await robot.Right_attach.run_angle(180, 25)
    await robot.Right_attach.run_angle(270, -100)

    # Go towards the blue area.
    await robot.Drive.straight(-80)
    await robot.Drive.turn(90)
    robot.Drive.settings(straight_speed=800)
    await robot.Drive.straight(650)
    robot.Drive.settings(straight_speed=500)