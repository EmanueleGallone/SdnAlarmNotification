"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

Unfortunately I discovered that the python implementation of SQLITE is not thread safe
To cope with this issue, I created a wrapper class that is thread-safe (hopefully) ;)

"""
import sqlite3
import threading
from datetime import datetime

lock = threading.Lock()  # creating a global lock mechanism


class DBHandler:

    def __init__(self, db_url='local.db'):
        self._db_url = db_url
        self._connection = None
        self._cursor = None

    def open_connection(self):
        if self._cursor is None:
            self._connection = sqlite3.connect(self._db_url)
            self._cursor = self._connection.cursor()
        return self

    def create_alarm_table(self):
        lock.acquire()

        try:
            self._cursor.execute('''CREATE TABLE IF NOT EXISTS alarm
                         (ID INTEGER PRIMARY KEY ,deviceIP text , severity text, time timestamp, description text, notified integer)''')

        except Exception as e:
            print("something wrong creating alarm table" + str(e))

        finally:
            lock.release()  # avoiding deadlock

    def close_connection(self):
        if self._connection is not None:
            self._connection.commit()  # save all changes
            self._connection.close()

    def select_alarm_by_ID(self, ID='0'):
        lock.acquire()

        t = (ID,)
        self._cursor.execute('SELECT * FROM alarm WHERE ID=?', t)
        result = self._cursor.fetchone()

        lock.release()
        return result

    def select_alarm_by_severity_unnotified(self, severity):
        lock.acquire()

        if severity is None:
            severity = '0'

        notified = 0
        t = (severity, notified)

        self._cursor.execute('SELECT * FROM alarm WHERE (severity=?) AND (notified=?)', t)
        result = self._cursor.fetchall()

        lock.release()

        return result

    def select_all(self):
        lock.acquire()

        self._cursor.execute('SELECT * FROM alarm')
        result = self._cursor.fetchall()

        lock.release()

        return result



    def insert_row_alarm(self, device_ip='0.0.0.0', severity='0', description='debug', notified=0):
        lock.acquire()
        # Insert a row of data
        time = datetime.now()
        t = (device_ip, severity, time, description, notified, )

        self._cursor.execute('''INSERT INTO alarm 
            (deviceIP, severity, time, description, notified) VALUES (?, ?, ?, ?, ?)''', t)

        lock.release()

    def set_notified_by_ID(self,ID='0'):
        notified = 1
        t = (ID, notified)

        self._cursor.execute('UPDATE alarm SET notified = ? WHERE ID = ?;', t)

        return self._cursor.fetchall()


#####################DEBUG#########################################

import threading, time, traceback, logging, json
logging.basicConfig(filename="log.log", level=logging.ERROR)

def worker(delay, task, *args):
    """worker definition for thread task

    @param delay: it specifies the delay in which the task will be performed
    @param task: pointer to the function that will be executed by the thread
    @param args: list of arguments that will be passed to the task's parameters
    @return: void
    """
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        logging.info("inside thread")
        try:
            task(*args)
        except Exception:
            traceback.print_exc()

            logging.exception("Problem while trying to retrieve alarms' data.")
            # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay

def insert_row_thread(*args):
    dbh = DBHandler().open_connection()
    dbh.insert_row_alarm(*args)

    dbh.close_connection()


def start_threads() -> []:
    # every 5 seconds the thread will get the alarms using netconf
    delay = 5
    threads = []

    worker1 = threading.Thread(target=lambda: worker(delay, insert_row_thread, '10.11.12.19', '830'))
    threads.append(worker1)

    worker2 = threading.Thread(target=lambda: worker(delay, insert_row_thread, '10.11.12.24', '10'))
    threads.append(worker2)

    worker1.start()  # starts the thread
    worker2.start()

    return threads


if __name__ == "__main__":
    # dbh = DBHandler()
    # dbh.open_connection().create_alarm_table()
    # dbh.insert_row_alarm()

    # result = dbh.select_alarm_by_severity_unnotified('1')
    # print(result)

    # result = dbh.select_alarm_by_ID('1')
    # print(result)

    # dbh.close_connection()


    threads = start_threads()

    for t in threads:
        t.join()




    print("ended")