from markupsafe import Markup
from flask_nav import get_renderer
from flask import url_for, request, current_app


class NavigationItem(object):
    active = False

    def render(self, renderer=None, **kwargs):
        """Render the sidebar item using a renderer

        :param renderer: An object implementing the :class:`~.Renderer` interface
        :param kwargs:
        :return: A markupsafe string with the rendered result
        """
        return Markup(get_renderer(current_app, renderer)(**kwargs).visit(self))


class SidebarLink(NavigationItem):

    def __init__(self, text, href, id):
        self.text = text
        self.href = href
        self.id = id


class SidebarElement(NavigationItem):

    def __init__(self, id, labeled_by, content):
        self.id = id
        self.labeled_by = labeled_by
        self.content = content
