from pybricks.parameters import Direction, Port

CONFIG = {
    'debug':            False,


    'drive':{
        'speed':        500,
        'minSpeed':     1,
        'maxSpeed':     1000,
        'diameter':     62.4, #mm 56 (small spike wheel) or 195.9 (wheel 32019), 24mm (Small white wheel), 30 (Wedge Belt Wheel)
        'width':        110, #mm Distance between the centers of the two wheels
        'left':         [Port.F,Direction.CLOCKWISE, [28, 20]],
        'right':        [Port.E,Direction.COUNTERCLOCKWISE, [28, 20]],
        'pid':          [1.7,0,0],
       
    },
    'attach': {
        'speed':        20,
        'left':         [Port.A, [28, 36]],
        'right':        [Port.B, [20, 28]],
        
    },
    'line': {
        'enable':       False,
        'speed':        60,
        'black':        32,
        'white':        95,
        'left':         Port.E,
        'right':        Port.F,
        'pid':          [.65,0,0],
    },
}

