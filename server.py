from flask import Flask
from flask import render_template
from flask_nav import Nav
from flask_nav import register_renderer
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import BootstrapRenderer
from dominate import tags
from hashlib import sha1


app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = 'supersecret'

nav = Nav()


class Subview(View):
    pass


class Banner(Navbar):

    def __init__(self, text, endpoint, **kwargs):
        super(text)
        self.endpoint = endpoint
        self.url_for_kwargs = kwargs

    def get_url(self):
        return url_for(self.endpoint, **self.url_for_kwargs)


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
        view_tag['class'] += ' nav-item'

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
    return Navbar(Link('Python Playground', '#'),
                  View('Home', 'index'),
                  View('Calendar', 'index'),
                  View('Configuration', 'index'),
                  Subgroup('Auth',
                           Subview('Login', 'index'),
                           Separator(),
                           Subview('Logout', 'index')
                           )
                  )



@app.route("/")
def index():
    return render_template('index.html')


register_renderer(app, 'navbar', MyNavRenderer)
nav.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
