import mysql.connector
import prettytable as pt
tb = pt.PrettyTable()
tb.field_names = ["ie", "name"]
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="test"
)
mycursor = mydb.cursor()
mycursor.execute("select id,name from users order by id desc limit 1")
c=mycursor.fetchall() 
mycursor.close()
print(type(c[0]))
print(c)
for i in c:
	tb.add_row(i)
print(tb)