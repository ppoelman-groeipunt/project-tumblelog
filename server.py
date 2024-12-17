from flask import Flask, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import *
from forms import *
from dotenv import load_dotenv
import os

# Setup server
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
connect(host=os.getenv('MONGODB_LOCAL'), db='tumblelog')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


# Define routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # POST-request
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, alias=form.alias.data)
        user.save()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    # GET-request
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # POST-request
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    # GET-request
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    # POST-request
    if form.validate_on_submit():
        p = TextPost(title=form.title.data, content=form.content.data, author=current_user)
        p.save()
        flash('Post created!', 'success')
        return redirect(url_for('index'))
    # GET-request
    posts = TextPost.objects.order_by('-timestamp')
    return render_template('index.html', form=form, posts=posts)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    p = Post.objects(id=post_id).first()
    form = CommentForm()
    # POST-request
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user)
        p.comments.append(comment)
        p.save()
        flash('Comment added!', 'success')
        return redirect(url_for('post', post_id=post_id))
    # GET-request
    return render_template('post.html', post=p, form=form)


if __name__ == '__main__':
    app.run(debug=True)
