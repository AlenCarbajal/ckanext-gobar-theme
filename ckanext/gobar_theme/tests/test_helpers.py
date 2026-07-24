"""Tests unitarios de la lógica no trivial de helpers.py.

Cubren el agregado recursivo del árbol de organismos y el dedupe del listado
top-level. Ambos operan sobre dicts sintéticos de ``h.group_tree()``
(name/title/children), sin fixtures de CKAN.
"""

import ckanext.gobar_theme.helpers as helpers


def _node(name, children=None):
    return {"name": name, "title": name.title(), "children": children or []}


def _tree():
    # economia
    #   ├─ super_seguros
    #   └─ afip
    #        └─ aduana
    # salud
    aduana = _node("aduana")
    afip = _node("afip", [aduana])
    super_seguros = _node("super_seguros")
    economia = _node("economia", [super_seguros, afip])
    salud = _node("salud")
    return [economia, salud], {
        "economia": economia,
        "super_seguros": super_seguros,
        "afip": afip,
        "aduana": aduana,
        "salud": salud,
    }


def test_org_tree_with_counts_sums_descendants(monkeypatch):
    top_nodes, by_name = _tree()
    counts = {
        "economia": 5, "super_seguros": 3, "afip": 10, "aduana": 2, "salud": 7,
    }
    monkeypatch.setattr(
        helpers, "gobar_org_details_by_name",
        lambda: {n: {"package_count": c} for n, c in counts.items()},
    )

    helpers.gobar_org_tree_with_counts(top_nodes)

    assert by_name["aduana"]["subtree_package_count"] == 2
    assert by_name["afip"]["subtree_package_count"] == 12   # 10 + 2
    assert by_name["economia"]["subtree_package_count"] == 20  # 5 + 3 + 10 + 2
    assert by_name["salud"]["subtree_package_count"] == 7


def test_org_tree_with_counts_missing_details_default_zero(monkeypatch):
    top_nodes, by_name = _tree()
    monkeypatch.setattr(helpers, "gobar_org_details_by_name", lambda: {})
    helpers.gobar_org_tree_with_counts(top_nodes)
    assert by_name["economia"]["subtree_package_count"] == 0


def test_dedupe_top_nodes_removes_nested_duplicate(monkeypatch):
    top_nodes, by_name = _tree()
    monkeypatch.setattr(
        helpers.toolkit.h, "group_tree", lambda type_: top_nodes, raising=False
    )
    # super_seguros aparece anidado bajo economia Y suelto en el top-level.
    top_nodes.append(by_name["super_seguros"])

    result = helpers.gobar_dedupe_top_nodes(top_nodes)

    names = [n["name"] for n in result]
    assert names == ["economia", "salud"]  # duplicado top-level filtrado


def test_dedupe_top_nodes_noop_without_duplicates(monkeypatch):
    top_nodes, _ = _tree()
    monkeypatch.setattr(
        helpers.toolkit.h, "group_tree", lambda type_: top_nodes, raising=False
    )
    assert helpers.gobar_dedupe_top_nodes(top_nodes) == top_nodes


def test_dedupe_top_nodes_usa_arbol_global_no_la_pagina(monkeypatch):
    # El bug real: /organization pagina y pasa solo esa página a group_tree(),
    # así que un hijo cuyo padre cayó en OTRA página se ve "top-level" en la
    # suya. El dedupe debe chequear contra el árbol GLOBAL, no contra
    # top_nodes (que acá simula una página que ni siquiera contiene al padre).
    full_top_nodes, by_name = _tree()
    monkeypatch.setattr(
        helpers.toolkit.h, "group_tree", lambda type_: full_top_nodes,
        raising=False,
    )
    # "Página 2": solo trae super_seguros suelto (su padre economia quedó en
    # la página 1 y no está en esta lista).
    page_2_top_nodes = [by_name["super_seguros"], by_name["salud"]]

    result = helpers.gobar_dedupe_top_nodes(page_2_top_nodes)

    names = [n["name"] for n in result]
    assert names == ["salud"]  # super_seguros se filtra aunque su padre no esté en esta página
