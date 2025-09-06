class StartPID:
    def __init__(self, pid=[1,0,0]):
        self.integral = 0
        self.lastError = 0
        self.Kp = pid[0]
        self.Ki = pid[1]
        self.Kd = pid[2]

    def update(self, error):
        pFix = error * self.Kp
        self.integral = self.integral + error # Problem: Integral Windup - https://en.wikipedia.org/wiki/Integral_windup
        iFix = self.integral * self.Ki
        derivative = error - self.lastError
        dFix = derivative * self.Kd
        self.lastError = error
        correction = pFix + iFix + dFix
        return correction
