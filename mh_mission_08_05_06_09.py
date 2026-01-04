from pybricks.tools import wait, multitask


#Completing missions 5 and 6 in one motion



async def run_6(robot):
  print("Starting Run: " + __name__)

  await multitask(robot.Right_attach.run_angle(300, 78), wait(850), race=True)
  await multitask(robot.Left_attach.run_angle(300, 78), wait(850), race=True)

  robot.Drive.settings(straight_speed=250, turn_rate=160)
  await robot.Drive.straight(420)
  
  #Completing Silo
  print(robot.gyro.heading())
  await robot.Right_attach.run_angle(500, -200) #hammer down
  await robot.Right_attach.run_angle(500,130) #hammer  up
  
  await robot.Right_attach.run_angle(500,-130) #hammer down
  await robot.Right_attach.run_angle(500,130) #hammer up

  await robot.Right_attach.run_angle(500,-130) #hammer down
  await robot.Right_attach.run_angle(500,155) #hammer up
  #await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
  #await robot.Right_attach.run_angle(500,85) #hammer up
  robot.Drive.settings(straight_speed=300)


  #Completing the Forge:
  #Going to the Forge
  await robot.Drive.turn(-45)
  await robot.Drive.straight(50)
  await robot.Drive.turn(45)
  await robot.Drive.straight(220) #reach the Boulder station
  await robot.Drive.turn(-6)
  await robot.Drive.straight(16)
  await robot.Right_attach.run_angle(500, 30)
  await robot.Right_attach.run_angle(500,-120) #Complete the Forge
  await robot.Right_attach.run_angle(500,100)
  await robot.Right_attach.run_angle(500,-100)
  await wait(500)
  
  #Completing Who Lives There:
  await robot.Drive.turn(-20) #Setting up to complete Who Lives There
  await multitask(robot.Right_attach.run_angle(500,-100), wait(700), race=True) #Resetting Wheel Arm
  await robot.Right_attach.run_angle(500,95) #Picking up arm to lever
  await wait(200)
  await robot.Drive.straight(50)
  robot.Drive.settings(turn_rate=80)
  await robot.Drive.turn(-30) #Completing Who Lives There
  await multitask(robot.Drive.straight(10), wait(700), race=True)
  await robot.Drive.turn(10)
  robot.Drive.settings(turn_rate=160)
  await robot.Drive.straight(-50)
  await robot.Right_attach.run_angle(500, 90)
  await robot.Drive.turn(-95)

  #Raising the Market Wares:
  await robot.Drive.straight(130) #Heading to What's on Sale
  await robot.Right_attach.run_angle(500,-180)
  await wait(500)
  await robot.Drive.straight(60) #Completing the market ware

  #Tip the Scales and Rasing Ceiling:
  await robot.Right_attach.run_angle(500,180)
  await robot.Drive.straight(-80)
  await robot.Drive.turn(-25)
  await robot.Drive.straight(180)
  await robot.Drive.turn(122)
  await robot.Drive.straight(40)
  await robot.Left_attach.run_angle(500,-170) #Tipping the Scale and grabbing ceiling
  await wait(800)
  await robot.Drive.straight(-210) #Bringing ceiling up
  await robot.Drive.straight(80)
  await robot.Left_attach.run_angle(500,60) #Releasing ceiling
  await wait(300)
  await robot.Left_attach.run_angle(500,90) #Releasing ceiling
  await wait(300)
  await robot.Drive.straight(-20) #Backing up after raising ceiling
  await robot.Drive.turn(-45) # Turning towards Scale Pan
  await robot.Drive.straight(80) #Driving to Scale Pan
  await robot.Drive.turn(30)
  await robot.Drive.straight(-20)
  await robot.Left_attach.run_angle(500,-90) #Grabbing Scale Pan
  await wait(100)
  await robot.Drive.turn(-30)
  await robot.Drive.straight(-150) #Bringing Scale Pan up
  await robot.Drive.turn(-135)
  await robot.Drive.straight(200) #Driving to home area

  # await robot.Drive.straight(-480)
  # await robot.Left_attach.run_angle(500,-75)#lift up arm after lifting up the celling