

# hub = PrimeHub()

# R_Motor = Motor(Port.E,positive_direction=Direction.COUNTERCLOCKWISE, gears=[28, 20])
# L_Motor = Motor(Port.F,positive_direction=Direction.CLOCKWISE, gears=[28, 20])
# Left_attach=Motor(Port.A, gears=[28, 36])
# Right_attach=Motor(Port.B, gears=[28, 36])
# Drive= DriveBase(L_Motor,R_Motor,62.4,110)
# Drive.use_gyro(True)
async def run_6(robot):
    print("Starting Run: " + __name__)
    robot.Drive.use_gyro(True)
    await robot.Drive.straight(250)
    await robot.Drive.turn(90)
    await robot.Drive.straight(-670)
    await robot.Drive.turn(25)
    await robot.Drive.straight(65)
    await robot.Right_attach.run_angle(250,-600)
#Drive.straight(-200)
#Drive.turn(-25)
#Drive.straight(700)


