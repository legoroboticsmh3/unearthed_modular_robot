from pybricks.tools import wait, multitask


#going to the mission model mission 3
async def run_1(robot):
    #robot.Drive.settings(straight_speed=400)
    robot.Drive.settings(turn_rate=160)
    robot.Right_attach.dc(55)
    #robot.Left_attach.dc(90)
    await wait(600)
    await robot.Right_attach.run_angle(200, -120)
    #move from wall
    await robot.Drive.straight(50)
    #turn towards mission
    await robot.Drive.turn(91)
    #drive to mission
    await robot.Drive.straight(280) 
    await wait(50)
    #bring attatchment down to hook mission
    robot.Right_attach.dc(-75)
    await wait(250)

    # drive back and lift right arm up
    robot.Right_attach.stop()
    await robot.Drive.straight(-160)
    await robot.Right_attach.run_angle(200, 130)
    await robot.Drive.turn(2)
    await robot.Drive.straight(245)
    robot.Left_attach.dc(-80)
    await wait(300)
    robot.Left_attach.dc(10)
    await wait(300)
    # await robot.Left_attach.run_angle(200, -70*-0.77)
    # await robot.Left_attach.run_angle(200, 70*-0.77)
    # drive back home
    await robot.Drive.straight(-500)

