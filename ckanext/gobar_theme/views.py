# -*- coding: utf-8 -*-
from __future__ import annotations

from flask import Blueprint
import ckan.plugins.toolkit as toolkit

from ckanext.gobar_theme.helpers import gobar_show_recursos

# El blueprint "custom_pages" (/paginas/*) se eliminó: el contacto vive ahora
# en argentina.gob.ar/datos-abiertos/contacto y el resto de sus rutas
# (acerca, guía, estadísticas, mapa, api-docs) nunca tuvo template. "Acerca"
# lo cubre el override de core en templates/home/about.html (ruta /about).


# ── Blueprint de recursos/productos ──
recursos_bp = Blueprint(
    "recursos",
    __name__,
    url_prefix="/recursos",
)


@recursos_bp.route("/")
def recursos():
    if not gobar_show_recursos():
        return toolkit.abort(404)
    return toolkit.render("recursos/index.html", extra_vars={
        "page_title": "Recursos",
    })


# La página /series la registra ckanext-series-explorer (blueprint "series").
def get_blueprints() -> list[Blueprint]:
    return [recursos_bp]
