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


@eel.expose
def load_database(filename: str) -> None:
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
        return


@eel.expose
def setup_leaderboard(racers: int, max_lap_time_s: int):
    if not db:
        load_database("")

    try:
        racers = int(racers) if racers else 0
        if max_lap_time_s:
            race.MAX_LAP_TIME_MS = int(max_lap_time_s) * 1000
    except ValueError:  
        raise ValueError("Invalid input")

    create_users(racers)

    leaderboard()


@eel.expose
def go_to_page(page: str):
    if page == "leaderboard":
        leaderboard()
    elif page == "index":
        index()
    else:
        raise ValueError("Invalid page")

def index():
    if db:
        database_default = db.filename
    else:
        database_default = ""

    eel.go_to_jinja_page(eel.btl.jinja2_template("index.html", database_default=database_default))

def leaderboard():
    racers = db.get_users_sorted_by_top_time(SHOW_TIMES)
    
    eel.go_to_jinja_page(eel.btl.jinja2_template("web/templates/leaderboard.html", racers=racers, show_times=SHOW_TIMES))

def race(racer: User):
    eel.go_to_jinja_page(eel.btl.jinja2_template("web/templates/race.html", racer=racer))


if __name__ == "__main__":
    try:
        eel.init(web_dir)

        # Start the app
        eel.start('templates/index.html', jinja_templates='templates', size=(800, 600), block=False)
        eel.btl.

        # logic
        while True:
            eel.sleep(1)

    # eel.stop() was called, which calls sys.exit() done for proper cleanup
    except SystemExit: 
        pass

    # user closed the window    
    except KeyboardInterrupt:
        eel.stop()
