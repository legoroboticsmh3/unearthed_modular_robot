from pybricks.tools import wait

#these are all the default setings for the robot
# hub = PrimeHub()
# R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
# L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
# Left_attach=Motor(Port.A, gears=[28, 36])
# Right_attach=Motor(Port.B,)
# Drive=DriveBase(L_motor, R_motor, 62.4, 110)

#going to the mission model mission 3
async def run_10(robot):
    # robot.Drive.settings(straight_speed=650)
    # robot.Drive.settings(turn_rate=160)

    # await robot.Drive.straight(360)
    # await robot.Drive.turn(-90)
    # await robot.Drive.straight(640)
    # await robot.Drive.turn(25)
    # await robot.Drive.straight(-175)
    # await robot.Drive.turn(-27)
    # await robot.Drive.turn(10)
    # await robot.Drive.straight(-10)
    # await robot.Drive.straight(20)
    # await robot.Left_attach.run_angle(500,-823)

    # # Turn to Dino 
    # await robot.Drive.turn(23)

    # # Lower the Right Arm and Move
    # await robot.Right_attach.run_angle(360,-90)
    # await robot.Drive.straight(210)
    # await robot.Drive.turn(24)
    # await robot.Drive.straight(10)

     #  Lift the Dino
     await robot.Right_attach.run_angle(720,150)
     await robot.Drive.straight(-100)
     await robot.Drive.turn(-90)
     await robot.Drive.straight(300)