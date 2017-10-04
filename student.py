import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 140
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 140
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        if __name__ == '__main__':
            while True:
                self.stop()
                self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):

        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")

        ##### WRITE YOUR FIRST PROJECT HERE

        if(self.safety_check):
             self.to_the_right()
             self.stanky_leg()
             self.moonwalk()
             self.to_the_left()
             self.headbob()

    def to_the_right(self):
        for x in range(1):
            self.servo(30)
            self.encR(80)
            self.encR(80)


    def to_the_left(self):
        for x in range(1):
            self.servo(130)
            self.encL(80)
            self.encL(80)


    def backwards(self):
        for x in range(1):
            self.servo(130)
            self.servo(25)
            self.encB(40)
            self.encF(40)

    def stanky_leg(self):
        for x in range(1):
            self.encL(90)
            self.encR(90)


    def headbob(self):
         for x in range(1):
             self.servo(25)
             self.servo(150)

    def moonwalk(self):
        for x in range(1):
            self.backwards()
            self.encL(16)
            self.encR(16)
            self.stop()


    @property
    def safety_check(self):
        for x in range(4):
            self.servo(self.MIDPOINT) # look straight ahead
            for loop in range(4):
                if not self.is_clear():
                    print("not working")
                    return False
                print("nCheck#%d" % loop + 1)
                self.encR(8)
            print("safe to dance")
            return True





            # turn 90 degree
            # scan again
            # loop 3 times





    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")


    ####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
