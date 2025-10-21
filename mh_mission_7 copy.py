
async def run_2(robot):
    await robot.Drive.straight(770)
    await robot.Drive.turn(40)
    await robot.Drive.straight(-40)
    await robot.Right_attach.run_angle(250,55)
    await robot.Drive.straight(63)
    await robot.Right_attach.run_angle(200,-50)
    await robot.Drive.turn(-40)
    await robot.Drive.straight(-770)
