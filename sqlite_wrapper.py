"""
Wrapper to add data to database with SQLite.
Provides a bit easier access to database than sqlite itself.
Table is created when not found. Database is saved after every delete_data()
and insert_data().

For example usage, see bottom of the file.
"""

import sqlite3 as sqlite


class Database(object):
    """
    Wrapper for SQLite. Provides even easier access to database for other
    modules.
    """

    def __init__(self, db_filename, db_tablename, fields, ins_params):

        self.db_filename = db_filename  # Databases filename
        self.db_tablename = db_tablename  # Table's name
        self.fields = fields  # Fields to create new table
        self.insert_params = ins_params  # Params used in INSERT commands

        self._connect()

    def insert_data(self, values):
        """Insert data into table and save.
        values is tuple, that contains every mandatory value in table.
        """
        table = self.db_tablename
        params = self.insert_params
        sql_cmd = 'INSERT INTO %s VALUES %s' % (table, params)

        # Insert given parameters to database.
        self._cursor.execute(sql_cmd, values)
        self._conn.commit()  # Save changes to db.

    def delete_data(self, where=None):
        """Delete data matching where and save.
        If where is not specified, all records are deleted.
        """
        sql_cmd = 'DELETE FROM %s' % self.db_tablename
        if where is not None:
            sql_cmd += ' WHERE %s' % where

        self._cursor.execute(sql_cmd)  # Delete matching
        self._conn.commit()  # Save changes

    def select_data(self, where=None):
        """Select data from self.db_tablename, matching where statement,
        return as list.

        If where is not specified, all rows are returned.
        """
        sql_cmd = 'SELECT * FROM %s' % self.db_tablename
        if where is not None:
            sql_cmd += ' WHERE %s' % where
        return [x for x in self._cursor.execute(sql_cmd)]

    # Non-public

    def _connect(self):
        """Connect to database."""
        self._conn = sqlite.connect(self.db_filename)
        self._cursor = self._conn.cursor()

        self._create_table()  # Creates table if it does not exist!

    def _create_table(self):
        """Create table if it does not exist"""
        try:  # Try to open table.
            self._cursor.execute('SELECT * FROM %s' % self.db_tablename)

        except sqlite.OperationalError, e:

            # Table does not exist. Create a new table.
            if 'no such table' in e[0]:
                # Create table with given fields.
                table = self.db_tablename
                sql_cmd = 'CREATE TABLE %s (%s)' % (table, self.fields)
                self._cursor.execute(sql_cmd)

            else:  # It was unknown error, re-raise
                raise


def main():
    """Example how to use Database class."""

    # Values to create to table.
    fields = 'id INTEGER PRIMARY KEY,time INTEGER,receiver TEXT,msg TEXT'

    # Basically, id is null and ? is replaced given value when insert_data()
    # is called.
    ins_params = '(null, ?, ?, ?)'

    db_filename = 'messages.db'
    table = 'messages'

    db = Database(db_filename, table, fields, ins_params)

    # Using the database

    # Add one record and print all records.
    import time
    db.insert_data((int(time.time()), 'receiver-jack', 'hello, hello.'))
    print db.select_data()

    # Delete all records and print the empty table.
    db.delete_data()
    print db.select_data()

    # Remove created databasefile.
    import os
    os.remove(db_filename)


if __name__ == '__main__':
    main()
