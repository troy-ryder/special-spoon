import psycopg2
conn = psycopg2.connect(
   # host="database-1.cluster-cdyenwaondwk.us-west-2.rds.amazonaws.com",
    host="localhost:5432",
    database="postgres",
    user="postgres",
    password="1qEmxCDzAeSDfhqo42DH")

cursor = conn.cursor()

cursor.execute('SELECT * FROM information_schema.tables')

rows = cursor.fetchall()
for table in rows:
    print(table)
conn.close()
