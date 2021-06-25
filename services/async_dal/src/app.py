from src.controllers import main_controller
from src import conf
import traceback

def run():
    conf.initialize()
    while True:
        try:
            main_controller.process_event_loop()
        except Exception as e:
            print(traceback.format_exc())

if __name__ == "__main__":
    run()
