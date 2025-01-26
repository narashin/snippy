import itertools
import threading
import time


def show_loading_animation(message="Loading..."):
    animation = itertools.cycle(["|", "/", "-", "\\"])
    stop_animation = threading.Event()

    def animate():
        while not stop_animation.is_set():
            print(f"\r{message} {next(animation)}", end="", flush=True)
            time.sleep(0.1)
        print("\r", end="", flush=True)

    thread = threading.Thread(target=animate)
    thread.start()
    return stop_animation
