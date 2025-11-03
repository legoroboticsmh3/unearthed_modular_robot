from pybricks.tools import wait

async def run_9(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=500)
    
    #Drives to Mision 13
    await robot.Drive.straight(67)
    await robot.Drive.turn(60)
    await robot.Drive.straight(680)
    await robot.Drive.turn(-93)
    await wait(100)
    await robot.Drive.straight(40)
    await wait(100)
    robot.Right_attach.dc(-120)
    await wait(100)
    await robot.Right_attach.run_angle(500,100)
    await wait(100)
    await robot.Drive.turn(90)