from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session, request

def create_account(username, password):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'on'
        print(is_admin)

        hash_value = generate_password_hash(password)

        try:
            sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
            db.session.execute(sql, {"username":username, "password":hash_value, "admin":is_admin})
            db.session.commit()
            session["username"] = username
            
        
        except:
            return "Error creating account."
    
    return login(username,password)

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        print('ei ole käyttäjää')
        return False
    
    hash_value = user.password
    if not check_password_hash(hash_value, password):
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

def check_for_admin_rights():
    admin_or_not = db.session.execute(text("SELECT * FROM users WHERE admin = TRUE"))
    admins = admin_or_not.fetchall()
    return admins