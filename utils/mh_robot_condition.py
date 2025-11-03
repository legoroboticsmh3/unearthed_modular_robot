#from umath import pi

def StopConditionSet(self, amount=999999, unit='cm', startAngle=None):
    #self.leftDrive.reset_angle(0)
    #self.gyro.reset_heading(0)
    seconds = 0
    degrees = 0
    reflect = 0
    angle   = 0
    #circumference = self.config['drive']['diameter']*self.config['drive']['gearRatio']*pi
    if unit == 'degrees':
        degrees = amount
    if unit == 'cm':
        degrees = int(amount * 10 * (360/self.config['drive']['circumference']))
    if unit == 'in':
        degrees = int(amount * (360/(self.config['drive']['circumference']/25.4)))
    if unit == 'rotations':
        degrees = int(amount * 360)
    if unit == 'seconds':
        seconds = amount*1000
    if unit == 'reflect':
        reflect = amount
    if unit == 'angle':
        angle = amount
    return {
        'degrees':  degrees,
        'seconds':  seconds,
        'reflect':  reflect,
        'angle':    angle,
        'startSeconds': self.timer.time(),
        'startDegrees': self.leftDrive.angle(),
        'startAngle':   self.FixNone(startAngle,self.gyro.heading()),
        'progress':0
    }

async def StopConditionCheck(self, condition):
    #Measure how many degrees we have traveled
    if abs(condition['degrees']) > 0:
        degrees = abs(self.leftDrive.angle()-condition['startDegrees'])
        condition['progress'] = degrees/abs(condition['degrees'])
        if degrees < abs(condition['degrees']):
            return False

    #Measure how many seconds have passed
    if condition['seconds'] > 0:
        seconds = self.timer.time() - condition['startSeconds']
        condition['progress'] = seconds/condition['seconds']
        if (seconds < condition['seconds']):
            return False

    #Wait for Black Line
    if condition['reflect'] == 'black':
        #maximum Accelerate to 80% max speed and stay there (assumes PID max speed at 50%)
        condition['progress'] = min(.5, condition['progress'] + .1)
        if await self.reflectSensor.reflection() > self.config['line']['black']:
            return False

    #Wait for White Line
    if condition['reflect'] == 'white':
        #maximum Accelerate to 80% max speed and stay there (assumes PID max speed at 50%)
        condition['progress'] = min(.5, condition['progress'] + .1)
        if await self.reflectSensor.reflection() > self.config['line']['white']:
            return False
    
    #Wait until target angle is reached
    if abs(condition['angle']) > 0:
        #accelerate to 100% max speed
        condition['progress'] = min(.5, condition['progress'] + .1)
        if abs(self.gyro.heading()-condition['startAngle']) < abs(condition['angle']):
            return False

    #One or more conditions above were met, return True to exit while loop
    return True
