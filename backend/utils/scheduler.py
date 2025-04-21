import time
import threading
from typing import Callable, List
from utils.logger import log_event, log_error


class ScheduledTask:
    def __init__(self, name: str, interval_sec: int, action: Callable):
        self.name = name
        self.interval = interval_sec
        self.action = action
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self._stop_flag = False

    def start(self):
        log_event(f"[Scheduler] Starting task: {self.name}")
        self.thread.start()

    def stop(self):
        log_event(f"[Scheduler] Stopping task: {self.name}")
        self._stop_flag = True

    def _run_loop(self):
        while not self._stop_flag:
            try:
                log_event(f"[Scheduler] Running task: {self.name}")
                self.action()
            except Exception as e:
                log_error(f"[Scheduler] Task {self.name} error: {e}")
            time.sleep(self.interval)


class Scheduler:
    def __init__(self):
        self.tasks: List[ScheduledTask] = []

    def add_task(self, name: str, interval_sec: int, action: Callable):
        task = ScheduledTask(name, interval_sec, action)
        self.tasks.append(task)
        task.start()

    def stop_all(self):
        for task in self.tasks:
            task.stop()
