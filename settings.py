# Django settings for itcq project.
import os
PROJECT_DIR = os.path.dirname(__file__)

# Add apps to project.
os.sys.path.append(os.path.join(PROJECT_DIR, 'apps'))

gettext = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mkeller_itcq',
        'USER': 'mkeller_itcq',
        'PASSWORD': 'eye1cee2tee3queue4',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
#ADMIN_MEDIA_ROOT = os.path.join(PROJECT_DIR, '../admin_media/')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'collected_static')

# ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't@)am85)xqlwhb_4@se5m^1y1_n$lf!x%8-o3l$ne8gs!k6##p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

# STATICFILES_FINDERS = (
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder")

# STATICFILES_DIRS = (
#     os.path.join(PROJECT_DIR, 'apps', 'itcq', 'static'),
# )

MIDDLEWARE_CLASSES = (
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    #'itcq.middleware.PrivateDraft',
    #'cms.middleware.multilingual.MultilingualURLMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    "django.core.context_processors.static",
    "django.core.context_processors.debug",

    'sekizai.context_processors.sekizai',
    "cms.context_processors.cms_settings",
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'djangocms_text_ckeditor',  # should be set before cms
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    'djangocms_admin_style',
    'reversion',
    'south',

    # 'djangocms_picture',
    # 'djangocms_file',
    # 'djangocms_flash',
    # 'djangocms_link',

    # 'cms.plugins.googlemap',
    # 'cms.plugins.snippet',
    'itcq',
    # 'ao',

    'itcq.plugins.researchareapreview',
    'itcq.plugins.publicationslist',
    'itcq.plugins.linklist',
    'itcq.plugins.heading',
    'itcq.plugins.person',
    'itcq.plugins.itcqpicture',
    'itcq.plugins.itcqflash',
#    'haystack',


    'tinymce',
    # 'publisher', # post publisher
)

CMS_TEMPLATES = (
    ('itcq/default.html', gettext('default')),
    ('itcq/withsubnav.html', gettext('Page with sub-navigation')),
    ('itcq/subnavpicsleft.html', gettext('Page with sub-navigation (pictures on the left)')),
    ('itcq/subnavpicsright.html', gettext('Page with sub-navigation (pictures on the right)')),
    ('itcq/home.html', gettext('Home page')),
    ('itcq/intmeeting.html', gettext('International Symposium on Cavity-QED')),
)

CMS_PLACEHOLDER_CONF = {
    'right-column': {
        "plugins": ('FilePlugin','FlashPlugin','LinkPlugin','PicturePlugin','TextPlugin', 'SnippetsPlugin'),
        "extra_context": {"theme":"16_16"},
        "name":gettext("right column")
    },

    'body': {

        "extra_context": {"theme":"16_5"},
        "name":gettext("body"),
    },
    'fancy-content': {
        "plugins": ('TextPlugin', 'LinkPlugin'),
        "extra_context": {"theme":"16_11"},
        "name":gettext("fancy content"),
    },
}

CMS_MODERATOR = True
CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_PERMISSIONS = False

CMS_LANGUAGE_REDIRECT = False

# CMS_USE_TINYMCE = True

CMS_SOFTROOT = True

TINYMCE_DEFAULT_CONFIG = {'theme': "advanced"}

WYM_CONTAINERS = ",\n".join([
    "{'name': 'P', 'title': 'Paragraph', 'css': 'wym_containers_p'}",
    "{'name': 'H1', 'title': 'Heading_1', 'css': 'wym_containers_h1'}",
    "{'name': 'H2', 'title': 'Heading_2', 'css': 'wym_containers_h2'}",
    "{'name': 'PRE', 'title': 'Preformatted', 'css': 'wym_containers_pre'}",
    "{'name': 'BLOCKQUOTE', 'title': 'Blockquote', 'css': 'wym_containers_blockquote'}",
])

WYM_CLASSES = ""

HAYSTACK_SEARCH_ENGINE = 'whoosh'

HAYSTACK_WHOOSH_PATH = '/home/mkeller/whoosh/itcq_index'

try:
    from local_settings import *
except ImportError:
    pass
