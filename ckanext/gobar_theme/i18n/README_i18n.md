# Traducciones override de gobar_theme

`GobarThemePlugin` implementa `ITranslation` (vía `DefaultTranslation`), por lo
que CKAN fusiona este catálogo **por encima** de las traducciones de core para
los mismos `msgid`. Sirve para sobrescribir, por ejemplo, "Datasets"
(hoy "Conjuntos de datos") por "datasets".

- Dominio: `ckanext-gobar_theme`
- Locales provistos: `es_AR/` y `es/`
- Archivos a completar: `<locale>/LC_MESSAGES/ckanext-gobar_theme.po`

## Procedimiento

1. **Completar** los `msgstr` en `es_AR/LC_MESSAGES/ckanext-gobar_theme.po`
   (y/o `es/...`). Agregar cualquier otra cadena de CKAN core que se quiera
   sobrescribir, copiando el `msgid` exacto en inglés.

2. **Compilar** los `.po` a `.mo` (dentro del contenedor / entorno con CKAN):

   ```bash
   python setup.py compile_catalog
   # o, equivalente:
   pybabel compile -d ckanext/gobar_theme/i18n -D ckanext-gobar_theme
   ```

   La config de Babel ya está en `setup.cfg` (`[compile_catalog]`, dominio
   `ckanext-gobar_theme`, directorio `ckanext/gobar_theme/i18n`).

3. **Reiniciar** CKAN (`bin/reload` o reinicio del contenedor) para que tome
   los `.mo`. El locale activo depende de `ckan.locale_default` del portal
   (si es `es_AR`, se aplica `es_AR/`; si es `es`, `es/`).

> Sin `.mo` compilado, el catálogo no se activa (no rompe nada): se sigue
> mostrando el texto de CKAN core.
