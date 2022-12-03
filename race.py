import time

def time_ms() -> float:
    return time.time_ns() // 1_000_000

LAPS = 3
MAX_LAP_TIME_MS = 30000

class Race:
    times: list[float]
    lap: int = 0
    racer: str
    timer: float

    def __init__(self, user: str) -> None:
        self.times = []

        self.racer = user

    def start(self) -> None:
        self.timer = time_ms()

    # returns wheather it is finished
    def lap_elapsed(self) -> bool:
        self.times.append(time_ms() - self.timer)
        self.lap += 1

        if self.lap == LAPS:
            return True

        self.timer = time_ms()

        return False

    def get_last_lap_time(self) -> float:
        return self.times[-1]

    def get_lap(self) -> int:
        return self.lap
    
    def get_current_lap_time(self) -> float:
        return time_ms() - self.timer

    def get_times(self) -> list[float]:
        return self.times

    def time_run_out(self) -> bool:
        return MAX_LAP_TIME_MS < time_ms() - self.timer
