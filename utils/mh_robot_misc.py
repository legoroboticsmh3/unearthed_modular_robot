from pybricks.tools import wait, multitask
from pybricks.parameters import Button, Stop
from .mh_controllers import StartPID

def FixNone(robot, value, fix):
    if isinstance(value, type(None)):
        return fix
    else:
        return value

def WaitButton(robot,button):
    while not button in robot.buttons.pressed():
        wait(10)

def GetTurnAngle(robot,target,startAngle):
    return target - (robot.gyro.heading()-startAngle)

def CounterCalculate(robot,turnAngleChange):
    offsetDistance = ((robot.config['drive']['offCenter_circumference']/360) * turnAngleChange)
    # TODO: Need to address gear ratio for swerve module
    counterDegrees = (((360/robot.config['drive']['circumference']) * offsetDistance) + turnAngleChange)*-1
    return counterDegrees

async def CounterTurnWheel(robot,wheel,wheelAngle, stopOnStall=False):
    if wheel == 'right':
        turnMotor = robot.rightTurn
        driveMotor = robot.rightDrive
        turnOffset=0
    else:
        turnMotor = robot.leftTurn
        driveMotor = robot.leftDrive
        turnOffset= robot.leftTurnOffset
    turnStart = turnMotor.angle()
    driveStart = driveMotor.angle()
    if isinstance(wheelAngle, str):
        wheelAngle = turnStart + int(wheelAngle)
    wheelAngle = wheelAngle+turnOffset
    turnMotor.run_target(900,wheelAngle,wait=False)
    while not turnMotor.done() and (stopOnStall == False or turnMotor.stalled() == False):
        turnCurrent = turnMotor.angle()
        driveCurrent = driveMotor.angle()
        driveError = driveCurrent - (driveStart + robot.CounterCalculate(turnCurrent-turnStart))
        driveMotor.run(driveError*robot.config['drive']['pid'][0]*-50)
        await wait(10)
    turnMotor.hold()
    driveMotor.hold()
    await wait(10)
    return wheelAngle

async def TurnSwerveWheels(robot,wheelAngle=0):
    if isinstance(wheelAngle, str):
        wheelAngle = robot.wheelAngle + int(wheelAngle)
    await robot.SwerveStop()
    await multitask(CounterTurnWheel(robot,'left',wheelAngle), CounterTurnWheel(robot,'right',wheelAngle))
    robot.wheelAngle = wheelAngle
    await robot.SwerveStart()

def TurnSwerveWheel(self, wheel='right', turnNewAngle=0, speed=900, Wait=True):
    CounterTurnWheel(robot,wheel,turnNewAngle)

async def moveAttachment(robot, attachmentID=1,amount=360,unit="degrees", speed=200,gearRatio=[1,1]):
    degrees = 0
    attachment = 0 if attachmentID == 1 else 180
    degreeCalculator = gearRatio[1]/gearRatio[0] # Driven Gear / Driving Gear
    if unit == 'degrees':
        degrees = int(amount*degreeCalculator)
    if unit == 'rotations':
        degrees = int(amount * 360 * degreeCalculator)

    await robot.SwerveStop()
    #print(robot.leftDrive.control.stall_tolerances()) # 20,200  (not able to reach 20% speed for 200ms)
    startSelectorWheel = robot.rightTurn.angle()   
    await multitask(CounterTurnWheel(robot,'left',attachment), CounterTurnWheel(robot,'right',attachment))
    await CounterTurnWheel(robot,'left',str(degrees), True)
    await multitask(CounterTurnWheel(robot,'left',90+degrees), CounterTurnWheel(robot,'right',90))
    await CounterTurnWheel(robot,'left',str(degrees*-1), True)
    #await TurnSwerveWheels(robot, startSelectorWheel)
    await multitask(CounterTurnWheel(robot,'left',startSelectorWheel), CounterTurnWheel(robot,'right',startSelectorWheel))

    await robot.SwerveStart()

async def cancelRun(robot):
    #When Center button pessed, Stop Run by exiting race
    while not Button.CENTER in robot.buttons.pressed():
        await wait(50)
    #Before Exiting, Stop Motor Movement
    await robot.SwerveStop()