import sqlite3

class DB:
    
    def __init__(self, db_path):
        self.db_path = db_path 
 
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.curs = self.conn.cursor()

    def create_table(self, table_name, *columns):

        try:
            cmd = "create table {0} ( ".format(table_name) 
            for column in columns:
                if isinstance(column, Column) == True:
                    cmd += "{} {},".format(column.name, column.datatype)
            cmd = cmd[:-1]
            cmd += ");"
            self.curs.execute(cmd)
        except sqlite3.OperationalError:
            print("Table {} has already been created".format(table_name))

    def drop_table(self, table):
        cmd = "drop table {}".format(table)
        self.curs.execute(cmd)
    
    def insert(self, table, *values):
        cmd = "insert into {} values (".format(table) 
        for value in values:
            cmd += "'" + value + "'" + "," 
        cmd = cmd[:-1]
        cmd += ");"
        self.curs.execute(cmd)
        self.conn.commit()
    
    def delete(self, table, conditions='all'):
        cmd = "delete from {} ".format(table)
        if conditions == 'all':
            cmd += ";"
        else:
            cmd += conditions
            cmd += ";" 
        self.curs.execute(cmd)
        self.conn.commit()

    def update(self, table, column, value, where):
        cmd = "update {} set {}={} where {}" 
        self.curs.execute(cmd)
        self.conn.commit()

    def select(self, table, *columns):
        cmd = "select " 
        for column in columns:
            if column != 'all':
                cmd += "{},".format(column)
            else:
                cmd += "*"
        cmd = cmd [:-1]
        cmd += " from {};".format(table)
        self.curs.execute(cmd)
        return self.curs.fetchall()
    

class Column:
    
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


if __name__ == '__main__':
    db = DB('test.db')
    db.connect()
    db.insert('users', '1', 'ben')
    db.insert('users', '2', 'alex')
    numbers = db.select('users', 'num')
    for num in numbers:
        print(num[0])
