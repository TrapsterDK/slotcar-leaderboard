"""
Entry Point to The App
"""

import logging
import os
import eel
from camera import VideoCamera
import base64

feed = True

def gen(camera):
    while feed:
        frame = camera.get_frame()
        yield frame


@eel.expose
def video_feed():
    global feed
    feed = True

    x = VideoCamera()
    y = gen(x)
    for each in y:
        print(1)
        # Convert bytes to base64 encoded str, as we can only pass json to frontend
        blob = base64.b64encode(each)
        blob = blob.decode("utf-8")
        eel.updateImageSrc(blob)()
        # time.sleep(0.1)
    print(2)

@eel.expose
def stop_feed():
    global feed 
    feed = False

@eel.expose
def text_set(text):
    eel.add_text(text + "ADD")()

if __name__ == "__main__":
    # Set logging level
    logging.basicConfig(level=logging.INFO)

    # Set web files folder
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    eel.init(web_dir)

    # Start the app
    eel.start('index.html', size=(800, 600))