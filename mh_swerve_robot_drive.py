from pybricks.tools import wait
from mh_controllers import StartPID

# Method Move(amount='0,0', unit='xy', speed=60, direction=lastDirection, chassis=lastChassis, directionCurve=True, chassisCurve=True)
#   Parameters:
#       amount - Stop Condition Amount. Default: '0,0'
#       unit - Stop Condition Unit. Default: 'xy'
#       speed - Movement Speed. Default: 60
#       direction - Movement/Wheel Direction. Default: lastDirection
#       chassis - Chassis Angle. Default: lastChassis
#       directionCurve - Smooth Transition to new Direction.  False = Turn then go Straight.  Default: True
#       chassisCurve - Smooth Transition to new Direction.  False = Rotate Chassis before muvement.   Default: True
#
#Passing wheel or chassis angle as as string invokes relative changes.

async def SwerveMove(robot,**keywordArgs):
    # Local Variable =     Passed Keyword Value.  If value is None, use this default value
    amount=         robot.FixNone(keywordArgs.get('amount')         ,'0,0')
    unit=           robot.FixNone(keywordArgs.get('unit')           ,'xy')
    speed=          robot.FixNone(keywordArgs.get('speed')          ,60)
    direction=      robot.FixNone(keywordArgs.get('direction')      ,robot.wheelAngle + robot.chassisAngle)
    chassis=        robot.FixNone(keywordArgs.get('chassis')        ,robot.chassisAngle)
    directionCurve= robot.FixNone(keywordArgs.get('directionCurve') ,True)
    chassisCurve=   robot.FixNone(keywordArgs.get('chassisCurve')   ,True)
    #If values are strings, treat as relative changes
    lastChassis = robot.chassisAngle
    # print('direction', direction,'lastChassis',lastChassis,'chassis',chassis)
    #Compass cardinal & intercardinal/ordinal directions
    compass_rose = {"N":0, "NE":45, "W":90, "SE":135, "S":180, "SW":225, "E":270, "NW":315}
    if direction in compass_rose:
        direction = compass_rose[direction]
    if chassis in compass_rose:
        chassis = compass_rose[chassis]
    # print('direction', direction,'lastChassis',lastChassis,'chassis',chassis)
    if isinstance(direction, str):
        direction = robot.wheelAngle + int(direction)
    else:
        # Implement Field Oriented Targets without constant Gyro Lock
        direction = direction - robot.chassisAngle

        # Identify target new target wheel Angle
        direction = robot.wheelAngle + await robot.closest_rotation(robot.wheelAngle, direction)

    if isinstance(chassis, str):
        chassis = robot.chassisAngle + int(chassis)
    else:
        # Implement Field Oriented Chassis relative diregrees and find shortest path
        # Use string relative path to control rotation direction
        ChassisDiff = (chassis % 360) - (robot.chassisAngle % 360) 
        if ChassisDiff > 180:
            ChassisDiff -= 360
        elif ChassisDiff < -180:
            ChassisDiff += 360
        chassis = robot.chassisAngle + ChassisDiff


    direction = direction + lastChassis - chassis
    if(robot.config['debug']):
        print('[SwerveMove]Effective direction', direction, 'lastChassis', lastChassis, 'chassis', chassis, 'directionCurve', directionCurve,'chassisCurve', chassisCurve)

    # Change the Starting Wheel and Chassis Direction if requested
    if not directionCurve or not chassisCurve:
        turnDirection = direction
        turnChassis = chassis if not chassisCurve else robot.chassisAngle
        await robot.SwerveTurn(turnDirection, turnChassis)
    
    # Move Robot if requested
    if unit == 'reflect' or (unit in ['degrees','cm','in','rotations','seconds','angle'] and abs(amount) > 0):
        await robot.SwerveDrive(amount, unit, speed, direction,chassis)


