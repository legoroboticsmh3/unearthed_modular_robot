from pybricks.parameters import Direction, Port

CONFIG = {
    'debug':            False,


    'drive':{
        'speed':        500,
        'minSpeed':     1,
        'maxSpeed':     1000,
        'diameter':     62.4, #mm 56 (small spike wheel) or 195.9 (wheel 32019), 24mm (Small white wheel), 30 (Wedge Belt Wheel)
        'width':        110, #mm Distance between the centers of the two wheels
        'left':         [Port.F,Direction.COUNTERCLOCKWISE, [12, 20]],#switched numbers
        'right':        [Port.E,Direction.CLOCKWISE, [12, 20]],
        'pid':          [1.7,0,0],
       
    },
    'attach': {
        'speed':        20,
        'left':         [Port.B, [24, 16]], # Previous 28, 20
        'right':        [Port.A, [24, 16]], # Previous 28, 20
        
    },
    'line': {
        'enable':       False,
        'speed':        60,
        'black':        32,
        'white':        95,
        'left':         Port.D,
        'right':        Port.C,
        'pid':          [.65,0,0],
    },
}

'''
P – Proportional: “How big is the error right now?”

Big error → big push.

Small error → small push.

This makes the robot respond quickly, but if P is too big, it overshoots and wiggles past the target.

I – Integral: “Have we been wrong for a long time?”

If the robot is always a little off (like it always stops just short), I slowly adds more push to fix that “stuck” error.

Too much I can make the robot start to swing back and forth.

D – Derivative: “Where is the error heading?”

D watches how fast the error is changing.

If you’re racing toward the target, D says “Slow down, you’re coming in too hot!”

This helps reduce overshoot and makes motion smoother.

The controller adds these three parts together to decide the motor power:

P = react to the now

I = remember the past

D = predict the future
'''