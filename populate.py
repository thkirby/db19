import psycopg2
import random
conn = psycopg2.connect("dbname=edison user=postgres")
cur = conn.cursor()

submition_array = ["review", "complaint"]
for i in range(1,100):
    subType = submition_array[random.randint(0, 1)]
    cur.execute("INSERT INTO Submission (subID, custID, typeofSub) VALUES (%s, %s, %s)",
    (i, random.randint(0, 999), subType))


