
#sudo apt-get install rpi.gpio
#pip install rpi.gpio
import RPi.GPIO as GPIO

#https://learn.sparkfun.com/tutorials/raspberry-gpio/all
start_input = 17
pass_input = 27

def RP_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(start_input, GPIO.IN)
    GPIO.setup(pass_input, GPIO.IN)

def RP_callback(start_input_callback, pass_input_callback):
    GPIO.add_event_detect(start_input, GPIO.RISING, callback=lambda pin: start_input_callback() if GPIO.event_detected(pin) and GPIO.input(pin) == 1 else None, bouncetime=300)
    GPIO.add_event_detect(pass_input, GPIO.RISING, callback=lambda pin: pass_input_callback() if GPIO.event_detected(pin) and GPIO.input(pin) == 1 else None, bouncetime=300)

def RP_cleanup():
    GPIO.cleanup()
