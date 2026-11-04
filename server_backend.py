
"""
    This script requires:
        - Flask (the framework, of course)
        - attributes.json file (must be in the same directory as this script btw)
    
    unstable-alpha/v1.0.0a
"""

from flask import Flask, request, Response, jsonify
import os, json, sys

from datetime import datetime 

# debugging logging (no harm guaranteed)
def console_log(message, level):
    print(f"[{level}/{datetime.now()}]~: {message}")
    
JSON_required_attributes = {
"DB_USERNAME",
"DB_PASSWORD",
"DB_DATABASE",
"DB_HOST"
} 

try:
    with open("attributes.json", "r") as file:
        data = json.load(file)
        for i in JSON_required_attributes:
            if not i in data:
                console_log("A required attribute wasn't found", "ERR")
                sys.exit() # idk, i think this is a good option if its about closing the running program i hope?
                break
except FileNotFoundError as err:
    console_log(err, "ERR")

import mysql.connector
from mysql.connector import MySQLConnection

server = Flask(__name__)
db = None # mysql server connection 

try:
    db = mysql.connector.connect(
host=os.environ.get("DB_HOST"), # The sql server ip
database=os.environ.get("DB_DATABASE"), # Specify a database of the sql
user=os.environ.get("DB_USERNAME"), # sql server username
password=os.environ.get("DB_PASSWORD") # its password ofc
)
except mysql.connector.errors.InterfaceError as err:
    console_log(err, "ERR")

@server.route("/v1/login", methods=["POST"])
def login():
    
    """
        comment: it isn't that much, but readable
        and easily to change som things
        
        (last edited on 11/4/26)
    """
    
    username = request.form["username"]
    password = request.form["password"]
    
    data = {
        "status": None,
        "message": ""
    }
    
    if all([username, password]): # checks if all values are present
        data.status, data.message = 400, "Bad request"
    else:
        # Database logic here
        pass
    
    return jsonify(data), data["status"]
    
    
    
            
