import sqlite3
import json
import logging
logging.basicConfig(filename="database.log", level=logging.DEBUG)

config = json.load(open("config.json"))

def db(func):
    def inner(*args, **kwargs):
        connection = sqlite3.connect(config["database_path"])
        cursor = connection.cursor()
        R = func(cursor,*args,**kwargs)
        connection.commit()
        connection.close()
        return R
    return inner

def initialize_tables(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    #Children IP table
    cursor.execute("create table if not exists children (id integer primary key autoincrement,\
                                                         IP text not null,\
                                                         name text);")
    cursor.execute("create table if not exists bio (id integer,\
                                                    timestamp datetime default current_timestamp,\
                                                    chromossome_data text,\
                                                    fitness real,\
                                                    foreign key(id) references children(id));")
    connection.commit()

@db
def dump_bin_data(cursor,IP,fitness,chromossome_data):
    id = cursor.execute(f"select id from children where IP='{IP}'").fetchone()
    if id:
        id = id[0]
        cursor.execute(f"insert into bio(id, chromossome_data, fitness) values ({id}, {chromossome_data}, {fitness});")
        logging.info(f"\tInserting new data dump for IP {IP}.")
    else:
        logging.warning(f"\tIP: {IP} not found in children list.")

@db
def add_new_child(cursor,IP,name):
    cursor.execute(f"insert into children(IP,name) values ('{IP}', '{name}');")
    logging.info(f"\tAdding IP {IP} in table children.")

@db
def fetch_children(cursor,limit=5):
    children = cursor.execute(f"select * from children limit {limit};").fetchall()
    return children

@db
def fetch_recent_data(cursor, limit=5):
    recent_data = cursor.execute(f"select * from bio order by timestamp desc limit {5};").fetchall()
    return recent_data

if __name__=="__main__":
    initialize_tables(config["database_path"])
