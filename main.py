import datetime
import os
import eel
from camera import VideoCamera
import base64
from tkinter import Tk, filedialog

from database import Database, User     
import race

SHOW_TIMES = 3  

# Set web files folder
web_dir = os.path.join(os.path.dirname(__file__), 'web')
last_user_id: int = 0
db: Database = None 


@eel.expose
# file select popup returns the path to the file, "" if no file is selected
def file_select(defaultextension=".db", filetypes=[("Database", "*.db")]):
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file = filedialog.askopenfile(defaultextension = defaultextension, filetypes = filetypes)
    if file:
        return file.name
    return ""
    

def create_users(amount: int) -> None:
    if not amount:
        return
        
    count = db.get_user_count() + 1
    db.add_users([f"Team {count + i}" for i in range(last_user_id, last_user_id + amount)])

@eel.expose
def print_text(text):
    print(text)


def load_database(filename: str = None) -> None:
    global db
    
    # check if filename was given
    if not filename:
        # normal filename for new database  
        filename = f"database_{datetime.datetime.now().strftime('%d-%m-%Y')}.db"
        
        # extend filename if file already exists
        if os.path.exists(filename):
            filename = filename[:-3] + f"_{datetime.datetime.now().strftime('%H-%M-%S')}" + filename[-3:]

    try:
        db = Database(filename)
    except Exception as e:
        raise e


@eel.expose
def setup_leaderboard(database_filename: str, racers: int, max_lap_time_s: int):
    load_database(database_filename)

    try:
        racers = int(racers) if racers else 0
        if max_lap_time_s:
            race.MAX_LAP_TIME_MS = int(max_lap_time_s) * 1000
    except ValueError:  
        raise ValueError("Invalid input")

    create_users(racers)

def get_current_racer() -> User:
    return db.get_user(last_user_id)


if __name__ == "__main__":
    try:
        eel.init(web_dir)

        setup_leaderboard("", 20, 0)

        db.create_fake_data()

        # Start the app
        eel.start('templates/leaderboard.html', jinja_templates='templates', size=(800, 600), block=False, 
            jinja_global={
                "show_times": SHOW_TIMES, 
                "get_racers": lambda: db.get_users_sorted_by_top_time(SHOW_TIMES),
                "get_current_racer": lambda: get_current_racer(),
                "default_database": lambda: db.filename if db else "",
            })
    
        # logic
        while True:
            eel.sleep(1)

    # eel.stop() was called, which calls sys.exit() done for proper cleanup
    except SystemExit: 
        pass

    # user closed the window    
    except KeyboardInterrupt:
        eel.stop()
