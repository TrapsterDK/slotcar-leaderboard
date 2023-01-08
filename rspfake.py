from threading import Thread
from time import sleep
import keyboard

def RP_setup():
    pass

def RP_thread(start_input_callback, pass_input_callback):
    while True:
        if keyboard.read_key() == "q":
            print("start_q")
            start_input_callback()
        if keyboard.read_key() == "w":
            print("pass_w")
            pass_input_callback()

def RP_callback(start_input_callback, pass_input_callback):
    t = Thread(target=RP_thread, args=(start_input_callback, pass_input_callback))
    t.start()

def RP_cleanup():
    pass