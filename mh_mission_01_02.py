from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt

async def run_3(robot):
    print("Starting Run: " + __name__)

    # R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
    # L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
    # Left_attach=Motor(Port.A, gears=[28, 36])
    # Right_attach=Motor(Port.B, gears=[28, 36])
    # await robot.Drive.=await robot.Drive.Base(L_motor, R_motor, 62.4, 110)
    # await robot.Drive..use_gyro(True)

    await robot.Drive.straight(670)
    await robot.Drive.turn(-43.5)
    await robot.Drive.straight(253)
    await robot.Right_attach.run_angle(500,-180) 
    await robot.Drive.straight(-200) 
    await robot.Drive.turn(44.5)
    await robot.Drive.straight(-670)
    #wait(10000)
    #await robot.Drive.straight(550)
    #Right_attach.run_angle(200, 130)
    #await robot.Drive.straight(-200)
    #Right_attach.run_angle(200, -130)
    #await robot.Drive.turn(-90)
    #await robot.Drive.straight(180)
    #await robot.Drive.turn(90)
    #Right_attach.run_angle(200, 130)
    #await robot.Drive..straight(300)
