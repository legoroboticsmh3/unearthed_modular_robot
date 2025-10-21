from pybricks.tools import wait

#these are all the default setings for the robot
# hub = PrimeHub()
# R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
# L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
# Left_attach=Motor(Port.A, gears=[28, 36])
# Right_attach=Motor(Port.B,)
# Drive=DriveBase(L_motor, R_motor, 62.4, 110)

#going to the mission model mission 3
async def run_4(robot):
    robot.Drive.settings(straight_speed=350)
    robot.Drive.settings(turn_rate=160)
    await robot.Drive.straight(470)
    #await robot.Right_attach.run_angle(200, 130*-1)
    robot.Right_attach.dc(-75)
    await wait(250)
    robot.Right_attach.stop()
    await robot.Drive.straight(-120)
    await robot.Right_attach.run_angle(200, -130*-1)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(182)
    await robot.Drive.turn(90)
    await robot.Right_attach.run_angle(200, 130*-1)
    await robot.Drive.straight(-60)
    await robot.Drive.straight(370)
    await robot.Drive.straight(-600)

'''
    robot.Drive.settings(straight_speed=350)
    robot.Drive.settings(turn_rate=160)
    await robot.Drive.straight(470)
    await robot.Right_attach.run_angle(200, 130*-1)
    await robot.Drive.straight(-120)
    await robot.Right_attach.run_angle(200, -130*-1)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(182)
    await robot.Drive.turn(90)
    await robot.Right_attach.run_angle(200, 130*-1)
    await robot.Drive.straight(-60)
    await robot.Drive.straight(370)
    await robot.Drive.straight(-600)
'''