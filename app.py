from flask import Flask, render_template, json, request
from flask import render_template
import sqlite3 as sql

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
	if request.method == 'POST':
		try:
			with sql.connect("base_datos.db") as con: #Conectamos a la base de datos y lo llamamos "con"
				cursor = con.cursor()
				cursor.execute("SELECT Documento FROM dbauxiliar WHERE N=1")
				
			return render_template('exporesult.html',msg=documento)
		except:
			
			return render_template('resultado.html')
		finally:
			
			return render_template('exporesult.html',msg=documento)
	
    


if __name__ == '__main__':
    app.run(debug=True, port=8000)
