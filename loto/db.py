# coding: utf-8
import postgresql


class Loto:

    def __init__(self, user, password, hostname, dbname, table_name):
        self.max_time = 0
        self.table_name = table_name

        conn_str = 'pq://' + user + ':' + password + '@' + hostname + ':5432/' + dbname

        db = postgresql.open(conn_str)

        max_time = db.prepare("SELECT max(times) FROM " + table_name)
        for row in max_time():
            self.max_time = int(row[0])
