from flask import Blueprint
from flask import render_template ,request,flash,redirect,url_for
from flask_login import login_required,current_user
views=Blueprint("views",__name__)
from .model import Post,User,Comment
from . import db

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts=Post.query.all()
    return render_template("home.html",user=current_user,posts=posts)

@views.route("/create-post",methods=["GET","POST"])
@login_required
def create_post():
    if request.method=="POST":
        text=request.form.get('text')
        if not text:
            flash('post can not be empty',category="error")
        else:
            post=Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('post created',category="success")
            return redirect(url_for('views.home'))
    return render_template('create_post.html',user=current_user)
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    if not post:
        flash("post does not exist",category='error')
    elif current_user.id!=post.author:
        flash('you do not have permission to delete ',category='error')
    else:
        db.session.delete(post)   
        db.session.commit()
        flash('post deleted',category="success")
    return redirect(url_for('views.home'))
@views.route('/post/<username>')
@login_required
def posts(username):
    user=User.query.filter_by(username=username).first()
    if not user:
        flash('no such username exists',category="error")
        return redirect(url_for('views.home'))
    posts=user.posts
    return render_template('posts.html',user=current_user,posts=posts,username=username)
@views.route('/create-comment/<post-id>')
@login_required
def create_comment(post_id):
    text=request.form.get("text")
    if not text:
        flash("comment cant be empty",category="error")
    else:
        post=Post.query.filter_by(post_id)
        if post:
            comment=Comment(text=text,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("post doesnt exist",category="error")
    return redirect(url_for('views.home'))
        