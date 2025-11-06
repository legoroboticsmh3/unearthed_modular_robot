from pybricks.tools import wait


#going to the mission model mission 3
async def run_4(robot):
    robot.Drive.settings(straight_speed=650)
    robot.Drive.settings(turn_rate=160)

    await robot.Drive.straight(550)
    #await robot.Right_attach.run_angle(200, 130*-1)
    #right arm down to grab
    robot.Right_attach.dc(-75)
    await wait(250)

    # drive back and lift right arm up
    robot.Right_attach.stop()
    await robot.Drive.straight(-120)
    await robot.Right_attach.run_angle(200, -130*-1)

    # drive straight to lift ship up
    await robot.Drive.straight(270)

    # deliver
    await robot.Left_attach.run_angle(200, 70*-0.77)
    await robot.Left_attach.run_angle(200, -70*-0.77)
    # drive back home
    await robot.Drive.straight(-550)