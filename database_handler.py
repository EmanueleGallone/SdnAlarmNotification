"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

Unfortunately I discovered that the python implementation of SQLITE is not thread safe
To cope with this issue, I created a wrapper class that is thread-safe (hopefully)
by creating methods that resembles atomic operations.

Issue #2: Performances.
Sqlite is known for its poor performances but it's simple to implement and for the purpose of this project
is more than enough.

"""
import sqlite3
import threading
import logging
from datetime import datetime

lock = threading.Lock()  # creating a global lock mechanism

default_url = 'local.db'


class DBHandler(object):

    def __init__(self, db_url=default_url):
        self._db_url = db_url
        self._connection = None
        self._cursor = None

    def open_connection(self):
        #  should I check here if table exists?

        if self._cursor is None:
            self._connection = sqlite3.connect(self._db_url)
            self._cursor = self._connection.cursor()
        return self

    def create_alarm_table(self):
        lock.acquire()
        # from here on, thread-safe environment!
        try:
            self._cursor.execute('''CREATE TABLE IF NOT EXISTS alarm
                         (ID INTEGER PRIMARY KEY ,deviceIP text , severity text,
                          description text, time timestamp, notified integer, ceased integer)''')

        except Exception as e:
            print("something wrong creating alarm table" + str(e))

        finally:
            lock.release()  # avoiding deadlock

    def close_connection(self):
        lock.acquire()

        if self._connection is not None:
            self._connection.commit()  # save all changes
            self._connection.close()

        lock.release()

    def select_alarm_by_ID(self, ID='0'):
        lock.acquire()

        result = ''

        try:
            t = (ID,)
            self._cursor.execute('SELECT * FROM alarm WHERE ID=?', t)
            result = self._cursor.fetchone()

        except Exception as e:
            logging.log(logging.ERROR, "something wrong selecting alarm by ID" + str(e))

        finally:
            lock.release()  # avoiding deadlock

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

    def select_alarm_by_host_time_severity(self, host, timestamp, severity):
        lock.acquire()

        t = (host, timestamp, severity)

        self._cursor.execute('SELECT * FROM alarm WHERE (deviceIP=?) AND (time =?) AND (severity=?)', t)
        result = self._cursor.fetchall()

        lock.release()

        return result

    def select_alarm_by_device_ip(self, host):
        lock.acquire()

        t = (host,)

        self._cursor.execute('SELECT * FROM alarm WHERE (deviceIP=?)', t)
        result = self._cursor.fetchall()

        lock.release()

        return result

    def select_ceased_alarms(self):
        lock.acquire()

        ceased = 1
        t = (ceased,)

        self._cursor.execute('SELECT * FROM alarm WHERE (ceased=?)', t)
        result = self._cursor.fetchall()

        lock.release()

        return result


    def select_all(self):
        lock.acquire()

        self._cursor.execute('SELECT * FROM alarm')
        result = self._cursor.fetchall()

        lock.release()

        return result

    def insert_row_alarm(self, device_ip='0.0.0.0', severity='0', description='debug', _time=None, notified=0, ceased=0):
        lock.acquire()

        if _time is None:
            _time = datetime.now()

        t = (device_ip, severity, description, _time, notified, ceased)

        self._cursor.execute('''INSERT INTO alarm 
            (deviceIP, severity, description, time, notified, ceased) VALUES (?, ?, ?, ?, ?, ?)''', t)

        lock.release()

    def update_ceased_alarms(self, ID):
        lock.acquire()

        ceased = 1
        t = (ID, ceased)

        self._cursor.execute('UPDATE alarm SET ceased = ? WHERE ID = ?', t)

        lock.release()

    def update_notified_by_ID(self, ID):
        lock.acquire()

        notified = 1
        t = (ID, notified)

        self._cursor.execute('UPDATE alarm SET notified = ? WHERE ID = ?;', t)

        lock.release()
