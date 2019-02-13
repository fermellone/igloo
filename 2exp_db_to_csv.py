import sqlite3
import csv
dbfile = "base_datos.db"
conn = sqlite3.connect(dbfile)
conn.text_factory = str 
cur = conn.cursor()
#data = cur.execute("SELECT Apellido,Documento FROM dbdatos where Documento=29030")
data = cur.execute("SELECT * FROM dbsensores")
with open("prueba.csv", "a", newline='') as csv_file:  # Python 3 version    
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cur.description]) # write headers (encabezados)
    csv_writer.writerows(cur)
print ("finished")