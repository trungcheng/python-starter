import pymysql

# Open database connection
db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")

# prepare a cursor object using cursor() method
cursor = db.cursor()


# --------------- INSERT ---------------
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
   LAST_NAME, AGE, SEX, INCOME)
   VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()


# --------------- READ ---------------
sql = "SELECT * FROM EMPLOYEE \
      WHERE INCOME > '%d'" % (1000)
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        # Now print fetched result
        print("fname = %s,lname = %s,age = %d,sex = %s,income = %d" %
              (fname, lname, age, sex, income))
except:
    print("Error: unable to fetch data")


# --------------- UPDATE ---------------
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 \
      WHERE SEX = '%c'" % ('M')
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()


# --------------- DELETE ---------------
sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()


# disconnect from server
db.close()
