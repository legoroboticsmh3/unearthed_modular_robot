from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_8(robot):
    print("Starting Run: " + __name__)
    #print(robot.gyro.heading())
    #await wait(300)
#    robot.Drive.stop()
#    robot.Drive.use_gyro(True)
#    robot.gyro.reset_heading(0)
    #print(robot.gyro.heading())
    robot.Drive.settings(turn_rate=160)

    #print(robot.gyro.heading())
    #robot.Drive.drive(60,0)
    #start_time = robot.timer.time()
    #while(robot.timer.time()-start_time < 3000):
    #    await wait(100)
    #    print(robot.gyro.heading())

    await robot.Drive.straight(430)
    print(robot.gyro.heading())
    
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer  up
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer up
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,120) #hammer up
    await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
    await robot.Right_attach.run_angle(500,85) #hammer up
    await robot.Drive.straight(-120)
    await robot.Drive.turn(-15)
    await robot.Drive.straight(215)
    await robot.Drive.turn(-100)
    await robot.Right_attach.run_angle(500,-100)
    await robot.Drive.straight(40)
    await robot.Right_attach.run_angle(500,100)
    await robot.Drive.straight(-60)
    #await robot.Drive.straight(20)
    #await robot.Drive.straight(-30)
    #await robot.Drive.straight(-430) #drive back
    await robot.Drive.turn(-90)
    await robot.Drive.straight(235)



