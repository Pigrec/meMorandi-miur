from flask import Flask, request, render_template
import mysql.connector, time
from datetime import datetime

user='' #cambiare con Ctrl+H
password=''
host=''
nome_DB = time.strftime('anno_%Y')

def checkDB(user, password, host, nome_DB):
    try:
        mydb = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database=nome_DB
        )
    except:
        # if int(time.strftime("%d"))>15:
        #     return render_template('error.html', errore="Qualcosa è andato storto, riprovare o contattare l'assistenza.")
        
        mydb = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
        )
        
        mycursor = mydb.cursor()
        mycursor.execute(f"CREATE DATABASE {nome_DB}")
        mydb = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database=nome_DB
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("""CREATE TABLE eventi (
                        idEventi INT AUTO_INCREMENT PRIMARY KEY, 
                        TitoloEvento VARCHAR (255), 
                        Data DATE, 
                        numSettimana INT,
                        OraStart TIME, 
                        OraEnd TIME, 
                        Special BOOLEAN, 
                        Block BOOLEAN, 
                        Luogo VARCHAR (255), 
                        Note VARCHAR (255))""") 

app = Flask(__name__)
@app.route("/")
def root():
    user=''
    password=''
    host=''
    nome_DB = time.strftime('anno_%Y')
    
    checkDB(user, password, host, nome_DB)
    
    #lettura dati giorno
    mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database=nome_DB
    )
    mycursor = mydb.cursor()

    sql = "SELECT idEventi, TitoloEvento, OraStart, OraEnd, Luogo, Note FROM eventi WHERE Data = %s ORDER BY OraStart"
    target = time.strftime('%Y-%m-%d'),
    mycursor.execute(sql, target)

    myresult = mycursor.fetchall()

    lista_eventi = []

    for i in myresult:
        lista_eventi.append(i)
    
    e1, e2, e3, e4, e5, e6, e7, e8, e9 = [], [], [], [], [], [], [], [], []  

    try:
        e1 = lista_eventi[0]
        ee1 = 'block'
    except:
        ee1 = 'none'
    try:
        e2 = lista_eventi[1]
        ee2 = 'block'
    except:
        ee2 = 'none'
    try:
        e3 = lista_eventi[2]
        ee3 = 'block'
    except:
        ee3 = 'none'
    try:
        e4 = lista_eventi[3]
        ee4 = 'block'
    except:
        ee4 = 'none'
    try:
        e5 = lista_eventi[4]
        ee5 = 'block'
    except:
        ee5 = 'none'
    try:
        e6 = lista_eventi[5]
        ee6 = 'block'
    except:
        ee6 = 'none'
    try:
        e7 = lista_eventi[6]
        ee7 = 'block'
    except:
        ee7 = 'none'
    try:
        e8 = lista_eventi[7]
        ee8 = 'block'
    except:
        ee8 = 'none'
    try:
        e9 = lista_eventi[8]
        ee9 = 'block'
    except:
        ee9 = 'none'

    #lettura dati settimana
    lun, mar, mer, giov, ven, sab = ['','','','','','','','',''], ['','','','','','','','',''], ['','','','','','','','',''], ['','','','','','','','',''], ['','','','','','','','',''], ['','','','','','','','','']
    
    mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database=nome_DB
    )
    mycursor = mydb.cursor()

    sql = "SELECT idEventi, TitoloEvento, Data , OraStart, OraEnd, Luogo, Note FROM eventi WHERE numSettimana = %s ORDER BY OraStart DESC"
    target = time.strftime('%V'),
    mycursor.execute(sql, target)

    myresult = mycursor.fetchall()

    lista_eventi = []

    for y in myresult:
        disc = datetime.strptime(str(y[2]), "%Y-%m-%d").strftime("%w")
        
        timer = datetime.strptime(str(y[3]), "%H:%M:%S")
        #print(timer.strftime("%H:%M"))

        s = f'{y[1]} [{timer.strftime("%H:%M")}]' #f'{y[1]} [{y[2]}, {y[3]}]'
        
        match (int(disc)-1):       
            case 0:
                lun.insert(0,s)
            case 1:
                mar.insert(0,s)
            case 2:
                mer.insert(0,s)
            case 3:
                giov.insert(0,s)
            case 4:
                ven.insert(0,s)
            case 5:
                sab.insert(0,s)
            
    a = time.strftime('%w')
    settimana = {}
    settimana ['1'] = 'Lunedì'
    settimana ['2'] = 'Martedì'
    settimana ['3'] = 'Mercoledì'
    settimana ['4'] = 'Giovedì'
    settimana ['5'] = 'Venrdì'
    settimana ['6'] = 'Sabato'

    oggi = time.strftime(f"%d/%m/%Y, {settimana[a]}")
    
    return render_template('home.html', lun=lun, mar=mar, mer=mer, giov=giov, ven=ven, sab=sab, e1=e1, e2=e2, e3=e3, e4=e4, e5=e5, e6=e6, e7=e7, e8=e8, e9=e9, ee1=ee1, ee2=ee2, ee3=ee3, ee4=ee4, ee5=ee5, ee6=ee6, ee7=ee7, ee8=ee8, ee9=ee9, oggi=oggi)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/admin", methods=['POST'])
