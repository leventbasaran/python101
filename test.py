from flask import Flask, request, make_response
import os
from configparser import ConfigParser
import logging
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/python101.cfg')
logging.basicConfig(filename=config['LOGGING']['log_file'], level=config['LOGGING']['log_level'])

def connect():
    return mysql.connector.connect(
        user=config['DEFAULT']['mysql_user'],
	password=config['DEFAULT']['mysql_password'],
	host=config['DEFAULT']['mysql_host'],
	database=config['DEFAULT']['mysql_database'],
	auth_plugin='mysql_native_password') 


@app.route('/select', methods=['GET'])
def new_cursor():


    try:
     if request.method =='PUT':
      return make_response(jsonify(Error='Bu Endpoint Put methodunu desteklemez.'), 405)
     elif request.method == 'POST':
      return make_response(jsonify(Error='Bu Endpoint Post methodunu desteklemez.'), 405)
     elif request.method == 'DELETE':
      return make_response(jsonify(Error='Bu Endpoint Delete methodunu desteklemez.'), 405)
	
     else:
		

      mysqldb = connect()
      cursor =  mysqldb.cursor(buffered=True)
      query = f"""SELECT * FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']};"""
      cursor.execute(query)
      response = cursor.fetchall()
      mysqldb.close()

    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return("DB NOT EXIST! PLEASE CHECK LOG FILE.")
            
        else:
            logging.error(str(e))
            return("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
    return str(response)

@app.route('/insert', methods=['GET','PUT'])
def ins_ert():

   try:
    if request.method =='COPY':
     return make_response(jsonify(Error='Bu Endpoint Copy methodunu desteklemez.'), 405)
    elif request.method == 'POST':
     return make_response(jsonify(Error='Bu Endpoint Post methodunu desteklemez.'), 405)
    elif request.method == 'DELETE':
     return make_response(jsonify(Error='Bu Endpoint Delete methodunu desteklemez.'), 405)
	
    else:
     firstname = request.args.get("firstname")
     surname = request.args.get("surname")
     email = request.args.get("email")
     mysqldb = connect()
     cursor =  mysqldb.cursor(buffered=True)
     query = f"""INSERT INTO {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']} (name, surname, email) VALUES(%s,%s,%s);"""
     cursor.execute(query,(firstname,surname,email))
     mysqldb.commit()
     mysqldb.close()

   except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return("DB NOT EXIST! PLEASE CHECK LOG FILE.")
            
        else:
            logging.error(str(e))
            return("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
   return ("Islem Basariyla tamamlandi. SELECT endpointine giderek eklenen veriye bakabilirsiniz.")

@app.route('/delete', methods=['DELETE'])
def del_ete():

    try:
     if request.method =='COPY':
      return make_response(jsonify(Error='Bu Endpoint Copy methodunu desteklemez.'), 405)
     elif request.method == 'POST':
      return make_response(jsonify(Error='Bu Endpoint Post methodunu desteklemez.'), 405)
     elif request.method == 'GET':
      return make_response(jsonify(Error='Bu Endpoint Get methodunu desteklemez.'), 405)
     else:
      number = request.args.get("number")
      mysqldb = connect()
      cursor =  mysqldb.cursor(buffered=True)
      query = (f"""DELETE FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']} WHERE id = %s """)
      cursor.execute(query,(number,))
      mysqldb.commit()
      mysqldb.close()

    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return("DB NOT EXIST! PLEASE CHECK LOG FILE.")
            
        else:
            logging.error(str(e))
            return("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
    return ("Numarali kayit Basariyla Silindi. SELECT endpointine giderek tablonun son halini gorebilirsiniz.")


if __name__ == '__main__':
    app.run(debug=True, host=config['APISERVER']['api_host'], port=config['APISERVER']['api_port'])
