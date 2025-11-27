from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_7(robot):
    print("Starting Run: " + __name__)

    robot.Drive.settings(turn_rate=160)
    # Attach_Right=Motor(Port.D)
    # Attach_Left=Motor(Port.C)
    #Drive.straight(680)  #this is the distance for the original wihout the mission 9 back attachment
    await robot.Drive.straight(250)  
    await robot.Drive.turn(-45)
    await robot.Drive.straight(265)

    await robot.Right_attach.run_angle(200,80*-1) # the attachment to latch to the sale
    print("Latching to Sale")
    #robot.Drive.settings(straight_speed=200)
    await robot.Drive.straight(-73)
    print("Pulling Sale Back")
    await robot.Right_attach.run_angle(180,-80*-1)
    print("Releasing Sale Latch")
    wait(100)
    print("wait")
    robot.Drive.settings(straight_speed=500)
    #robot.Drive.settings(turn_rate=160)
    print("Driving Backwards")
    await robot.Drive.straight(-50)
    print("Backing Up Complete")
    await robot.Drive.straight(20)
    print("Adjusting Position")
    await robot.Right_attach.run_angle(200,80*-1)
    await robot.Drive.straight(50)
    await robot.Right_attach.run_angle(200,-80*-1)
    print("Lowering Attachment")
    await robot.Drive.straight(-300)
    print("Final Backward Move Complete")


    