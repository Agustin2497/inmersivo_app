
from flask import Flask, request, redirect, url_for, abort
from flask import render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy

#from models import User, Post
from forms import SignupForm, LoginForm, PostForm

from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:memoria1@localhost:5433/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import User, Post

posts = []

############################################
@app.route("/")
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)

############################################
@app.route("/p/<string:slug>/")
@login_required
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)


####################### POSTEAR UN ARTICULO #####################

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)
#################### SING UP  ########################

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

############################################################


###################¿Cómo podemos acceder en nuestro código al usuario cuyo ID se encuentra almacenado en sesión? ##########################################


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

from werkzeug.urls import url_parse

#################### REVISAR LOGIN WEB ########################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

#################################################################

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#################### REVISAR LOGIN UNREAL ########################
@app.route('/loginue5', methods=['POST'])
def login_ue():
    if current_user.is_authenticated:
            autentic = "autenticado"
            return autentic
    user_ue = request.get_json() # <-- Parseamos el JSON
    email = user_ue["email"]
    print("*******email:")
    print(email)
    user = User.get_by_email(user_ue["email"])
    if user is not None and user.check_password(user_ue["password"]):
            login_user(user, remember=True)
            #next_page = request.args.get('next')
            # if not next_page or url_parse(next_page).netloc != '':
            #     next_page = url_for('index')
            # return redirect(next_page)
    #return render_template('login_form.html', form=form)
    logeado = "logeado"
    return logeado




