import sqlite3
import json
import time
import logging
import numpy as np
import os
logging.basicConfig(filename="database.log", level=logging.DEBUG)

dir_name = os.path.dirname(__file__)

config = json.load(open(os.path.join(dir_name,"config.json")))
y_column = json.load(open(os.path.join(dir_name,"y_column.json")))["y_column_names"]

if not os.path.exists(config["database_path"]):
    config["database_path"] = os.path.join(dir_name, "database.db")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def db(database, commit=True, row_factory=dict_factory):
    def decorator(func):
        def inner(*args, **kwargs):
            connection = sqlite3.connect(database)
            if row_factory:
                connection.row_factory = dict_factory
            cursor = connection.cursor()
            R = func(cursor,*args,**kwargs)
            connection.commit() if commit else 0
            connection.close()
            return R
        return inner
    return decorator

def initialize_tables(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    #Children IP table
    cursor.execute("create table if not exists children (id integer primary key autoincrement,\
                                                         url text not null,\
                                                         IP text not null,\
                                                         name text);")
    cursor.execute("create table if not exists bio (id integer,\
                                                    batch_id integer,\
                                                    timestamp datetime default current_timestamp,\
                                                    chromossome_data text,\
                                                    fitness real,\
                                                    request_id,\
                                                    foreign key(id) references children(id));")
    cursor.execute("create table if not exists assignment (id integer,\
                                                           batch_id integer,\
                                                           request_id integer primary key autoincrement,\
                                                           chromossome_data text,\
                                                           fitness real default 0,\
                                                           status integer default 0,\
                                                           foreign key(id) references children(id));")
    connection.commit()

@db(database=config["database_path"])
def dump_bin_data(cursor,IP,fitness,chromossome_data):
    id = cursor.execute(f"select id from children where IP='{IP}'").fetchone()
    if id:
        id = id[0]
        cursor.execute(f"insert into bio(id, chromossome_data, fitness) values ({id}, {chromossome_data}, {fitness});")
        logging.info(f"\tInserting new data dump for IP {IP}.")
    else:
        logging.warning(f"\tIP: {IP} not found in children list.")

@db(database=config["database_path"])
def add_new_child(cursor,IP,name,url):
    """
    Url must contain full path
    """
    cursor.execute("insert into children(IP,name,url) values (?, ?, ?);", (IP, name, url))
    logging.info(f"\tAdding IP {IP} in table children.")

@db(database=config["database_path"], commit=False)
def fetch_children(cursor,limit=5):
    children = cursor.execute(f"select * from children limit {limit};").fetchall()
    return children

def fetch_children_no_dec(cursor,limit=5):
    children = cursor.execute(f"select * from children limit {limit};").fetchall()
    return children

@db(database=config["database_path"], commit=False)
def fetch_children_subset(cursor,id=[]):
    children = cursor.execute(f"select * from children where id in ({','.join(['?']*len(id))});", tuple(id)).fetchall()
    return children

@db(database=config["database_path"])
def fetch_all_children(cursor):
    children = cursor.execute(f"select * from children;").fetchall()
    return children

@db(database=config["database_path"])
def fetch_recent_data(cursor, limit=5):
    recent_data = cursor.execute(f"select * from bio order by timestamp desc limit {5};").fetchall()
    return recent_data

@db(database=config["database_path"])
def fitness_from_batch_id(cursor, id, return_request_id=False):
    if not return_request_id:
        fitness = cursor.execute("select fitness from bio where batch_id=? order by timestamp asc;", (id,)).fetchall()
        return fitness
    else:
        fitness = cursor.execute("select fitness, request_id from bio where batch_id=? order by timestamp asc;", (id,)).fetchall()
        return fitness

def fetch_recent_data_no_dec(cursor, limit=5):
    recent_data = cursor.execute(f"select * from bio order by timestamp desc limit {5};").fetchall()
    return recent_data

@db(database=config["database_path"])
def fetch_assignments(cursor, limit=5):
    recent_data = cursor.execute(f"select * from assignment order by batch_id desc;").fetchall()
    return recent_data

@db(database=config["database_path"], commit=False)
def get_new_batch_id(cursor):
    batch_id = cursor.execute("select batch_id from bio order by batch_id desc limit 1;").fetchone()
    batch_id = batch_id["batch_id"]+1 if batch_id else 1 #Do not set to zero
    logging.info(f"\tNew batch started with id {batch_id}")
    return batch_id

@db(database=config["database_path"], commit=True)
def get_exsiting_batch(cursor):
    batch_id = cursor.execute("select batch_id from assignment order by batch_id desc limit 1;").fetchone()
    batch_id = batch_id["batch_id"] if batch_id else False
    data = []
    if batch_id:
        data = cursor.execute(f"""select * from assignment
                                join children on assignment.id=children.id
                                where batch_id=? and status=0""", (batch_id,)).fetchall()
        if len(data)==0:
            """If this is empty, then all assignments are done. Move them to history."""
            cursor.execute(f"""insert into bio(id, batch_id, chromossome_data, fitness, request_id, {', '.join(y_column)})
                            select id, batch_id, chromossome_data, fitness, request_id, {', '.join(y_column)} from assignment where assignment.batch_id=?;""", (batch_id,))
            cursor.execute(f"""delete from assignment where batch_id=?;""", (batch_id,))
            print("All done")
    return data

@db(database=config["database_path"])
def create_assignment(cursor,id,data,batch_id):
    cursor.execute(f"insert into assignment(batch_id,id,chromossome_data) values ({batch_id}, {id}, ?);", (data,))

@db(database=config["database_path"])
def create_assignments(cursor,iterable,batch_id):
    for id,batch in iterable:
        for data in batch:
            cursor.execute("insert into assignment(batch_id,id,chromossome_data) values (?, ?, ?);", (batch_id,id,str(data.tolist())))

@db(database=config["database_path"])
def update_assignment(cursor,fitness,request_id):
    if isinstance(fitness,dict):
        update_string = ", ".join([f"{k}='{fitness[k]}'" for k in y_column])
    else:
        update_string = ", ".join(list(map(lambda x: f"{x[0]}='{x[1]}'",zip(y_column,fitness))))
    print("update_string:\n", update_string)
    cursor.execute(f"update assignment set status=1, {update_string} where request_id={request_id};")

def get_fitness_graph(cursor,limit=100):
    """
    returns maximum for each batch_id
    """
    y = cursor.execute("select max(fitness) from bio group by batch_id order by batch_id desc limit ?", (limit,)).fetchall()
    y = list(map(lambda x: x[0], y))[::-1]
    return y

@db(database=config["database_path"], commit=False, row_factory=None)
def get_home_data(cursor):
    """
    returns all data for the homepage
    """
    data = {}
    data["graph"] = get_fitness_graph(cursor)
    return data

@db(database=config["database_path"], commit=False, row_factory=None)
def get_genome_graph(cursor, id, limit=10):
    data = cursor.execute("select chromossome_data from bio where id=? order by batch_id desc limit ?", (id,limit)).fetchall()
    data = [eval(x[0]) for x in data]
    L = len(data[0])
    data = list(filter(lambda x: len(x)==L, data))
    return data

@db(database=config["database_path"], commit=False, row_factory=None)
def get_best_individual(cursor, n=1):
    q = cursor.execute("select id, max(fitness) from bio group by id order by fitness desc").fetchmany(n)
    return [x[0] for x in q]

@db(database=config["database_path"], commit=False, row_factory=None)
def get_column_names(cursor):
    cursor.execute("select * from bio limit 1;")
    col_data = cursor.description
    columns = list(map(lambda x: x[0],col_data))
    return columns

@db(database=config["database_path"], commit=False, row_factory=None)
def get_graph(cursor, column, limit, reactor_id):
    y = cursor.execute(f"select {column} from bio where id=? order by batch_id desc limit ?", (reactor_id, limit)).fetchall()
    print(y)
    y = list(map(lambda x: x[0], y))[::-1]
    return y

if __name__=="__main__":
    initialize_tables(config["database_path"])
    get_exsiting_batch()
