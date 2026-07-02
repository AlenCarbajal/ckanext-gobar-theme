# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import logging
from collections import OrderedDict
from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import CKANConfig
from ckan.config.declaration import Declaration, Key
from ckan.lib.plugins import DefaultTranslation

from ckanext.gobar_theme.views import get_blueprints
from ckanext.gobar_theme import helpers as gobar_helpers

log = logging.getLogger(__name__)

# Campos select de scheming (valores URI) que se exponen como facetas. Se
# indexan con prefijo ``vocab_`` porque en el schema Solr de CKAN ese campo
# dinámico es ``string`` (sin tokenizar) y por lo tanto faceteable de forma
# exacta, a diferencia de ``extras_*`` que es texto analizado. Ver
# before_dataset_index y dataset_facets.
SCHEMING_FACET_FIELDS = ("dataset_status", "dataset_accrualPeriodicity")


def provincias_from_index(pkg_dict: dict[str, Any]) -> list[str]:
    """Nombres de provincia para facetar, desde spatial_coverage/spatial_uri.

    Al indexar, los campos multivalor de scheming llegan como string JSON.
    Solo se toman las entradas de nivel ``Provincia`` del vocabulario
    territorio-argentina (infra.datos.gob.ar); país, departamentos, etc. se
    ignoran. Se prefiere ``spatial_coverage[].text`` (nombre con tildes) y se
    cae al slug de la URI si no está.
    """

    def loads(value: Any) -> list:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                return [value]
        if isinstance(value, list):
            return value
        return [value] if value else []

    provincias = []
    for item in loads(pkg_dict.get("spatial_coverage")):
        if isinstance(item, dict) and "/Provincia/" in (item.get("uri") or ""):
            text = item.get("text") or item["uri"].rsplit("/", 1)[1].replace("-", " ")
            provincias.append(text)
    if not provincias:
        for uri in loads(pkg_dict.get("spatial_uri")):
            if isinstance(uri, str) and "/Provincia/" in uri:
                provincias.append(uri.rsplit("/", 1)[1].replace("-", " "))
    return provincias


class GobarThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IConfigDeclaration)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)

    # ── IConfigurer ──
    def update_config(self, config_: CKANConfig) -> None:
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        # CORREGIDO: apunta a 'assets' donde está webassets.yml
        toolkit.add_resource("assets", "gobar_theme")

    # ── IBlueprint ──
    def get_blueprint(self) -> list:
        return get_blueprints()

    # ── ITemplateHelpers ──
    def get_helpers(self) -> dict[str, Any]:
        return gobar_helpers.get_helpers()

    # ── IConfigDeclaration (CKAN 2.11 strict mode) ──
    def declare_config_options(
        self, declaration: Declaration, key: Key
    ) -> None:
        declaration.declare(key.ckanext.gobar_theme.contact_email, "")
        declaration.declare_int(
            key.ckanext.gobar_theme.featured_datasets_limit, 4
        )
        declaration.declare_int(
            key.ckanext.gobar_theme.spatial_map_max_results, 200
        )
        declaration.declare_bool(
            key.ckanext.gobar_theme.show_api_docs, True
        )

    # ── IFacets ──
    def dataset_facets(
        self, facets_dict: "OrderedDict[str, Any]", package_type: str
    ) -> "OrderedDict[str, Any]":
        # Para harvest u otros tipos, no tocar las facetas heredadas.
        if package_type and package_type != "dataset":
            return facets_dict
        facets = OrderedDict()
        facets["organization"] = toolkit._("Organizaciones")
        facets["groups"] = toolkit._("Grupos")
        facets["res_format"] = toolkit._("Formato")
        facets["vocab_dataset_status"] = toolkit._("Estado")
        facets["vocab_dataset_accrualPeriodicity"] = toolkit._(
            "Frecuencia de actualización"
        )
        facets["vocab_provincias"] = toolkit._("Provincia")
        facets["tags"] = toolkit._("Etiquetas")
        return facets

    # ── IPackageController ──
    def before_dataset_index(
        self, pkg_dict: dict[str, Any]
    ) -> dict[str, Any]:
        # Expone los campos select de scheming (extras con valor URI) como
        # campos ``vocab_*`` (string en Solr) para poder facetar de forma
        # exacta. Se indexa la ETIQUETA legible (p. ej. "actualizado") en lugar
        # de la URI, de modo que la faceta y el filtro muestren texto claro.
        for field in SCHEMING_FACET_FIELDS:
            value = pkg_dict.get(field)
            if value:
                pkg_dict["vocab_" + field] = gobar_helpers.gobar_facet_label(
                    field, value
                )
        # Provincias de la cobertura geográfica (vocab_* es string multivalor
        # en el schema Solr de CKAN, faceteable de forma exacta).
        provincias = provincias_from_index(pkg_dict)
        if provincias:
            pkg_dict["vocab_provincias"] = provincias
        return pkg_dict
