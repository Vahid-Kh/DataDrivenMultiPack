
import pandas as pd
import pyodbc
cnxn = pyodbc.connect(

                      "DRIVER={SQL Server};"
                      "Server=sintef; "
                      "DSN=sintef"
                      "Trusted_Connection=yes; "
                      "UID=sintef; "
                      "PWD=am3ob7e8p2pvcsdy;"
                      "host = abaco-db-1-do-user-6613097-0.db.ondigitalocean.com;"
                      "port = 25061;"

                      )


# cursor = cnxn.cursor()
# cursor.execute('SELECT * FROM Table')
#
# for row in cursor:
#     print('row = %r' % (row,))


#