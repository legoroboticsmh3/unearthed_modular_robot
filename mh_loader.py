from pybricks.tools import wait, multitask
from pybricks.parameters import Button, Color

async def loader(robot,runs=[]):
    #robot.hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))
    robot.hub.system.set_stop_button(Button.BLUETOOTH)
    programID = 0  #Start on First Program (Displays as 1 instead of zero)
    maxProgramID = max(0,len(runs)-1)
    robot.light.on(Color.GREEN)

    lastPressed = [] #Used for Button Release Detection
    while True:
        pressed = robot.buttons.pressed()

        #When Center Button is Released
        if Button.CENTER in lastPressed and Button.CENTER not in pressed:
            # Code Running
            robot.light.on(Color.RED)
            if type(runs[programID]) == list:
                    for run in runs[programID]:
                        #Run until completion or Center Button Pressed
                        await multitask(run(robot),robot.cancelRun(), race=True)
            else:
                    #Run until completion or Center Button Pressed
                    await multitask(runs[programID](robot),robot.cancelRun(), race=True)
                # Code Complete
            robot.light.on(Color.GREEN)
            programID += 1

        #When Right Button is Released
        if Button.RIGHT in lastPressed and Button.RIGHT not in pressed:
            programID += 1

        #When Left Button is Released
        if Button.LEFT in lastPressed and Button.LEFT not in pressed:
            programID -= 1

        #Wrap Arround Left & Beep
        if programID < 0:
            programID = maxProgramID
            await robot.speaker.beep()
        
        #Wrap Arround Right & Beep
        if programID > maxProgramID:
            programID = 0
            await robot.speaker.beep()
        
        #In Code, Lists start with 0 however add one and display as program id
        robot.display.number(programID+1)
        await wait(50)
        lastPressed = pressed # Used for Button Release Detection

