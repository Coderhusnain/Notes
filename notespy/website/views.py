from website import app,db
from .models import User,Notes
from flask_login import login_user,logout_user,current_user,login_required,login_remembered
from flask import render_template,request,flash,redirect,url_for,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import json
with app.app_context():
    db.create_all()
@app.route("/", methods=['POST','GET'])
@login_required
def home():
    if request.method=="POST":
        note=request.form.get('note')
        if len(note) <1:
            flash("Note is too short.",category="danger")
            return redirect(url_for("home"))

        else:
            new_note=Notes(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully',category='success')
            return redirect(url_for("home"))

    if request.method=='GET':

    
        return  render_template("index.html",user=current_user)
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('pwd')
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)

                flash('Logged in successfully',category='success')
                return redirect(url_for("home"))

            else:
                flash('Incorrect Password or Email.Try again!',category='danger')
                return redirect(url_for("login"))

        else:
            flash('Incorrect Email.Try again!',category='danger')
            return redirect(url_for("login"))

    if request.method=="GET":

        return  render_template("login.html",user=current_user)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return  redirect(url_for("login"))
@app.route("/signup",methods=['POST','GET'])
def signup():
    
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('pwd')
        cpassword=request.form.get('cpwd')
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category="danger")
        
        elif len(email) < 7:
            flash('Email must be greater than 7 characters',category='danger')
            return redirect(url_for("signup"))

        elif len(name) <3:
            flash('Name must be greater than 2 characters',category='danger')
            return redirect(url_for("signup"))

        elif len(password) <4:
            flash('Password must be greater than 4 characters',category='danger')
            return redirect(url_for("signup"))

        elif password!=cpassword:
            flash('Passwords must be same',category='danger')
            return redirect(url_for("signup"))

        else:
            new_user=User(email=email,username=name,password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)

            flash(f'Account has created successfully for {name} ',category='success')
            return redirect(url_for("home"))
    if request.method=='GET':
        return  render_template("signup.html",user=current_user)

@app.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