def admin():
    if request.form['pw']=='morandi':
        return render_template('admin.html')
    else:
        return render_template('error.html', errore="Password errata, riprovare o contattare l'assistenza.")
    
@app.route("/mod", methods=['POST'])
def form():
    user=''
    password=''
    host=''
    nome_DB = time.strftime('anno_%Y')

    dizionario = {}

    dizionario['nome'] = request.form['nome']
    dizionario['data'] = request.form['data']
    dizionario['start'] = request.form['inizio']
    dizionario['end'] = request.form['fine']
    dizionario['dove'] = request.form['dove']
    dizionario['visib'] = 'None'
    dizionario['note'] = request.form['note']
    dizionario['special'] = 'NULL' #in futuro forse..
    dizionario['num_settimana'] = datetime.strptime(str(dizionario['data']), "%Y-%m-%d").strftime("%V")

    if dizionario['note'] == '':
        dizionario['note'] = 'NULL'

    mydb = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database=nome_DB
    )
    
    mycursor = mydb.cursor()

    sql = f"INSERT INTO eventi (TitoloEvento, Data, numSettimana, OraStart, OraEnd, Luogo, Note) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (dizionario['nome'],dizionario['data'],dizionario['num_settimana'],dizionario['start'],dizionario['end'],dizionario['dove'],dizionario['note'])
    
    mycursor.execute(sql,val) 
    mydb.commit()
    return render_template('confirm.html')

@app.route("/admin/del")
def delate():
    return render_template('/admin/del.html')

@app.route("/admin/delData", methods=['POST'])
def delData():
    target = request.form['data']

    user=''
    password=''
    host=''
    nome_DB = time.strftime('anno_%Y')

    mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database=nome_DB
    )
    mycursor = mydb.cursor()

    sql = "SELECT idEventi, TitoloEvento, OraStart, OraEnd, Luogo, Note FROM eventi WHERE Data = %s  ORDER BY OraStart DESC"
    target = target,
    mycursor.execute(sql, target)

    myresult = mycursor.fetchall()

    lista_eventi = ['','','','','','','','','','','','','','','']

    for i in myresult:
        appoggio = f'id: {i[0]} - Titolo: {i[1]} [{i[2]} - {i[3]}] presso {i[4]}'
        lista_eventi.insert(0, appoggio)

    return render_template('/admin/delData.html', dat=lista_eventi)

@app.route("/admin/conf", methods=['POST'])
def confDel():
    id = request.form['id']

    user=''
    password=''
    host=''
    nome_DB = time.strftime('anno_%Y')
    
    #lettura dati giorno
    mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database=nome_DB
    )
    mycursor = mydb.cursor()

    sql = "DELETE FROM eventi WHERE idEventi = %s"
    val = id,

    mycursor.execute(sql,val)

    mydb.commit()

    return render_template('/admin/conferma.html')

if __name__ == '__main__':
    app.run()