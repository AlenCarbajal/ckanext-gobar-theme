from setuptools import setup

setup(
    entry_points={
        'ckan.plugins': [
            'gobar_theme=ckanext.gobar_theme.plugin:GobarThemePlugin'
        ]
    }
)
