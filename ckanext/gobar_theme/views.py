from flask import Blueprint


gobar_theme = Blueprint(
    "gobar_theme", __name__)


def page():
    return "Hello, gobar_theme!"


gobar_theme.add_url_rule(
    "/gobar_theme/page", view_func=page)


def get_blueprints():
    return [gobar_theme]
