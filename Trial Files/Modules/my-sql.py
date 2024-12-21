import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "cavitestateuniversity"
)
sql = mydb.cursor()
sql.execute("USE traffic_density")
sql.execute('SHOW TABLE status')

for x in sql:
    print(x)

sql.execute('SELECT * FROM report')
for x in sql:
    print(x)

sql.execute("USE traffic_density")
# sql.execute("""
#     CREATE TABLE report (
#         id INT PRIMARY KEY AUTO_INCREMENT,
#         minute INT NOT NULL,
#         hour INT NOT NULL,
#         day INT NOT NULL,
#         date INT NOT NULL,
#         month INT NOT NULL,
#         year INT NOT NULL,
#         lane INT NOT NULL,
#         density FLOAT(5,2) NOT NULL    
#     )
# """)


# sql.execute("DROP table report")

