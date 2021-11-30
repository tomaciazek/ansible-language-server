# pylint: disable=invalid-name
# Requires Python 3.6+
# Ref: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""Configuration for the Sphinx documentation generator."""

import collections
import os
import sys
from functools import partial
from pathlib import Path

from setuptools_scm import get_version


# Patches for parsimonious->sphinx-js under Python 3.10/3.9:
collections.Mapping = collections.abc.Mapping


# -- Path setup --------------------------------------------------------------

PROJECT_ROOT_DIR = Path(__file__).parents[1].resolve()  # pylint: disable=no-member
get_scm_version = partial(get_version, root=PROJECT_ROOT_DIR)

# Patch necessary for sphinx-js to locate the `typedoc` executable:
os.environ['PATH'] = (
    f'{PROJECT_ROOT_DIR / "node_modules" / "typedoc" / "bin"!s}'
    f'{os.pathsep}{os.getenv("PATH", "")}'
)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.


# Make in-tree extension importable in non-tox setups/envs, like RTD.
# Refs:
# https://github.com/readthedocs/readthedocs.org/issues/6311
# https://github.com/readthedocs/readthedocs.org/issues/7182
sys.path.insert(0, str((Path(__file__).parent / '_ext').resolve()))

# -- Project information -----------------------------------------------------

ansible_homepage_url = 'https://www.ansible.com'
github_url = 'https://github.com'
github_repo_org = 'ansible'
github_repo_name = 'ansible-language-server'
github_repo_slug = f'{github_repo_org}/{github_repo_name}'
github_repo_url = f'{github_url}/{github_repo_slug}'
github_sponsors_url = f'{github_url}/sponsors'

project = ' '.join(github_repo_name.split('-')).title()
author = f'{project} project contributors'
copyright = author  # pylint: disable=redefined-builtin

# The short X.Y version
version = '.'.join(
    get_scm_version(
        local_scheme='no-local-version',
    ).split('.')[:3],
)

# The full version, including alpha/beta/rc tags
release = get_scm_version()

rst_epilog = f"""
.. |project| replace:: {project}
.. |release_l| replace:: ``{release}``
"""


# -- General configuration ---------------------------------------------------


# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'ansible'

# Default domain
# Tell sphinx what the primary language being documented is.
primary_domain = 'js'

# Tell sphinx what the pygments highlight language should be.
highlight_language = 'js'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # stdlib-party extensions:
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',

    # Third-party extensions:
    'myst_parser',  # extended markdown; https://pypi.org/project/myst-parser/
    'notfound.extension',
    # FIXME: `sphinx-js` is not fully configured right now; TODO: change this.
    # 'sphinx_js',  # Support for using Sphinx on JSDoc-documented JS code
    'sphinxcontrib.towncrier',  # provides `towncrier-draft-entries` directive
]

# Conditional third-party extensions:
try:
    import sphinxcontrib.spelling as _sphinxcontrib_spelling
except ImportError:
    extensions.append('spelling_stub_ext')
else:
    del _sphinxcontrib_spelling
    extensions.append('sphinxcontrib.spelling')

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'changelog-fragments.d/**',  # Towncrier-managed change notes
]

primary_domain = 'js'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_ansible_theme'

html_show_sphinx = True

html_theme_options = {
    'collapse_navigation': False,
    'analytics_id': '',
    'style_nav_header_background': '#ff5850',  # 5bbdbf
    'style_external_links': True,
    'canonical_url': f'https://{github_repo_name}.readthedocs.io/en/latest/',
    'vcs_pageview_mode': 'edit',
    'topbar_links': {
        'AnsibleFest': f'{ansible_homepage_url}/ansiblefest',
        'Products': f'{ansible_homepage_url}/tower',
        'Community': f'{ansible_homepage_url}/community',
        'Webinars & Training': f'{ansible_homepage_url}/webinars-training',
        'Blog': f'{ansible_homepage_url}/blog',
    },
    'navigation_depth': 3,
}

html_context = {
    'display_github': True,
    'github_user': github_repo_org,
    'github_repo': github_repo_name,
    'github_version': 'main/docs/',
    'current_version': version,
    'latest_version': 'latest',
    'available_versions': ('latest',),
}


# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f'{project} Documentation'

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'ALS Documentation'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
html_use_opensearch = f'https://{github_repo_name}.readthedocs.io/en/latest/'

# The master toctree document.
root_doc = master_doc = 'index'  # Sphinx 4+ / 3-  # noqa: WPS429


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    'ansible-runner': ('https://ansible-runner.rtfd.io/en/latest', None),
    'python': ('https://docs.python.org/3', None),
    'python2': ('https://docs.python.org/2', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for sphinxcontrib.spelling extension ----------------------------

spelling_ignore_acronyms = True
spelling_ignore_importable_modules = True
spelling_ignore_pypi_package_names = True
spelling_ignore_python_builtins = True
spelling_ignore_wiki_words = True
spelling_show_suggestions = True
spelling_word_list_filename = [
    'spelling_wordlist.txt',
]

# -- Options for extlinks extension ------------------------------------------

extlinks = {
    'issue': (f'{github_repo_url}/issues/%s', '#'),  # noqa: WPS323
    'pr': (f'{github_repo_url}/pull/%s', 'PR #'),  # noqa: WPS323
    'commit': (f'{github_repo_url}/commit/%s', ''),  # noqa: WPS323
    'gh': (f'{github_url}/%s', 'GitHub: '),  # noqa: WPS323
    'user': (f'{github_sponsors_url}/%s', '@'),  # noqa: WPS323
}

# -- Options for linkcheck builder -------------------------------------------

linkcheck_ignore = [
    r'http://localhost:\d+/',  # local URLs
]
linkcheck_workers = 25

# -- Options for towncrier_draft extension -----------------------------------

towncrier_draft_autoversion_mode = 'draft'  # or: 'sphinx-version', 'sphinx-release'
towncrier_draft_include_empty = True
towncrier_draft_working_directory = PROJECT_ROOT_DIR
# Not yet supported: towncrier_draft_config_path = 'pyproject.toml'  # relative to cwd

# -- Options for myst_parser extension ---------------------------------------

myst_enable_extensions = [
    'colon_fence',  # allow to optionally use ::: instead of ```
    'deflist',
    'html_admonition',  # allow having HTML admonitions
    'html_image',  # allow HTML <img> in Markdown
    'linkify',  # auto-detect URLs @ plain text, needs myst-parser[linkify]
    'replacements',  # allows Jinja2-style replacements
    'smartquotes',  # use "cursive" quotes
    'substitution',  # replace common ASCII shortcuts into their symbols
]
myst_substitutions = {
  'project': project,
  'release': release,
  'release_l': f'`{release}`',
  'version': version,
}

# -- Options for sphinx_js extension -----------------------------------------

# Example sphinx-js use: https://mozilla.github.io/fathom/ruleset.html
js_language = 'typescript'
# js_source_path = '../src'  # default: '../'
# jsdoc_cache =  # FIXME: think about cache invalidation?
# jsdoc_config_path = '../conf.json'
# root_for_relative_js_paths = js_source_path

# -- Strict mode -------------------------------------------------------------

# The reST default role (used for this markup: `text`) to use for all
# documents.
# Ref: python-attrs/attrs#571
default_role = 'any'

nitpicky = True
_any_role = 'any'
_py_obj_role = 'py:obj'
_py_class_role = 'py:class'
nitpick_ignore = [
    (_any_role, '.'),
    (_py_class_role, '.'),
    (_py_obj_role, '.'),
]
