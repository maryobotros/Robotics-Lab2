from pycreate2 import packets, create2api, Create2
import time


def main():
    port = "COM3"  # The port to connect to the Create2
    bot = Create2(port)
    bot.start()  # Start the Create2
    bot.safe()  # Put the Create2 into 'safe' mode so we can drive it, still provides protection

    while True: # This code does not have an end condition for which the robot stops once it completes the maze
        sensors = bot.get_sensors()
        lb_left = sensors[36]
        lb_center_left = sensors[38]
        lb_front_left = sensors[37]
        lb_right = sensors[41]
        lb_center_right = sensors[39]
        lb_front_right = sensors[40]
        print("Front Right Bumper: " + str(lb_front_right))
        print("Front Center Right: " + str(lb_center_right))
        print("Right Bumper" + str(lb_right))
        print("Left Bumper" + str(lb_left))
        if lb_front_right >= 800:  # Wall corner turn
            print("Wall detected, Now turn left")
            print("lb left: " + str(lb_left))
            print("lb front left: " + str(lb_front_right))
            print("lb center left: " + str(lb_center_left))
            bot.drive_direct(0, 0)
            while lb_left > 20 or lb_center_left > 20 or lb_front_left > 20:  # How long to make the turn
                print("turning")
                sensors = bot.get_sensors()
                lb_left = sensors[36]
                lb_center_left = sensors[38]
                lb_front_left = sensors[37]
                print("lb left: " + str(lb_left))
                print("lb front left: " + str(lb_front_left))
                print("lb center left: " + str(lb_center_left))
                bot.drive_direct(15, -15)
                time.sleep(1)
        elif lb_right < 500 and lb_right > 60 and lb_center_right != 0:  # Keep going straight, not a special corner turn
            print("lb Right: " + str(lb_right))
            bot.drive_direct(40, 40)
        elif lb_right <= 60:
            if lb_right == 0:  # Case of a special corner turn
                while lb_right < 60:  # How long the robot to turn until it detects the wall to continue hugging
                    sensors = bot.get_sensors()
                    lb_right = sensors[41]
                    print("special corner turn LB RIGHT: " + str(lb_right))
                    bot.drive_direct(0, 70)  # It continuously moves forward as it turns to "smoothly" hug the corner
                    time.sleep(1)
                    bot.drive_direct(40, 40)
                    time.sleep(1)
            else:  # Small adjustment turn when too far away from wall
                sensors = bot.get_sensors()
                lb_right = sensors[41]
                print("small turn LB RIGHT: " + str(lb_right))
                bot.drive_direct(-15, 15)
                time.sleep(1)
                bot.drive_direct(40, 40)
                time.sleep(1.3)

        elif lb_right >= 500 and lb_center_right > 0: # Going too far away from wall
            print("adjustment left turn called: " + str(lb_right))
            bot.drive_direct(20, -20)
            time.sleep(1)

    bot.stop()
    bot.close()


main()
