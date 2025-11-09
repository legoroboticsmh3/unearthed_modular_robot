

# hub = PrimeHub()

# R_Motor = Motor(Port.E,positive_direction=Direction.COUNTERCLOCKWISE, gears=[28, 20])
# L_Motor = Motor(Port.F,positive_direction=Direction.CLOCKWISE, gears=[28, 20])
# Left_attach=Motor(Port.A, gears=[28, 36])
# Right_attach=Motor(Port.B, gears=[28, 36])
# Drive= DriveBase(L_Motor,R_Motor,62.4,110)
# Drive.use_gyro(True)
async def run_11(robot): # was "run_6"
    print("Starting Run: " + __name__)
    robot.Drive.use_gyro(True)

    await robot.Drive.straight(-320) #was -315
    await robot.Drive.turn(88)
    await robot.Drive.straight(-660) # Goes to mission 11
    await robot.Drive.turn(28)
    await robot.Right_attach.run_angle(200, -140)
    await robot.Drive.straight(-310)
    await robot.Drive.turn(-40)#was -40
    await robot.Left_attach.run_angle(200, 340) # Turns gear to lift up artifact
    await robot.Drive.turn(40)
    await robot.Drive.straight(140)
    await robot.Drive.turn(-18)
    robot.Drive.settings(straight_speed=900) # increases speed to move fast
    await robot.Drive.straight(-900) # goes to blue base
    robot.Drive.settings(straight_speed=500) # reset the speed to normal


