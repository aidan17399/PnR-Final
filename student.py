import pigo
import time  # import just in case students need
import random
import datetime
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
        self.start_time = datetime.datetime.utcnow()
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 20
        self.HARD_STOP_DIST = 20
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 135
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
                "o": ("obstacle count", self.obstacle_count),
                "t": ("test smoothL", self.smoothL),
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

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        outter_counter = 0
        for x in range(1):
            self.wide_scan()
            found_something = False
            inner_counter = 0
            for distance in self.scan:
                if distance and distance < 40 and not found_something:
                    found_something = True
                    inner_counter += 1
                    print("Object # %d found, I think" % inner_counter)
                if distance and distance > 40 and found_something:
                    found_something = False
            print("\n----I SEE %d OBJECTS----\n" % inner_counter)
            outter_counter += inner_counter
        print("\n----IN TOTOAL I SAW %d OBJECTS----\n" % outter_counter)

    def dance(self):

        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")

        ##### WRITE YOUR FIRST PROJECT HERE

        self.wait_for_turn()
        if(self.safety_check()):
             self.to_the_right()
             self.stanky_leg()
             self.moonwalk()
             self.to_the_left()
             self.headbob()

    def safety_check(self):
        self.servo(self.MIDPOINT) # look straight ahead
        if not self.is_clear():
            print("too dangerous to dance")
            return False
        self.encR(8)
        print("safe to dance")
        return True

        # turn 90 degree
        # scan again
        # loop 3 times

    def wait_for_turn(self):
        last_scan = self.dist()
        while True:
            time.sleep(10)
            if self.dist() == last_scan:
                break
            else:
                last_scan = self.dist()
        print("now my turn")

    def to_the_right(self):
        for x in range(1):
            self.servo(30)
            self.encR(80)
            self.encR(80)

    def to_the_left(self):
        for x in range(3):
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
        for x in range(5):
            self.encL(90)
            self.encR(90)

    def headbob(self):
         for x in range(4):
             self.servo(25)
             self.servo(150)

    def moonwalk(self):
        for x in range(8):
            self.backwards()
            self.encL(16)
            self.encR(16)
            self.stop()


            self.encR(10)

    def restore_heading(self):
        """Uses self.turn_track to reorient to original heading"""

        print("restoring heading")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))

    def test_restore_heading(self):
        self.encR(5)
        self.encL(14)
        self.encR(10)
        self.encR(10)
        self.encL(7)
        self.restore_heading()


    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print("It took you %d seconds to run this" % difference)
        while True:
            if self.is_clear():  # no obstacles are detected by the robot
                print("I am going to move forward!")
                self.cruise()  # moves robot forward due to clear path
            else:  # obstacle is detected by the robot
                print("Ut oh! Something is blocking my path!")
                self.encB(8)  # backs up robot if it still cannot find clear path and retests right and left
                self.encR(8)  # turns right to find clear path
                self.encL(16)
                self.restore_heading()
                self.encR(8)
                if self.is_clear():  # clear path found to the right
                    self.cruise()  # robot moves forward in clear direction
                else:
                    self.encL(8)  # turns left to find clear path if no clear path to the right
                    if self.is_clear():  # path is clear
                        self.cruise()  # robot moves forward in clear direction
            self.restore_heading()  # reorients robot to original heading

    def smooth_turn(self):
        self.right_rot()
        start = datetime.datetime.utcnow()
        while True:
            if self.dist() > 100:
                self.stop()
                print("i think i have found a good path")
            elif datetime.datetime.utcnow() - start > datetime.timedelta(seconds):
                self.stop()
                print("i give up")
            time.sleep(2)

    def cruise(self):
        """ drive straight while path is clear"""
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.5)
        self.stop()

    def smoothR(self, x = 100):
        count = 0
        found_it = False
        self.set_speed(100, 100)
        self.right_rot()
        while True:
            if self.dist() > x:
                count += 1
            elif found_it:
                self.stop()
                self.encL(3)
                break
            else:
                count = 0

            if count > 3:
                found_it = True
            time.sleep(.1)
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)


    def smoothL(self, x=100):
        count = 0
        found_it = False
        self.set_speed(100, 100)

        while True:
            self.left_rot()
            if self.dist() > x:
                count += 1
            elif found_it:
                self.stop()
                self.encR(3)
                break
            else:
                count = 0
            if count > 3:
                found_it = True
            time.sleep(.3)
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)


########## STATIC FUNCTIONS


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


