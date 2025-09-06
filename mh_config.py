from pybricks.parameters import Direction, Port

CONFIG = {
    'debug':            False,
    'hub':              'prime', #prime or technic
    'xboxcontroller':{
        'enable':       False,
        'deadzone':     6
    },
    'drive':{
        'speed':        50,
        'minSpeed':     1,
        'maxSpeed':     1200,
        'gearRatio':    12/12,
        'diameter':     43.2, #mm 56 (small spike wheel) or 195.9 (wheel 32019), 24mm (Small white wheel), 30 (Wedge Belt Wheel)
        'left':         [Port.A, Direction.CLOCKWISE],
        'right':        [Port.B, Direction.CLOCKWISE],
        'pid':          [1.7,0,0],
        'offCenter':    7.5, #mm - distance swerve wheel is off from center point of wheel module rotation
    },
    'turn': {
        'speed':        20,
        'left':         [Port.C, Direction.CLOCKWISE, [20, 60]],
        'right':        [Port.D, Direction.CLOCKWISE, [20, 60]],
        'leftZero':     351, #Red 327,40  #yellow 351,45  #white 321,345 #black 303,51
        'rightZero':    45,
        'pid':          [.43,.0015,.15], #was previously .43
        'dGain':        20, # Differential Steering Proportial Controller Gain
        'aGain':        -1.2, # Ackerman/Swerve Steering Proportial Controller Gain
    },
    'line': {
        'enable':       True,
        'speed':        60,
        'black':        32,
        'white':        95,
        'left':         Port.E,
        'right':        Port.F,
        'pid':          [.65,0,0],
    },
}

