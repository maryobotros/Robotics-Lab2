from pycreate2 import Create2
import time


def main():
    port = "COM3"  # The port to connect to the Create2
    bot = Create2(port)
    bot.start()  # Start the Create2
    bot.safe()  # Put the Create2 into 'safe' mode so we can drive it, still provides protection
    num_of_turns = 0

    while num_of_turns < 4: # Our main condition is based on number of turns, we assume a 4 sided wall
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
        if lb_front_right >= 800:  # Case: Wall corner turn
            print("Wall detected, Now turn left")
            print("lb left: " + str(lb_left))
            print("lb front left: " + str(lb_front_right))
            print("lb center left: " + str(lb_center_left))
            bot.drive_direct(0, 0)
            while lb_left > 20 or lb_center_left > 20 or lb_front_left > 20:
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
            num_of_turns += 1
            print("Number of turns: " + str(num_of_turns))
        elif lb_right < 500 and lb_right > 60: # Keep going straight if in sweet spot
            print("lb Right: " + str(lb_right))
            bot.drive_direct(40, 40)
        elif lb_right <= 60: # Going to far away from wall
            bot.drive_direct(-15, 15)  # Turn right
            time.sleep(1)
        elif lb_right >= 500: # Going too close to wall
            print("small turn: " + str(lb_center_right))
            bot.drive_direct(15, -15)

    bot.stop()
    bot.close()


main()

"Comment"