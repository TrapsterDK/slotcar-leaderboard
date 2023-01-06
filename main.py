
import datetime
import os
import eel
from tkinter import Tk, filedialog

from database import Database, User
from rsp import RP_setup, RP_callback, RP_cleanup
from race import *

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
            global MAX_LAP_TIME_MS
            MAX_LAP_TIME_MS = int(max_lap_time_s) * 1000
    except ValueError:  
        raise ValueError("Invalid input")

    create_users(racers)

@eel.expose
def print_text(text):
    print(text)

race: Race = None

@eel.expose 
def set_current_racer(user_id: int):
    global race
    race = Race(db.get_user(user_id))

def get_current_racer() -> User:
    return race.user

def start_race():
    print("start")
    global race
    if race:
        race.start()
        eel.resetcountup()
    else:
        return

def round_elapsed():
    print("elapse")
    global race
    if race and race.started:
        race.lap_elapsed()
        lap_time = race.get_last_lap_time()
        eel.AddLapTime(lap_time)
        if race.is_done_laps():
            eel.last_lap(lap_time)
            db.add_times(race.user.id, [(i+1, race) for i, race in enumerate(race.get_times())])
            race = None
        else:
            eel.resetcountup()

@eel.expose
def cancel_round():
    global race
    race = None


if __name__ == "__main__":
    try:
        RP_setup()
        eel.init(web_dir)

        setup_leaderboard("", 0, 0)

        db.create_fake_data()

        # Start the app
        eel.start('templates/leaderboard.html', jinja_templates='templates', size=(800, 600), block=False, 
            jinja_global={
                "show_times": SHOW_TIMES, 
                "get_racers": lambda: db.get_users_sorted_by_top_time(SHOW_TIMES),
                "get_current_racer": lambda: get_current_racer(),
                "default_database": lambda: db.filename if db else "",
            })

        RP_callback(start_race, round_elapsed)
    
        # logic
        while True:
            eel.sleep(1)

    # eel.stop() was called, which calls sys.exit() done for proper cleanup
    except SystemExit: 
        pass

    # user closed the window    
    except KeyboardInterrupt:
        eel.stop()

RP_cleanup()

