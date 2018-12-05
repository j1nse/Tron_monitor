import mysql.connector
import prettytable as pt
from json import loads,dumps
tb = pt.PrettyTable()
tb.field_names = ["ie", "name"]
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="tron"
)
cursor = mydb.cursor()
word = '''\
SELECT blockID,number, block_header \
 FROM block ORDER BY number ASC LIMIT 1 \
 '''
cursor.execute(word)
tmp = cursor.fetchall()
all_data = []
if tmp:
    for i in tmp:
        one_row = []
        for j in i:
            if type(j) == str:
                one_row.append(loads(j))
            else:
                one_row.append(j)
        all_data.append(one_row)
print(
	{"blockID": all_data[0][0], 
    "block_header": all_data[0][2],
    'transactions':{}
    }

	)
