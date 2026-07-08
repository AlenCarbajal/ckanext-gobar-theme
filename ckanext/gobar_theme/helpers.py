# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import ckan.plugins.toolkit as toolkit
import ckan.model as model

log = logging.getLogger(__name__)


# ── Gobar theme helpers ──

def gobar_dataset_count() -> int:
    try:
        result = toolkit.get_action("package_search")(
            {"ignore_auth": True}, {"rows": 0, "include_private": False}
        )
        return result.get("count", 0)
    except Exception:
        return 0


def gobar_organization_count() -> int:
    try:
        return len(toolkit.get_action("organization_list")(
            {"ignore_auth": True}, {}
        ))
    except Exception:
        return 0


def gobar_group_count() -> int:
    try:
        return len(toolkit.get_action("group_list")(
            {"ignore_auth": True}, {}
        ))
    except Exception:
        return 0


def gobar_groups_with_details() -> list[dict[str, Any]]:
    try:
        return toolkit.get_action("group_list")(
            {"ignore_auth": True},
            {"all_fields": True, "include_extras": True, "limit": 20},
        )
    except Exception:
        return []


def gobar_organizations_with_details(limit: int = 20) -> list[dict[str, Any]]:
    """Retorna organizaciones con detalle para el carrusel."""
    try:
        return toolkit.get_action("organization_list")(
            {"ignore_auth": True},
            {"all_fields": True, "include_extras": True, "limit": limit},
        )
    except Exception:
        return []


# ── Custom pages helpers ──

def gobar_page_list() -> list[dict[str, str]]:
    pages = [
        {"title": "Acerca del Portal", "url": "/paginas/acerca", "icon": "info-circle"},
        {"title": "Guía de Uso", "url": "/paginas/guia", "icon": "book"},
        {"title": "Estadísticas", "url": "/paginas/estadisticas", "icon": "bar-chart"},
        {"title": "Mapa Espacial", "url": "/paginas/mapa", "icon": "globe"},
    ]
    show_api = toolkit.config.get("ckanext.gobar_theme.show_api_docs", True)
    if show_api:
        pages.append(
            {"title": "API / Desarrolladores", "url": "/paginas/api-docs", "icon": "code"}
        )
    pages.append(
        {"title": "Contacto", "url": "/paginas/contacto", "icon": "envelope"}
    )
    return pages


def gobar_productos_list() -> list[dict[str, str]]:
    """Retorna la lista de productos de la Dirección de Datos Abiertos."""
    return [
        {
            "title": "datos.gob.ar",
            "description": "Portal Nacional de Datos Abiertos de la República Argentina.",
            "logo": "images/Logo_datos-gob-ar_Color.png",
            "url": "https://datos.gob.ar",
        },
        {
            "title": "Portal Andino",
            "description": "Plataforma de publicación de datos abiertos para organismos del Estado.",
            "logo": "images/Logo_Andino_Color.png",
            "url": "https://github.com/datosgobar/portal-andino",
        },
        {
            "title": "Georef",
            "description": "Servicio de normalización y codificación de datos geográficos de Argentina.",
            "logo": "images/Logo_Georef_Color.png",
            "url": "https://georef-ar-api.readthedocs.io",
        },
        {
            "title": "Paquete de Apertura de Datos",
            "description": "Herramientas y guías para publicar datos abiertos de calidad.",
            "logo": "images/Logo_Paqueta-Apertura-Datos_Color.png",
            "url": "https://github.com/datosgobar/paquete-apertura-datos",
        },
        {
            "title": "Series de Tiempo",
            "description": "API para acceder y explorar series de tiempo de datos económicos y estadísticos.",
            "logo": "images/Logo_Series_de_Tiempo.png",
            "url": "https://apis.datos.gob.ar/series",
        },
    ]


def gobar_comunidad_list() -> list[dict[str, str]]:
    """Retorna la sección "Documentación y otros" de la página Recursos."""
    return [
        {
            "title": "GitHub datosgobar",
            "description": "Repositorios públicos con código, estándares y documentación técnica.",
            "icon": "fa-brands fa-github",
            "url": "https://github.com/datosgobar",
        },
        {
            "title": "Perfil de Metadatos",
            "description": "Especificación del perfil de metadatos para catálogos de datos abiertos de Argentina.",
            "icon": "fa fa-book",
            "url": "https://datosgobar.github.io/paquete-apertura-datos/perfil-metadatos/",
        },
        {
            "title": "Vocabularios & Codelists",
            "description": "Vocabularios controlados y listas de códigos de referencia para publicar datos.",
            "icon": "fa fa-tags",
            "url": "https://infra.datos.gob.ar/vocabulario/",
        },
        {
            "title": "Contacto",
            "description": "Escribinos con tus consultas, sugerencias o para sumarte a la comunidad.",
            "icon": "fa fa-envelope",
            "url": "/paginas/contacto",
        },
    ]


def gobar_get_config(key: str, default: str = "") -> str:
    return toolkit.config.get(key, default)


def gobar_theme_profile() -> str:
    return toolkit.config.get("ckanext.gobar_theme.profile", "nacional")


def gobar_is_apn() -> bool:
    """Único lugar que compara contra el literal "apn": todo lo demás
    (templates y helpers) llama a esta función en vez de repetir la
    comparación de string."""
    return gobar_theme_profile() == "apn"


def gobar_show_recursos() -> bool:
    raw = str(
        toolkit.config.get("ckanext.gobar_theme.show_recursos", "auto")
    ).strip().lower()
    if raw == "auto":
        return not gobar_is_apn()
    return raw in ("true", "1", "yes", "on")


def gobar_institutional_name() -> str:
    configured = toolkit.config.get("ckanext.gobar_theme.institutional_name", "")
    if configured:
        return configured
    return "" if gobar_is_apn() else "Dirección de Datos Abiertos"


