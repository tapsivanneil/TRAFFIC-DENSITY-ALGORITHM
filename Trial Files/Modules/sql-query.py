import mysql.connector

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "cavitestateuniversity"
    )

sql = mydb.cursor()
sql.execute("use traffic_density") 

sql.execute("DROP TABLE report") 

sql.execute("""CREATE TABLE report (
    id INT AUTO_INCREMENT PRIMARY KEY,
    minute INT,
    hour INT,
    day INT,
    date INT,
    week INT,
    month INT,
    year INT,
    lane INT,
    density DECIMAL(5,2),
    class_1 INT,
    class_2 INT,
    class_3 INT,
    class_4 INT
)""")