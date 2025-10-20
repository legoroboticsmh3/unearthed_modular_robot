

#these are all the default setings for the robot
# hub = PrimeHub()
# R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
# L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
# Left_attach=Motor(Port.A, gears=[28, 36])
# Right_attach=Motor(Port.B,)
# Drive=DriveBase(L_motor, R_motor, 62.4, 110)

#going to the mission model mission 3
async def run_4(robot):
    await robot.Drive.straight(550)
    await robot.Right_attach.run_angle(200, 130)
    await robot.Drive.straight(-200)
    await robot.Right_attach.run_angle(200, -130)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(180)
    await robot.Drive.turn(90)
    await robot.Right_attach.run_angle(200, -130)
    await robot.Drive.straight(355)
    await robot.Drive.straight(-500)
