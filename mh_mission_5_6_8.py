from pybricks.tools import wait

async def run_3(robot):
    print("Starting Run: " + __name__)
 
    await robot.Drive.straight(430)
  
    # robot.Right_attach.dc(-60)
    # await wait(500)
    # await robot.Right_attach.run_angle(500,85) #hammer  up
    # robot.Right_attach.dc(-60)
    # await wait(500)
    # await robot.Right_attach.run_angle(500,85) #hammer up
    # robot.Right_attach.dc(-60)
    # await wait(500)
    # await robot.Right_attach.run_angle(500,120) #hammer up
   #  await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
   #  await robot.Right_attach.run_angle(500,85) #hammer up

   #  #continue to mission 5 and 6 (this version does not push the boulders back)
    await robot.Drive.straight(-104)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(70)
    await robot.Drive.turn(90)
    await robot.Drive.straight(340) 
    await robot.Drive.turn(45)
    await robot.Drive.straight(75) #reach the Boulder station
    robot.Drive.settings(turn_rate=150)   #to get the boulders down 
    await robot.Drive.turn(-39)        #flip the red lever
    robot.Drive.settings(turn_rate=160)

    await robot.Drive.turn(-20) #align to reach who lives there
    await robot.Drive.straight(-25) #moving straight for who lives there and try to push the lever
    await robot.Right_attach.run_angle(500,-80) #put the hammer down
    await robot.Right_attach.run_angle(500,20)
    await robot.Drive.straight(80) # here is where the hammer reaches the who lives there
    await robot.Right_attach.run_angle(500,-30)
    robot.Drive.settings(turn_rate=50)
    await robot.Drive.turn(-50)  
    robot.Drive.settings(turn_rate=150)   
    # await robot.Drive.straight(-40) 
    
    #continue to mission Tip the scales and whats on scale
    await robot.Drive.straight(20) # move towards 
    await robot.Right_attach.run_angle(360,70) # life the arm up
    await robot.Drive.turn(-10)
    await robot.Drive.straight(550)
    await robot.Drive.turn(-130)
    await robot.Drive.straight(40)
    await robot.Right_attach.run_angle(500,-60) # hammer the Tip Scales
    await robot.Drive.turn(-30)
    await robot.Drive.straight(-40)
    await robot.Right_attach.run_angle(500,70)
    await robot.Right_attach.run_angle(500,-80)
    # await robot.Drive.turn(-20)
    await robot.Drive.straight(200) #whats on scale
    await robot.Right_attach.run_angle(500,70)
    await robot.Drive.straight(-100)




#     await robot.Drive.straight(55)
#     await robot.Drive.turn(-115)     #turn an angle to align and push the boulders back
#     #await robot.Drive.straight(-263) #push the boulders back
#    # await robot.Drive.turn(-8)
#     #await robot.Drive.straight(310)  
#     await robot.Drive.turn(120)
#     await robot.Drive.straight(125) #reach the who lives here area
#     robot.Drive.settings(turn_rate=30)
#     await robot.Drive.turn(-39) #flip the red lever
#     robot.Drive.settings(turn_rate=160) #reset the turn rate


   # # robot.Drive.straight(590)
   # #  await robot.Drive.straight(200)
   # #  await robot.Drive.turn(12)
   # #  await robot.Drive.straight(500)
   # #  await robot.Drive.turn(35)
   # #  robot.Drive.settings(straight_speed=500)
   # #  await robot.Drive.straight(-370)
   # #  await robot.Drive.straight(230)
   # #  await robot.Drive.turn(-60)
   # #  await robot.Drive.straight(890)
   # #  await robot.Drive.turn(-75)
   # #  await robot.Drive.straight(640)
   