import threading
import time
import typing
import logging
logging.basicConfig(level=logging.INFO)


def wait_and_reset(login: str, code: str, update_password: typing.Callable):
    def wait():
        logging.info('Write your code')
        inp_code = input('')
        if LIVE and code == inp_code:
            try:
                print('Write new password')
                new_pass = input()
                update_password(login, new_pass)
                logging.info('Data saved')

            except Exception as err:
                logging.error(err)
        else:
            logging.info('Time is over or wrong code')

        nonlocal STOP
        STOP = True


    def countdown(sec: int):
        for _ in range(sec):
            if STOP:
                break
            time.sleep(1)
        logging.info('Over')
        nonlocal LIVE
        LIVE = False

    LIVE = True
    STOP = False

    thr1 = threading.Thread(target=wait)
    thr2 = threading.Thread(target=countdown, args=(40,))

    thr1.start()
    thr2.start()

    thr1.join()
    thr2.join()

# if __name__ == '__main__':
#     wait_and_reset()