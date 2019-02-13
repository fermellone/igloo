from flask import Flask, render_template, json, request
from flask import render_template
import sqlite3 as sql
import csv
from flask import send_file
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/carga', methods = ['POST','GET'])
def carga():
    return render_template('carga.html')


@app.route('/resultado', methods = ['POST','GET']) #index es para los views
def resultado():
	"""global datos
	global pulso
	global temperatura"""
	if request.method == 'POST':
		try:	
			nombre = request.form['Nombre']
			apellido = request.form['Apellido']
			documento = request.form['Documento']
			datos = [nombre, apellido, documento]
			with sql.connect("base_datos.db") as con: #Conectamos a la base de datos y lo llamamos "con"
				cursor = con.cursor()
				cursor.execute('''CREATE TABLE IF NOT EXISTS dbdatos (
									Nombre text,
									Apellido text,
									Documento text
									);'''
								)
				cursor.execute('''INSERT INTO dbdatos (Nombre, Apellido, Documento) VALUES (?,?,?);''', datos)
				q = '''UPDATE dbauxiliar SET documento=''' + documento
				cursor.execute(q)
				con.commit()
				return render_template('resultado.html')
		except Exception as e:
			print(str(e))
			return render_template('resultado.html')
		finally:
			con.close()
			return render_template('resultado.html')


@app.route('/reqcedula')
def reqcedula():
    return render_template('reqcedula.html')
    
   

@app.route('/exporesult', methods = ['POST','GET'])
def exporesult():
	if request.method=='POST':
		documento = request.form['Documento']
	else:
		documento = request.args.get('Documento')

	try:
		print("asd")
		dbfile = "base_datos.db"
		conn = sql.connect(dbfile)
		conn.text_factory = str 
		cur = conn.cursor()
		actual=0
		print(documento)
		with sql.connect("base_datos.db") as con: #Conectamos a la base de datos y lo llamamos "con"
			cursor = con.cursor()
			actual = cursor.execute("SELECT Documento FROM dbauxiliar WHERE id=1")
			actual = actual.fetchall()[0][0]
		print(actual)
		#data = cur.execute("SELECT Apellido,Documento FROM dbdatos where Documento=29030")
		q = "SELECT * FROM dbsensores WHERE documento="+str(documento)
		print(q)
		data = cur.execute(q)
		with open("prueba.csv", "w", newline='') as csv_file:  # Python 3 version    
			csv_writer = csv.writer(csv_file)
			print("generando archivo1")
			csv_writer.writerow([i[0] for i in cur.description]) # write headers (encabezados)
			print("generando archivo1")
			csv_writer.writerows(cur)
			print("generando archivo1")
			print ("finished")
		
			
		return render_template('exporesult.html')
	except Exception as e:
		print(str(e))
		
		return render_template('resultado.html')
	finally:
		
		return render_template('exporesult.html')

	
@app.route('/return-file/')
def return_file():
	return send_file('prueba.csv', as_attachment=True, attachment_filename="datos_paciente.csv")
@app.route('/file-downloads/')
def file_downloads():
	return render_template('exporesult.html')

	



if __name__ == '__main__':
    app.run(debug=True, port=8000)
