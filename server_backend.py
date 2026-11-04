
"""
    This script requires:
        - Flask (the framework, of course)
        - attributes.json file (must be in the same directory as this script btw)
    
    unstable-alpha/v1.0.0a
"""

from flask import Flask, request, Response, jsonify
import os, json, sys, hashlib

from datetime import datetime 

server = Flask(__name__)

# debugging logging (no harm guaranteed)
def console_log(message, level):
    print(f"[{level}/{datetime.now()}]~: {message}")
    
JSON_required_attributes = {
"DB_USERNAME",
"DB_PASSWORD",
"DB_DATABASE",
"DB_HOST",
"DB_USERS_TABLE"
} 

json_file = None

# attributes file check phase
try:
    with open("attributes.json", "r") as file:
        data, missing_atts = json.load(file), []
        json_file = file
        
        for i in JSON_required_attributes:
            if not i in data:
                missing_atts.append(i)
            else:
                if data[i]:
                    pass
                else:
                    missing_atts.append(i)
            
        if missing_atts and len(missing_atts) > 1:
            console_log(f"{', '.join(missing_atts)} are required attributes and they're missing.", "ERR")
        else:
            console_log(f"{missing_atts[0]} is a required attribute and it's missing.", "ERR")
                
        del missing_atts
except FileNotFoundError as err:
    console_log(err, "ERR")

import mysql.connector
from mysql.connector import MySQLConnection

# cursor and database conn variables
db = None # mysql server connection 
cursor = None

# database conn 
try:
    db = mysql.connector.connect(
host=os.environ.get("DB_HOST"), # The sql server ip
database=os.environ.get("DB_DATABASE"), # Specify a database of the sql
user=os.environ.get("DB_USERNAME"), # sql server username
password=os.environ.get("DB_PASSWORD") # its password ofc
)
except mysql.connector.errors.InterfaceError as err:
    console_log(err, "ERR")

if db:
    cursor = db.cursor()

# login method
@server.route("/login", methods=["POST"])
def login():
    
    """
        def comment: it isn't that much of impressive, but readable
        and easily to change som things
        
        (last edited on 11/4/26)
    """
    
    username = request.form["username"]
    password = hashlib(request.form["password"], os.urandom(16))
   
    # mysql user and password query
    query = cursor.execute("""
        SELECT * FROM %s
        WHERE Username = %s AND Password = %s
    """, (os.environ.get("DB_USERS_TABLE"), username, password,))

    # return
    data = {
        "status": None,
        "message": ""
    }

    if all([username, password]): # checks if all values are present
        if not query:
            data.message, data.status = 403, "Invalid username or password."   
    else:
        data.status, data.message = 400, "Bad request"
    
    return jsonify(data), data["status"]
