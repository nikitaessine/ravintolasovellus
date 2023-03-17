import os
import re
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import abort, session, request

def create_account(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        session["username"] = username
    
    except:
        return False
    
    return login(username,password)

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        print('ei ole käyttäjää')
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            print('oikea käyttäjä')
        else:
            print('väärä salasana')
            return False
        session["username"] = username

def logout():
    try:
        del session["username"]
    except:
        return

def send(name):
    sql = text("INSERT INTO restaurants (name) VALUES (:name)")
    db.session.execute(sql, {"name":name})
    db.session.commit()