from pybricks.tools import wait


#Shows mission 5
async def run_5(robot):#n
    print("Starting Run: " + __name__)#D
    robot.Drive.settings(straight_speed=400)
    robot.Drive.settings(turn_rate=100)

    await robot.Drive.straight(180)
    await robot.Drive.turn(88)
    await robot.Drive.straight(90)
    await robot.Left_attach.run_angle(80)
    await robot.Left_attach.run_angle(-80)