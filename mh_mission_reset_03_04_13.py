from pybricks.tools import wait, multitask

#DO NOT USE THIS FILE, USE mh_mission_03_13.py INSTEAD

async def run_12(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(120)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()
