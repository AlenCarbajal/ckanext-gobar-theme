# Guía de personalización de ckanext-gobar-theme

Todo lo personalizable del theme se configura por **variables de entorno o
claves del `ckan.ini`** — nunca editando templates ni código para un nodo
puntual. Esto cumple el invariante de "redistribuible con mínima config" de
Portal Andino V2: para adaptar un nodo alcanza con tocar el `.env`.

Las variables de entorno siguen la convención de `envvars` (el plugin que
CKAN ya usa en este stack): una clave `ckanext.gobar_theme.mi_clave` se
setea como `CKANEXT__GOBAR_THEME__MI_CLAVE=valor` en el `.env` del
despliegue. En desarrollo también se puede probar en caliente con
`ckan config-tool /srv/app/ckan.ini 'ckanext.gobar_theme.mi_clave=valor'`
seguido de un reload, pero eso no persiste si se recrea el contenedor —
para dejarlo fijo, siempre por `.env`.

## El perfil (`ckanext.gobar_theme.profile`)

Switch central de identidad visual. Valores: `nacional` (default) | `apn` |
`subnacional` | `base`.

- **`nacional`**: identidad "Datos Abiertos" completa (navy + índigo +
  violeta, Montserrat, mosaico) — la del portal nacional datos.gob.ar.
  Ninguna de las variables de esta guía cambia su comportamiento salvo que
  se configuren explícitamente.
- **`apn`**: organismos de la Administración Pública Nacional. Estética
  Poncho (navy + celeste, Lora en títulos) por defecto, y habilita todo lo
  personalizable de esta guía (título de una línea, subtítulo opcional,
  sección Recursos apagada, Acerca genérico, etc.)
- **`subnacional`** y **`base`**: hoy se comportan igual que `nacional`
  (no tienen identidad propia definida todavía) — quedan reservados para
  cuando se diseñe esa variante.

```
CKANEXT__GOBAR_THEME__PROFILE=apn
```

## Colores e imagen de fondo

Pisan el preset del perfil, sea cual sea. Vacíos por defecto (no cambian
nada).

| Variable | Efecto |
|---|---|
| `ckanext.gobar_theme.color_primary` | Color primario (navbar, botones, acentos) |
| `ckanext.gobar_theme.color_primary_dark` | Variante oscura (hover) |
| `ckanext.gobar_theme.color_accent` | Color de acento |
| `ckanext.gobar_theme.hero_background_image` | URL de una imagen de fondo para el hero de la home (con un overlay claro automático para que el texto se siga leyendo) |

```
CKANEXT__GOBAR_THEME__COLOR_PRIMARY=#232D4F
CKANEXT__GOBAR_THEME__HERO_BACKGROUND_IMAGE=https://miorganismo.gob.ar/fondo.jpg
```

## Título y subtítulo de la home (perfil `apn`)

- El título del hero sale de `ckan.site_title` (config nativa de CKAN, no
  específica de este theme) en una sola línea, con la última palabra en el
  color de acento.
- `ckanext.gobar_theme.subtitle`: frase opcional debajo del título. Vacío
  por defecto (no se muestra). Ejemplo (MAGyP):

```
CKAN__SITE_TITLE=Datos Agro
CKANEXT__GOBAR_THEME__SUBTITLE=En este portal podrás obtener datos numéricos y estadísticos del sector agropecuario y sus temas relacionados. Ingresá periódicamente y descubrí nuestros datos.
```

## "Organizaciones" → otro nombre

Algunos organismos APN son en rigor una Secretaría/Subsecretaría/Dirección
dentro de un ministerio, no una "organización" independiente. El texto es
configurable en los 5 lugares donde aparece (nav, footer, contador y título
de sección de la home, faceta de búsqueda):

```
CKANEXT__GOBAR_THEME__ORGANIZATIONS_LABEL=Organismos
```

Default: `Organizaciones` (sin cambios si no se configura).

## Footer: sección Institucional y logo de la Secretaría

| Variable | Default | Efecto |
|---|---|---|
| `ckanext.gobar_theme.institutional_name` | vacío (`Dirección de Datos Abiertos` en perfiles ≠ apn) | Texto del link institucional del footer |
| `ckanext.gobar_theme.institutional_url` | vacío (link a datos-abiertos en perfiles ≠ apn) | URL de ese link |
| `ckanext.gobar_theme.show_secretariat_logo` | `true` | Mostrar/ocultar el logo institucional de la esquina inferior derecha del footer |
| `ckanext.gobar_theme.secretariat_logo_url` | vacío (usa el logo de Secretaría de Innovación del theme) | URL de un logo propio |
| `ckanext.gobar_theme.secretariat_logo_alt` | `Secretaría de Innovación, Ciencia y Tecnología` | Texto alternativo de ese logo |

```
CKANEXT__GOBAR_THEME__INSTITUTIONAL_NAME=Ministerio de Agricultura, Ganadería y Pesca
CKANEXT__GOBAR_THEME__INSTITUTIONAL_URL=https://www.magyp.gob.ar
CKANEXT__GOBAR_THEME__SECRETARIAT_LOGO_URL=https://miorganismo.gob.ar/logo-blanco.png
CKANEXT__GOBAR_THEME__SECRETARIAT_LOGO_ALT=Ministerio de Agricultura, Ganadería y Pesca
```

## Sección /recursos (productos de la Dirección de Datos Abiertos)

Es contenido específico del portal nacional (datos.gob.ar, Georef, Series
de Tiempo...). `ckanext.gobar_theme.show_recursos`: `true` | `false` |
`auto` (default). En `auto`, se muestra en todos los perfiles salvo `apn`.
`true`/`false` fuerza el valor sin importar el perfil.

```
CKANEXT__GOBAR_THEME__SHOW_RECURSOS=true
```

## Otras variables existentes (no específicas de esta guía)

- `ckanext.gobar_theme.contact_email` — destino del formulario de `/paginas/contacto`.
- `ckanext.gobar_theme.featured_datasets_limit` — cantidad de datasets destacados en la home.
- `ckanext.gobar_theme.spatial_map_max_results` — tope de resultados en el mapa espacial.
- `ckanext.gobar_theme.show_api_docs` — muestra/oculta `/paginas/api-docs`.

## Cómo agregar una nueva variable personalizable

1. Declararla en `plugin.py` → `declare_config_options` (con su default,
   preservando el comportamiento actual de todos los perfiles).
2. Exponer un helper en `helpers.py` (mejor un helper con nombre propio,
   p. ej. `gobar_mi_cosa()`, que un `gobar_get_config()` inline repetido en
   varios templates) y registrarlo en `get_helpers()`.
3. Usarlo desde el/los templates que corresponda.
4. Documentarla acá.
