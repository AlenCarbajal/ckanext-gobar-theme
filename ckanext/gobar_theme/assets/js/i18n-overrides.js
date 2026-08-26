/**
 * Anclas de extracción de i18n para strings que emite el JavaScript de OTRAS
 * extensiones. Este archivo no se ejecuta ni entra en ningún bundle de
 * webassets: existe solo para `pybabel extract`.
 *
 * CKAN arma el catálogo de traducciones de JS (ckan.lib.i18n.
 * build_js_translations) tomando de cada .pot únicamente las entradas cuya
 * ocurrencia termina en ".js". Como estos msgid viven en el código de
 * ckanext-spatial y no en el nuestro, sin este archivo nunca llegarían al
 * .pot y su traducción no se serviría al navegador: por eso el modal del
 * mapa se veía en inglés.
 *
 * En _build_js_translation los catálogos de los plugins se procesan después
 * del de core, así que lo que se ponga acá pisa la traducción de core.
 */
(function () {
  // ckanext-spatial — ckanext/spatial/assets/js/spatial_query.js
  _('Please draw query extent in the map:');
  _('Apply');
  _('Cancel');
  _('Draw an extent');
})();
