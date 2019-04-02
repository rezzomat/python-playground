from flask import current_app

from dominate import tags
from visitor import Visitor


class Renderer(Visitor):
    """Base interface for navigation renderers.

    Visiting a node should return a string or an object that converts to a
    string containing HTML."""

    def visit_object(self, node):
        """Fallback rendering for objects.

        If the current application is in debug-mode
        (``flask.current_app.debug`` is ``True``), an ``<!-- HTML comment
        -->`` will be rendered, indicating which class is missing a visitation
        function.
        Outside of debug-mode, returns an empty string.
        """
        if current_app.debug:
            return tags.comment('no implementation in {} to render {}'.format(
                self.__class__.__name__,
                node.__class__.__name__
            ))

        return ''


class SidebarRenderer(Renderer):
    """Renderer for sidebar"""
    pass
