from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
auth=Blueprint("auth",__name__)
from . import db 
from .model import User
@auth.route("/login",methods=["GET","POST"])
def login():
     if request.method=="POST":
         email=request.form.get("email")
         password=request.form.get("password")
         user=User.query.filter_by(email=email).first()
         if user:
             if check_password_hash(user.password,password):
                 flash('logged in!',category="success")
                 login_user(user,remember=True)
                 return redirect(url_for("views.home"))
             else:
                 flash('password is not correct!',category="error")
         else:
             flash('Email does not exist!',category="error")
     return render_template("login.html",user=current_user)

@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password1=request.form.get("password1")
        password2=request.form.get("password2")
        email_exists=User.query.filter_by(email=email).first()
        username_exists=User.query.filter_by(username=username).first()
        if email_exists:
            flash('hey email already exists!',category="error")
        elif username_exists:
            flash('username already taken ',category="error" )
        elif password1!=password2:
            flash('password doesn\'t mattch',category="error")
        elif len(username)<2:
            flash('hey username is too short',category="error") 
        elif len(password1)<2:
            flash('hey password is too short',category="error")
        else:
            new_user=User(email=email,password=generate_password_hash(password=password1,method='sha256'),username=username)   
            db.session.add(new_user) 
            db.session.commit()  
            login_user(new_user,remember=True)
            flash('user_created')
            redirect(url_for('views.home'))   
    
    return render_template("signup.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))