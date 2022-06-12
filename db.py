import sqlite3

conn=sqlite3.connect('user.db')
con=conn.cursor()

#data=(('kimhojin','12345',),
#      ('koseungreol','12345'))

#con.execute("CREATE TABLE user_info (id varchar(50),password varchar(50))")
#con.executemany('INSERT INTO user_info VALUES(?,?)',data)
#con.execute("CREATE TABLE kimhojin (follow_id varchar(50))")
#con.execute("CREATE TABLE koseungreol (follow_id varchar(50))")

#conn.commit()
#conn.close()

#conn=sqlite3.connect('keyword.db')
#con=conn.cursor()

#con.execute('CREATE TABLE keyword (keyword varchar(50))')
#con.execute('INSERT INTO keyword VALUES("컴퓨터")')
conn.commit()
conn.close()