def gobar_institutional_url() -> str:
    configured = toolkit.config.get("ckanext.gobar_theme.institutional_url", "")
    if configured:
        return configured
    return "" if gobar_is_apn() else "https://www.argentina.gob.ar/datos-abiertos"


def gobar_organizations_label() -> str:
    return toolkit.config.get(
        "ckanext.gobar_theme.organizations_label", "Organizaciones"
    )


def gobar_show_secretariat_logo() -> bool:
    return toolkit.config.get("ckanext.gobar_theme.show_secretariat_logo", True)


def gobar_secretariat_logo_url() -> str:
    return toolkit.config.get("ckanext.gobar_theme.secretariat_logo_url", "")


def gobar_secretariat_logo_alt() -> str:
    return toolkit.config.get(
        "ckanext.gobar_theme.secretariat_logo_alt",
        "Secretaría de Innovación, Ciencia y Tecnología",
    )


def gobar_color_overrides_style() -> str:
    """Construye el atributo style="..." con los overrides de color de
    .ini/env (vacíos por defecto). Se aplica en el <body> (base.html) en
    vez de un <style>/:root aparte: un atributo style inline le gana en
    especificidad a body.theme-profile-* sin necesitar !important."""
    overrides = {
        "--gobar-primary": toolkit.config.get("ckanext.gobar_theme.color_primary", ""),
        "--gobar-primary-dark": toolkit.config.get(
            "ckanext.gobar_theme.color_primary_dark", ""
        ),
        "--gobar-accent": toolkit.config.get("ckanext.gobar_theme.color_accent", ""),
    }
    declarations = [f"{prop}: {value};" for prop, value in overrides.items() if value]
    return " ".join(declarations)


def gobar_hero_background_style() -> str:
    image_url = toolkit.config.get("ckanext.gobar_theme.hero_background_image", "")
    if not image_url:
        return ""
    return (
        "background-image: linear-gradient(180deg, rgba(247,247,250,.88), "
        f"rgba(255,255,255,.92)), url('{image_url}'); "
        "background-size: cover; background-position: center;"
    )


def gobar_is_spatial_enabled() -> bool:
    plugins_str: str = toolkit.config.get("ckan.plugins", "")
    return any(
        p in plugins_str
        for p in ["spatial_metadata", "spatial_query", "spatial_widget_ar"]
    )


def gobar_featured_datasets(limit: int | None = None) -> list[dict[str, Any]]:
    if limit is None:
        limit = toolkit.config.get(
            "ckanext.gobar_theme.featured_datasets_limit", 4
        )
    try:
        result = toolkit.get_action("package_search")(
            {"ignore_auth": True},
            {"rows": limit, "sort": "metadata_modified desc",
             "include_private": False},
        )
        return result.get("results", [])
    except Exception:
        return []


def gobar_format_date(date_str: str | None, fmt: str = "%d/%m/%Y") -> str:
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime(fmt)
    except (ValueError, AttributeError):
        return str(date_str)


def gobar_facet_label(facet_name: str, value: str) -> str:
    """Devuelve la etiqueta legible de un valor de faceta.

    Las facetas ``extras_dataset_status`` y ``extras_dataset_accrualPeriodicity``
    guardan URIs como valor. Esta función busca el ``label`` correspondiente en
    las ``choices`` del schema de scheming. Si no lo encuentra (o el campo no es
    de scheming), devuelve el valor sin modificar.
    """
    if not value:
        return value
    field_name = facet_name
    for prefix in ("vocab_", "extras_"):
        if field_name.startswith(prefix):
            field_name = field_name[len(prefix):]
            break
    try:
        schema = toolkit.h.scheming_get_dataset_schema("dataset")
    except Exception:
        return value
    if not schema:
        return value
    for field in schema.get("dataset_fields", []):
        if field.get("field_name") != field_name:
            continue
        for choice in field.get("choices") or []:
            if choice.get("value") == value:
                label = choice.get("label")
                if isinstance(label, dict):
                    try:
                        return toolkit.h.scheming_language_text(label)
                    except Exception:
                        return label.get("es") or label.get("en") or value
                return label or value
    return value


# ── Registry ──

def get_helpers() -> dict[str, Any]:
    return {
        # Gobar home
        "gobar_dataset_count": gobar_dataset_count,
        "gobar_organization_count": gobar_organization_count,
        "gobar_group_count": gobar_group_count,
        "gobar_groups_with_details": gobar_groups_with_details,
        "gobar_organizations_with_details": gobar_organizations_with_details,
        # Custom pages
        "gobar_page_list": gobar_page_list,
        "gobar_get_config": gobar_get_config,
        "gobar_theme_profile": gobar_theme_profile,
        "gobar_is_apn": gobar_is_apn,
        "gobar_show_recursos": gobar_show_recursos,
        "gobar_institutional_name": gobar_institutional_name,
        "gobar_institutional_url": gobar_institutional_url,
        "gobar_organizations_label": gobar_organizations_label,
        "gobar_show_secretariat_logo": gobar_show_secretariat_logo,
        "gobar_secretariat_logo_url": gobar_secretariat_logo_url,
        "gobar_secretariat_logo_alt": gobar_secretariat_logo_alt,
        "gobar_color_overrides_style": gobar_color_overrides_style,
        "gobar_hero_background_style": gobar_hero_background_style,
        "gobar_is_spatial_enabled": gobar_is_spatial_enabled,
        "gobar_featured_datasets": gobar_featured_datasets,
        "gobar_format_date": gobar_format_date,
        "gobar_productos_list": gobar_productos_list,
        "gobar_comunidad_list": gobar_comunidad_list,
        # Facetas
        "gobar_facet_label": gobar_facet_label,
    }
