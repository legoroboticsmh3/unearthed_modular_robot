from pybricks.tools import wait



async def run_12(robot):#n
    print("Starting Run: " + __name__)#D
    robot.Drive.settings(straight_speed=100)
    robot.Drive.settings(turn_rate=100)

    await robot.Drive.straight(688)
    await robot.Drive.turn(-86)
    await robot.Left_attach.run_angle(100,20)
    await wait(100)
    await robot.Drive.straight(55)
    await robot.Left_attach.run_angle(1000, 90*-0.77)