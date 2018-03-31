# coding: utf-8
import postgresql


class Loto:

    def __init__(self, user, password, hostname, dbname, tablename):
        self.max_time = 0

        conn_str = 'pq://' + user + ':' + password + '@' + hostname + ':5432/' + dbname

        db = postgresql.open(conn_str)

        max_time = db.prepare("SELECT max(times) FROM " + tablename)
        for row in max_time():
            self.max_time = int(row[0])
