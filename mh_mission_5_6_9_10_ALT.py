from pybricks.tools import wait

async def run_3(robot):
  print("Starting Run: " + __name__)
  #robot.Drive.settings(straight_speed=100) # slow speed for testing

  #await robot.Drive.straight(430)
    
  #Mission Silo 8
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
    # await robot.Drive.straight(-104)
    # await robot.Drive.turn(-90)
    # await robot.Drive.straight(70)
    # await robot.Drive.turn(90)
  await robot.Drive.straight(660) 
  await robot.Drive.turn(45)
  await robot.Drive.straight(70) #reach the Boulder station
  robot.Drive.settings(turn_rate=150)   #to get the boulders down 
  await robot.Drive.turn(-39)        #flip the red lever
    
  robot.Drive.settings(turn_rate=160)
  await robot.Drive.turn(-20) #align to reach who lives there
  await robot.Drive.straight(-15) #moving straight for who lives there and try to push the lever
  
  await robot.Right_attach.run_angle(500,-70)
  await robot.Right_attach.run_angle(500,70)
  #await wait(500)
  await robot.Drive.straight(20)
  await robot.Drive.turn(-35)
  await robot.Drive.straight(100)
  await robot.Drive.turn(55)
  await robot.Drive.straight(-150)
  await robot.Drive.turn(10)
  await robot.Drive.straight(160)    #reach the who lives there station
  robot.Drive.settings(turn_rate=60)
  await robot.Drive.turn(-40)            #flip the who lives there red lever
  robot.Drive.settings(turn_rate=160)
  await robot.Drive.straight(-110)

  await robot.Drive.turn(-40)  
  await robot.Drive.straight(600) 

  await robot.Drive.turn(-140)
  await robot.Drive.straight(40)
  await robot.Right_attach.run_angle(500,-70) # hammer the Tip Scales
  await robot.Drive.turn(-20)
  await robot.Drive.straight(-40)

  await robot.Right_attach.run_angle(500,80)
  await robot.Right_attach.run_angle(500,-90) #bring the hammer down to Whats on Sale
  
  await robot.Drive.straight(200) #whats on scale
  await robot.Drive.straight(-40)
  await robot.Right_attach.run_angle(500,70)
  await robot.Drive.straight(-70)

  #return to base
  await robot.Drive.turn(-40)
  await robot.Drive.straight(270)
  await robot.Drive.turn(60)
  await robot.Drive.straight(700)



