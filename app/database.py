import psycopg2
con=psycopg2.connect(database="has")
cur=con.cursor()
cur.execute("CREATE TABLE blog(id serial,title text,post text)")
con.commit()
con.close()
