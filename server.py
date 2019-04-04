from flask import Flask
from flask import render_template
from flask import session
from flask import redirect

from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from flask_nav import Nav
from flask_nav import register_renderer
from flask_nav.elements import *

from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import BootstrapRenderer

from flask_sqlalchemy import SQLAlchemy

from requests_oauthlib import OAuth2Session

import os


app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = 'supersecret'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'discord_login'

nav = Nav()


class User(UserMixin, db.Model):
    __tablename__ = 'LoginUser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    discriminator = db.Column(db.Integer, nullable=False)

    def __init__(self, discord_id, username, discriminator):
        self.id = int(discord_id)
        self.username = username
        self.discriminator = discriminator


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Subview(View):
    pass


class MyNavRenderer(BootstrapRenderer):

    def visit_Navbar(self, node):
        nav_tag = super(MyNavRenderer, self).visit_Navbar(node)
        nav_tag['class'] += ' navbar navbar-expand-md navbar-dark bg-dark'

        container_tag = nav_tag.children[0]
        div_header = container_tag.children[0]
        div_header['class'] = 'd-flex flex-grow-1'

        button_tag = div_header.children[0]
        button_tag['class'] = "navbar-toggler"

        div_nav = container_tag.children[1]
        div_nav['class'] += ' flex-grow-1 text-right'
        ul_tag = div_nav.children[0]
        ul_tag['class'] += ' ml-auto flex-nowrap'

        return nav_tag

    def visit_View(self, node):
        view_tag = super(MyNavRenderer, self).visit_View(node)
        if 'class' in view_tag.attributes:
            view_tag['class'] += ' nav-item'
        else:
            view_tag.attributes['class'] = 'nav-item'

        a_tag = view_tag.children[0]
        if 'class' in a_tag.attributes:
            a_tag['class'] += ' nav-link'
        else:
            a_tag.attributes['class'] = 'nav-link'

        return view_tag

    def visit_Subview(self, node):
        view_tag = super(MyNavRenderer, self).visit_View(node)
        view_tag['class'] = 'dropdown-item'

        return view_tag

    def visit_Subgroup(self, node):
        subgroup_tag = super(MyNavRenderer, self).visit_Subgroup(node)
        subgroup_tag['class'] += ' nav-item dropdown'

        a_tag = subgroup_tag.children[0]
        if 'class' in a_tag.attributes:
            a_tag['class'] += ' nav-link'
        else:
            a_tag.attributes['class'] = 'nav-link'

        return subgroup_tag


@nav.navigation()
def my_navbar():
    if current_user.is_authenticated:
        return Navbar(Link('Python Playground', '#'),
                      View('Home', 'index'),
                      View('Calendar', 'index'),
                      View('Configuration', 'index'),
                      Subgroup(current_user.username,
                               Text(current_user.username),
                               Separator(),
                               Subview('Logout', 'discord_logout')
                               )
                      )
    else:
        return Navbar(Link('Python Playground', '#'),
                      View('Home', 'index'),
                      View('Calendar', 'index'),
                      View('Configuration', 'index'),
                      View('Login', 'discord_login')
                      )


@app.route("/")
def index():
    return render_template('index.html')


# =====================================================
# Auth
# =====================================================

OAUTH2_CLIENT_ID = 350502671137898498
OAUTH2_REDIRECT_URI = 'http://localhost:5000/discord/callback'
OAUTH2_CLIENT_SECRET = 'dyIqCZsCf7jSSbYNppa96CWBo2Sp7dtg'
API_BASE_URL = 'https://discordapp.com/api'
TOKEN_URL = API_BASE_URL + '/oauth2/token'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater
    )


@app.route('/discord/login')
def discord_login():
    scope = request.args.get('scope', 'identify guilds')
    discord = make_session(scope=scope.split(' '))
    auth_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_token'] = state
    return redirect(auth_url)


@app.route('/discord/callback')
def discord_callback():
    if request.values.get('error'):
        return request.values['error']

    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url
    )
    user = discord.get(API_BASE_URL + '/users/@me').json()
    user_id = user['id']

    loginuser = User.query.filter_by(id=user_id).first()
    if not loginuser:
        username = user['username']
        discriminator = user['discriminator']
        loginuser = User(user['id'], user['username'], user['discriminator'])
        db.session.add(loginuser)
        db.session.commit()

    login_user(loginuser, True)
    session['username'] = user['username']
    session['oauth2_token'] = token

    return redirect(url_for('index'))


@app.route('/discord/logout')
def discord_logout():
    logout_user()
    return redirect(url_for('index'))


register_renderer(app, 'navbar', MyNavRenderer)
nav.init_app(app)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
