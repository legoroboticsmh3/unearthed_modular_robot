from utils.mh_dump_all import dump_all
from pybricks.tools import wait


async def run_4(robot):  
    robot_correction_magic_number = -2
    # dump_all(robot) + __name__)
    robot.Drive.settings(turn_rate=120)
    robot.Drive.settings(straight_speed=300)
    #robot.Drive.use_gyro(True)
    await robot.Drive.straight(275) #was -315
    #await robot.Right_attach.run_angle(180, -55)
        
    await robot.Drive.turn(90) # Tur
    print("Starting Run: n and go to mission 11")
    await robot.Drive.straight((-700+robot_correction_magic_number))
    await robot.Drive.turn(90)

    await robot.Drive.straight((65+robot_correction_magic_number)) # Go towards mission 11 originally 158
    await robot.Drive.turn(-22)
    await robot.Left_attach.run_angle(500, -1600) # Turn the lever.

    await robot.Drive.turn(25) #  originally 35
    await robot.Drive.straight(-220) #  originally 180
    await robot.Drive.turn(-140)
    await robot.Drive.straight(-800)

    # # Move back towards Mission 10
    # await robot.Drive.turn(35)
    # await robot.Drive.straight(-70)
    # await robot.Drive.turn(20)
    # await robot.Drive.straight(-120)
 
    # # For the force move forward the arm and then back
    # await robot.Right_attach.run_angle(200, 60)
    # #await robot.Right_attach.run_angle(270, -100)

    # # Go towards the blue area.
    # await robot.Drive.straight(-80)
    # await robot.Drive.turn(90)
    # robot.Drive.settings(straight_speed=500)
    # await robot.Drive.straight(650)
    # robot.Drive.settings(straight_speed=500)