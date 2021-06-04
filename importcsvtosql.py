import pandas as pd
import pyodbc

data = pd.read_csv (r'falk.csv')
df = pd.DataFrame(data, columns= ['id', 'Namn', 'koordinatref', 'kommun', 'län', 'Förälder_id', 'År_hittad'])

print(df)



#conn = pyodbc.connect('Driver={Devart ODBC Driver for MySQL};User ID=dev;Password=1234;'
#                    'Server=127.0.0.1;'
#                    'Database=falk;'
#                    'Trusted_Connection=yes;')
#cursor = conn.cursor()

#for row in df.itertuples():
#    cursor.execute('''
#                   INSERT INTO falk.dbo.lokaler (id, Namn, koordinatref, kommun, län, Förälder_id, År_hittad)
#                   VALUES (?,?,?,?,?,?,?)
#                   ''',
#                  row.id,
#                  row.Namn,
#                  row.koordinatref,
#                  row.kommun,
#                  row.län,
#                  row.Förälder_id,
#                  row.År_hittad
#                  )

#conn.commit()
