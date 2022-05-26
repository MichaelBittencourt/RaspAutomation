import time
import wiringpi

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

position = 100
limitUp = 250
limitDown = 100

while True:
    character = getch()
    value = 0
    if character == 'h':
        value = 1
    elif character == 'l':
        value = -1
    elif character == 'q':
        exit(0)
    
    if value != 0:
        oldPosition = position
        position = position + value
        position = limitUp if position > limitUp else limitDown if position < limitDown else position
        print("will show position: ", position)
        if oldPosition != position:
            wiringpi.pwmWrite(18, position)
    #for pulse in range(100, 250, 1):
    #    wiringpi.pwmWrite(18, pulse)
    #    time.sleep(delay_period)
    #for pulse in range(250, 100, -1):
    #    wiringpi.pwmWrite(18, pulse)
    #    time.sleep(delay_period)
