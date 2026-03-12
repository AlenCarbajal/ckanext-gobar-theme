# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import CKANConfig
from ckan.config.declaration import Declaration, Key

from ckanext.gobar_theme.views import get_blueprints
from ckanext.gobar_theme import helpers as gobar_helpers

log = logging.getLogger(__name__)


class GobarThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IConfigDeclaration)

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
