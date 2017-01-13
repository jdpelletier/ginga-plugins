from setuptools import setup, find_packages

# You can have one or more plugins.  Just list them all here.
# For each one, add a setup function in plugins/__init__.py
#
entry_points = """
[ginga.rv.plugins]
myglobalplugin=plugins:myglobalplugin:setup_myglobalplugin
mylocalplugin=plugins:mylocalplugin:setup_mylocalplugin
"""

setup(
    name = 'MyGingaPlugins',
    version = "1.0",
    description = "Plugin examples for the Ginga reference viewer",
    author = "Tycho Brahe",
    license = "BSD 3-clause license",
    url = "http://tbrahe.github.com/mygingaplugins",
    version = "0.1.dev",
    install_requires = ["ginga>=2.6.2"],
    packages = find_packages(),
    include_package_data = True,
    package_data = {},
    entry_points = entry_points,
)
