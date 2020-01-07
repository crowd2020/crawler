#!/bin/env python
#-*- coding: UTF-8 -*-

import MySQLdb

import xlog
from xbase import XBaseException
from xbase import DisplayAttribute
from log_last_func import last_func


class DatabaseQueryError(XBaseException):
    pass


class XDatabase(DisplayAttribute):
    def __init__(self, host, db, port=3306, user='root', passwd='', connect_timeout=3):
        self.host = host
        self.name = db
        self.port = port
        self.user = user
        self.passwd = passwd
        self.connect_timeout = connect_timeout
        self.connect_db()

    def connect_db(self):
        try:
            self.db = MySQLdb.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                db = self.name,
                port = int(self.port),
                connect_timeout = self.connect_timeout,
                charset="utf8"
            )
            self.db.autocommit(True)
            xlog.LOG.INFO("database connected!")
            return True
        except MySQLdb.Error, err:
            xlog.LOG.ERROR("CONNECT TO XDB FAILED! ERR INFO: %s" % err)
            return False

    def reconnect_db(self):
        self.disconnect_db()
        return self.connect_db()

    def disconnect_db(self):
        try:
            self.db.close()
        except AttributeError, err:
            pass
        finally:
            xlog.LOG.INFO("database connection closed!")

    def is_db_connected(self):
        try:
            self.db.ping()
            return True
        except MySQLdb.Error, err:
            xlog.LOG.ERROR("XDB DISCONNECTED!Try to reconnect..., err info: %s"
                            % err)
        except AttributeError, err:
            xlog.LOG.ERROR("XDB DISCONNECTED!Try to reconnect..., err info: %s"
                            % err)
        return False

    def switch_db(self, userid, url_hash):
        pass

    def query(self, sql, dict_ret = False):
        result = list()
        if not self.is_db_connected():
            self.connect_db()
            if not self.is_db_connected():
                raise DatabaseQueryError()
                return result, 0

        cursor = self.db.cursor() if dict_ret == False else \
                 self.db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            rows = cursor.execute(sql)
        except MySQLdb.Error, err:
            xlog.LOG.ERROR("execute sql error,err info:%d-%s, sql:%s" %
                            (err.args[0], err.args[1], sql))
            ###Duplicate Key
            if err.args[0] == 1062:
                return result, -1
            self.disconnect_db()
            raise DatabaseQueryError()
        result = cursor.fetchall()
        cursor.close()
        return result, rows

    @staticmethod
    def my_format_str(sql_format, args, escape_func):
        if args is None or len(args)<=0:
            return sql_format
        tmp = []
        for a in args:
            if type(a) is str:
                tmp.append(escape_func(a))
            elif type(a) is unicode:
                tmp.append(escape_func(a.encode('utf8')))
            else:
                tmp.append(a)
        return sql_format % tuple(tmp)

    def query2(self, sql_format_str, args=None):
        if not args:
            args = tuple()
        result = list()
        if not self.is_db_connected():
            self.connect_db()
            if not self.is_db_connected():
                raise DatabaseQueryError()
                return result, 0

        sql = XDatabase.my_format_str(sql_format_str, args, self.db.escape_string)
        xlog.LOG.DEBUG(last_func("executing sql %r"), sql)
        cursor = self.db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            rows = cursor.execute(sql)
        except MySQLdb.Error, err:
            xlog.LOG.ERROR(last_func("execute sql error,err info:%d-%s") %
                            (err.args[0], err.args[1]))
            ###Duplicate Key
            if err.args[0] == 1062:
                return result, -1
            self.disconnect_db()
            raise DatabaseQueryError()
        result = cursor.fetchall()
        cursor.close()
        return result, rows
