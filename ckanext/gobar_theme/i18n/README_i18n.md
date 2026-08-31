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

## Strings que emite el JavaScript de otras extensiones

CKAN sirve las traducciones de JS por `/api/i18n/<lang>`, y arma ese catálogo
en `ckan.lib.i18n.build_js_translations()` con una regla propia: de cada
`.pot` toma **solo las entradas cuya ocurrencia (`#:`) termina en `.js`**, y
descarta las obsoletas. Los catálogos de los plugins se procesan después del
de core, así que lo nuestro pisa lo de core.

Consecuencia: para sobrescribir un string que emite el JS de otra extensión
(por ejemplo el modal de búsqueda espacial de `ckanext-spatial`) **no alcanza
con ponerlo en la sección de overrides manuales del `.po`** — esas entradas
no tienen `#:` y nunca llegarían al catálogo JS.

Por eso existe `ckanext/gobar_theme/assets/js/i18n-overrides.js`: un archivo
que no se ejecuta ni entra en ningún bundle, y cuya única función es darle a
esos msgid un call-site `.js` real para que `pybabel extract` los deje en el
`.pot`. Como efecto secundario resuelve el HAZARD documentado en los `.po`:
al tener call-site, `pybabel update` ya no los re-obsoleta.

Para agregar uno nuevo:

1. Sumar `_('El string exacto en inglés');` en `assets/js/i18n-overrides.js`.
2. `python setup.py extract_messages` para regenerar el `.pot`.
3. Agregar el `msgid`/`msgstr` en cada `<locale>/LC_MESSAGES/*.po`, con el
   comentario `#:` que quedó en el `.pot`.
4. Compilar (paso 2 de arriba) y reiniciar.

> `babel.cfg` tiene el mapping `[javascript: **/assets/js/*.js]`. Los patrones
> se evalúan **relativos al input dir** (`gobar_theme/...`), no a la raíz del
> repo — un patrón que arranque con `ckanext/` no matchea nada. Está acotado a
> `assets/js` a propósito: `public/vendor/` tiene el Poncho minificado.
