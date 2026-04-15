import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.translation import gettext_lazy
from django.urls import reverse


def now(fmt=''):
    """Return current datetime formatted with strftime."""
    if fmt:
        return datetime.now().strftime(fmt)
    return datetime.now()

from jinja2.environment import Environment
from jinja2.bccache import FileSystemBytecodeCache
from jinja2.runtime import Undefined


class SilentUndefined(Undefined):
    """Handle missing template variables gracefully (like Django templates)."""
    def _fail_with_undefined_error(self, *args, **kwargs):
        class EmptyString(str):
            def __call__(self, *args, **kwargs):
                return ''
            def get(self, key):
                return ''
            @property
            def title(self):
                return ''
        return EmptyString()

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
        __float__ = __complex__ = __pow__ = __rpow__ = \
        _fail_with_undefined_error


class JinjaEnvironment(Environment):
    def __init__(self, **kwargs):
        bc_dir = os.path.join(settings.BASE_DIR, '.jinja2_cache')
        os.makedirs(bc_dir, exist_ok=True)
        kwargs.setdefault('bytecode_cache', FileSystemBytecodeCache(bc_dir))
        kwargs.setdefault('auto_reload', settings.DEBUG)

        super().__init__(**kwargs)
        self.undefined = SilentUndefined

        self.globals.update({
            'static': staticfiles_storage.url,
            'url': reverse,
            '_': gettext_lazy,
            'now': now,
            'settings': settings,
            'set': set,
            'float': float,
            'int': int,
            'list': list,
            'len': len,
            'type': type,
        })
