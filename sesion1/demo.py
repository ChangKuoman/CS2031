import psycopg2

# connection = psycopg2.connect('dbname=test10')
connection = psycopg2.connect('dbname=test10 user=postgres password=admin')

cursor = connection.cursor()

cursor.execute('drop table if exists  table2')

cursor.execute('''create table table2(
    id integer primary key,
    completed boolean not null default false
);
'''
)

cursor.execute('insert into table2(id, completed) values(1, true);')
cursor.execute('insert into table2(id, completed) values(%s, %s);', (2, True))
cursor.execute('insert into table2(id, completed) values(%(id)s, %(completed)s)', {'id': 5, 'completed': False})

data = {
    'id': 16,
    'completed':True
}

SQL_INSERT = 'insert into table2(id, completed) values(%(id)s, %(completed)s);'
cursor.execute(SQL_INSERT, data)

cursor.execute('select * from table2;')
result = cursor.fetchall()
print('result:', result)

connection.commit()

connection.close()
cursor.close()