async def SwerveTurn(robot, direction, chassis):
        if(robot.config['debug']):
            print('[SwerveTurn] direction', direction, 'chassis', chassis)
        if robot.chassisAngle != chassis:
            await robot.setDirectionCorrection(0)

            await wait(200)
            condition = robot.StopConditionSet(chassis - robot.gyro.heading(), 'angle')
            robot.chassisAngle = chassis
            while (not await robot.StopConditionCheck(condition)):
                await wait(50)
        await robot.setDirectionCorrection(direction)
        await wait(300)

async def SwerveDrive(self, amount=999999, unit='cm', speed=60, newDirection=None, newChassis=None):
    if(self.config['debug']):
        print('[SwerveDrive] amount', amount, 'unit', unit, 'newDirection', newDirection, 'newChassis', newChassis)
    startChassis = self.chassisAngle
    startDirection = self.wheelAngle

    #Calculate Drive Speed
    speed = speed * 22 #Speed values are out of 1100+ not 100
    if unit in ['cm','in','degrees','rotations'] and amount < 0:
        speed = speed * -1
    #self.driveSpeed = speed #Static Speed, Replacing with acceleration/deceleration

    speedPID = StartPID([abs(speed)*self.config['drive']['pid'][0], self.config['drive']['pid'][1], self.config['drive']['pid'][2]]) # [Kp, Ki, Kd]
    condition = self.StopConditionSet(amount, unit)
    while (not await self.StopConditionCheck(condition)):
        progress = condition['progress']
        speedCorrection = speedPID.update(abs(progress-0.5))
        newSpeed = min(max(self.config['drive']['minSpeed'], abs(speed)-speedCorrection), self.config['drive']['maxSpeed'])
        if speed < 0:
            newSpeed *= -1
        self.driveSpeed = newSpeed

        self.chassisAngle = startChassis + ((newChassis - startChassis)  * progress)
        await self.setDirection(startDirection + ((newDirection - startDirection) * progress))
        await wait(25)
    
    # Just in case Progress != 100%
    self.chassisAngle=newChassis
    await self.setDirection(newDirection)
    self.driveSpeed=0

async def SwerveStart(self,resetGyro=False):
    if resetGyro:
        await wait(50)
        self.gyro.reset_heading(0)
        self.chassisAngle = 0
    #print('starting angle', measurements, self.chassisAngle)
    self.runAttachment = False

async def SwerveStop(self):
    #Consider changing this to a loop to repeat for a time
    self.runAttachment = True
    await wait(100)
    self.driveSpeed=0
    self.rightTurn.hold()
    self.leftTurn.hold()
    self.leftDrive.hold()
    self.rightDrive.hold()

async def closest_rotation(self, currentAngle, targetAngle):
    # Normalize the angles to be within 0 - 360
    def normalize_angle(angle):
        return angle % 360

    currentAngle = normalize_angle(currentAngle)
    if self.reverseWheels == -1:
        targetAngle = normalize_angle(targetAngle+180)
    else:
        targetAngle = normalize_angle(targetAngle)

    # Calculate the difference between normalized angles
    difference = targetAngle - currentAngle
    
    # Normalize the difference to be within -180 - 180
    if difference > 180:
        difference -= 360
    elif difference < -180:
        difference += 360

    return difference

async def setDirection(self, targetAngle):
    newAngleDelta = await self.closest_rotation(self.wheelAngle, targetAngle)

    # Normalize the difference to be within -90 - 90 and reverse wheel direction if needed
    if newAngleDelta > 90:
        newAngleDelta -= 180
        self.reverseWheels *= -1
    if newAngleDelta < -90:
        newAngleDelta += 180
        self.reverseWheels *= -1

    self.wheelAngle = self.wheelAngle + newAngleDelta

async def setDirectionCorrection(self, targetAngle):
    newAngleDelta = await self.closest_rotation(self.wheelAngle, targetAngle)

    # Normalize the difference to be within -90 - 90 and reverse wheel direction if needed
    if newAngleDelta > 90:
        newAngleDelta -= 180
        self.reverseWheels *= -1
    if newAngleDelta < -90:
        newAngleDelta += 180
        self.reverseWheels *= -1

    await self.TurnSwerveWheels(self.wheelAngle + newAngleDelta)
