from pybricks.tools import wait, multitask


#Completing missions 5 and 6 in one motion
###WORKING VERSION, DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING.



async def run_6(robot):
  print("Starting Run: " + __name__)

  robot.Drive.use_gyro(True)
  await multitask(robot.Right_attach.run_angle(300, 78), wait(300), race=True)
  await multitask(robot.Left_attach.run_angle(300, 78), wait(300), race=True)

  robot.Drive.settings(straight_speed=600, turn_rate=160)
  await robot.Drive.straight(420)
  
  #Completing Silo
  print(robot.gyro.heading())
  
  await multitask(robot.Right_attach.run_angle(200, -250), wait(800), race=True) #hammer down
  await robot.Right_attach.run_angle(500,130) #hammer  up
  
  await robot.Right_attach.run_angle(500,-130) #hammer down
  await robot.Right_attach.run_angle(500,130) #hammer up

  await robot.Right_attach.run_angle(500,-130) #hammer down
  await robot.Right_attach.run_angle(500,155) #hammer up
  robot.Drive.settings(straight_speed=300)


  #Completing the Forge and who lived here
  await robot.Drive.turn(-45)
  await robot.Drive.straight(150)
  await robot.Drive.turn(45)
  await robot.Drive.straight(200) #reach the Boulder station
  await robot.Right_attach.run_angle(500,-150) #hammer down
  await robot.Drive.turn(30)#turming to complete the forge
  await robot.Drive.turn(-50)# completing who lived heere    

  #Raising Market Wares:
  await robot.Drive.straight(-105)#come back from the who lived here
  await robot.Right_attach.run_angle(500,150)#hammer up
  await robot.Drive.straight(-15)#backing up to have space for turning
  await robot.Drive.turn(-110)#turning to face the market wares
  await robot.Drive.straight(43)#going to the market wares
  await robot.Right_attach.run_angle(250,-180) #place hammer into market waresssss
  await wait(300)
  await robot.Drive.straight(40) #Moving forward to raise market wares

  #Tip the Scales and Rasing Ceiling:
  await robot.Right_attach.run_angle(500,180) #lifting up hammmer from market wares 
  await robot.Drive.straight(-70) #backing up from market wares
  await robot.Drive.turn(-25) #setting up for ceiling and scale
  await robot.Drive.straight(160) #moving towards scale and ceiling area
  await robot.Drive.turn(110)#Facing the scale and ceiling
  await robot.Drive.straight(45) #going to scale and ceiling
  await robot.Left_attach.run_angle(500,-210) #Slamming Tipping the Scale and grabbing ceiling
  await wait(300)
  await robot.Drive.straight(-155) #Bringing ceiling up was -180
  await robot.Right_attach.run_angle(500,20)
  await robot.Drive.straight(50)
  await robot.Left_attach.run_angle(500,150) #Releasing ceiling

  await robot.Drive.straight(-20) #Backing up after raising ceiling
  await robot.Drive.turn(-45) # Turning towards Scale Pan
  await robot.Drive.straight(110) #Driving to Scale Pan
  await robot.Drive.turn(23)#Turning toward scale pan
  await robot.Drive.straight(-21)

  await wait(300)
  robot.Left_attach.dc(-70)
  await wait(200)
  robot.Left_attach.dc(-30)
  await wait(1000)
  await robot.Drive.turn(-15)
  await robot.Drive.straight(-400) #Bringing Scale Pan home
  await robot.Drive.turn(-80)#going to home area
  robot.Drive.settings(straight_speed=250, turn_rate=160) # Reset the straight_speed back.