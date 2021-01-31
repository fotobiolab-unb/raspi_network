import sqlite3
import os
import json

#Reading columns
y_columns = []
with open("columns.txt",'r') as fh:
     for curline in fh:
         if not curline.startswith("#"):
            y_columns.append(curline.rstrip())
y_columns_string = ", ".join(y_columns)
y_column_names = list(map(lambda x: x.split(" ")[0],y_columns))
with open("children/y_column.json", "w") as f:
    json.dump({"y_column_names":y_column_names},f)
with open("main_server/y_column.json", "w") as f:
    json.dump({"y_column_names":y_column_names},f)


#Creating children database
children_db_path = "children/database.db"
if os.path.exists(children_db_path):
    os.remove(children_db_path)
conn = sqlite3.connect(children_db_path)
conn.execute("""
CREATE TABLE children (id integer primary key autoincrement,
url text not null,
IP text not null,
name text)
""")
conn.execute(f"""
CREATE TABLE bio (id integer,
batch_id integer,
timestamp datetime default current_timestamp,
chromossome_data text,
fitness real,
{y_columns_string},
foreign key(id) references children(id))
""")
conn.execute(f"""
CREATE TABLE assignment (id integer,
batch_id integer,
request_id integer primary key,
chromossome_data text,
fitness real default 0,
status integer default 0,
sync integer default 0,
{y_columns_string},
foreign key(id) references children(id)
)
""")
conn.commit()
conn.close()

#Creating main_server database
children_db_path = "main_server/database.db"
if os.path.exists(children_db_path):
    os.remove(children_db_path)
conn = sqlite3.connect(children_db_path)
conn.execute("""
CREATE TABLE children (id integer primary key autoincrement,
url text not null,
IP text not null,
name text)
""")
conn.execute(f"""
CREATE TABLE bio (id integer,
batch_id integer,
timestamp datetime default current_timestamp,
chromossome_data text,
fitness real,
request_id,
{y_columns_string},
foreign key(id) references children(id))
""")
conn.execute(f"""
CREATE TABLE assignment (id integer,
batch_id integer,
request_id integer primary key,
chromossome_data text,
fitness real default 0,
status integer default 0,
sync integer default 0,
{y_columns_string},
foreign key(id) references children(id)
)
""")
conn.commit()
conn.close()