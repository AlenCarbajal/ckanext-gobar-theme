# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from typing import Any

from flask import Blueprint
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model

from ckanext.gobar_theme.helpers import gobar_show_recursos

log = logging.getLogger(__name__)

# ── Blueprint principal para las páginas personalizadas ──
custom_pages = Blueprint(
    "custom_pages",
    __name__,
    url_prefix="/paginas",
)


def _get_context() -> dict[str, Any]:
    user = toolkit.current_user.name if toolkit.current_user else ""
    return {
        "model": model,
        "user": user,
        "auth_user_obj": toolkit.current_user,
    }


@custom_pages.route("/")
def index():
    return toolkit.render(
        "custom_pages/index.html",
        extra_vars={
            "page_title": "Páginas del Portal",
            "page_description": (
                "Accedé a información institucional, "
                "guías y recursos del portal de datos abiertos."
            ),
        },
    )


@custom_pages.route("/acerca")
def about():
    return toolkit.render(
        "custom_pages/about.html",
        extra_vars={"page_title": "Acerca del Portal"},
    )


@custom_pages.route("/guia")
def user_guide():
    return toolkit.render(
        "custom_pages/user_guide.html",
        extra_vars={"page_title": "Guía de Uso"},
    )


@custom_pages.route("/estadisticas")
def stats():
    context = _get_context()
    try:
        result = toolkit.get_action("package_search")(
            context, {"rows": 0, "include_private": False}
        )
        dataset_count = result.get("count", 0)
    except Exception:
        dataset_count = 0
    try:
        org_count = len(toolkit.get_action("organization_list")(context, {}))
    except Exception:
        org_count = 0
    try:
        group_count = len(toolkit.get_action("group_list")(context, {}))
    except Exception:
        group_count = 0
    try:
        recent = toolkit.get_action("package_search")(
            context, {"rows": 5, "sort": "metadata_modified desc"}
        )
        recent_datasets = recent.get("results", [])
    except Exception:
        recent_datasets = []

    return toolkit.render(
        "custom_pages/stats.html",
        extra_vars={
            "page_title": "Estadísticas del Portal",
            "dataset_count": dataset_count,
            "org_count": org_count,
            "group_count": group_count,
            "recent_datasets": recent_datasets,
        },
    )


@custom_pages.route("/mapa")
def spatial_map():
    context = _get_context()
    max_results = toolkit.config.get(
        "ckanext.gobar_theme.spatial_map_max_results", 200
    )
    try:
        result = toolkit.get_action("package_search")(
            context,
            {
                "rows": max_results,
                "fq": "extras_spatial:[* TO *]",
                "sort": "metadata_modified desc",
            },
        )
        spatial_datasets = result.get("results", [])
    except Exception:
        spatial_datasets = []

    return toolkit.render(
        "custom_pages/spatial_map.html",
        extra_vars={
            "page_title": "Mapa de Datos Espaciales",
            "spatial_datasets": spatial_datasets,
        },
    )


CONTACT_TIPOS = (
    "Errores e incidencias",
    "Propuestas de mejora",
    "Soporte",
    "Sugerencias",
)


@custom_pages.route("/contacto", methods=["GET", "POST"])
def contact():
    extra_vars: dict[str, Any] = {
        "page_title": "Contacto",
        "tipos": CONTACT_TIPOS,
        "data": {},
        "errors": {},
    }
    if toolkit.request.method != "POST":
        return toolkit.render("custom_pages/contact.html", extra_vars=extra_vars)

    form = toolkit.request.form
    # Honeypot: campo invisible que los bots completan.
    if form.get("website"):
        return toolkit.redirect_to("custom_pages.contact")

    data = {
        k: (form.get(k) or "").strip()
        for k in ("tipo", "nombre", "email", "asunto", "mensaje")
    }
    errors = {k: "Este campo es obligatorio" for k, v in data.items() if not v}
    if "email" not in errors and "@" not in data["email"]:
        errors["email"] = "Ingresá un email válido"
    if "tipo" not in errors and data["tipo"] not in CONTACT_TIPOS:
        errors["tipo"] = "Elegí un tipo de consulta"

    if errors:
        extra_vars.update(data=data, errors=errors)
        return toolkit.render("custom_pages/contact.html", extra_vars=extra_vars)

    import ckan.lib.mailer as mailer

    recipient = toolkit.config.get(
        "ckanext.gobar_theme.contact_email", "datosargentina@sicyt.gob.ar"
    ) or "datosargentina@sicyt.gob.ar"
    body = (
        f"Tipo de consulta: {data['tipo']}\n"
        f"Nombre: {data['nombre']}\n"
        f"Email: {data['email']}\n\n"
        f"{data['mensaje']}"
    )
    try:
        mailer.mail_recipient(
            "Datos Argentina",
            recipient,
            subject=f"[Contacto datos.gob.ar] {data['asunto']}",
            body=body,
            headers={"Reply-To": data["email"]},
        )
    except Exception:
        log.exception("Fallo el envío del formulario de contacto")
        toolkit.h.flash_error(
            "No pudimos enviar tu mensaje. Probá de nuevo más tarde."
        )
        extra_vars.update(data=data)
        return toolkit.render("custom_pages/contact.html", extra_vars=extra_vars)

    toolkit.h.flash_success("¡Gracias! Tu mensaje fue enviado.")
    return toolkit.redirect_to("custom_pages.contact")


@custom_pages.route("/api-docs")
def api_docs():
    show = toolkit.config.get("ckanext.gobar_theme.show_api_docs", True)
    if not show:
        return toolkit.abort(404)
    site_url = toolkit.config.get("ckan.site_url", "")
    return toolkit.render(
        "custom_pages/api_docs.html",
        extra_vars={
            "page_title": "Documentación de la API",
            "site_url": site_url,
        },
    )



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



# ── Blueprint de series de tiempo ──
series_bp = Blueprint(
    "series",
    __name__,
    url_prefix="/series",
)


@series_bp.route("/")
def series():
    return toolkit.render("series/index.html", extra_vars={
        "page_title": "Series de Tiempo",
    })


def get_blueprints() -> list[Blueprint]:
    blueprints = [custom_pages, recursos_bp]
    if plugins.plugin_loaded("series_explorer"):
        blueprints.append(series_bp)
    return blueprints
