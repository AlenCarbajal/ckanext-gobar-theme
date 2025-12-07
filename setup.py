from setuptools import setup, find_packages

setup(
    name='ckanext-gobar-theme',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ckan>=2.11',
    ],
    entry_points={
        'ckan.plugins': [
            'gobar_theme=ckanext.gobar_theme.plugin:GobarThemePlugin'
        ]
    }
)
