from src import controller
from src import conf
import traceback

def run():
    config = conf.Config.get()
    while True:
        try:
            print(f'awaiting messages from: {", ".join(config.READ_STREAMS)}')
            controller.process_main_loop(config)
        except KeyboardInterrupt as e:
            print('\nKeyboard interrupt, ending...')
            return
        except Exception as e:
            if config.DEBUG:
                print(traceback.format_exc())
            else:
                print(f"Exception Caught on Main Loop: {e}")


if __name__ == '__main__':
    run()
