from django.conf import settings as django_settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from .utils import Singleton


class Settings(object):
    """
    A settings object that proxies settings and handles defaults,
    inspired by `django-appconf` and the way it works in `django-rest-framework`.

    By default, a single instance of this class is created as `<app>_settings`,
    from which `<APP>_SETTING_NAME` can be accessed as `SETTING_NAME`, i.e.::

        from editor.settings import editor_settings

        if editor_settings.SETTING_NAME:
            # DO FUNKY DANCE

    If a setting has not been explicitly defined in Django's settings, defaults
    can be specified as `DEFAULT_SETTING_NAME` class variable or property.
    """

    __metaclass__ = Singleton

    def __init__(self):
        """
        Assert app-specific prefix.
        """
        assert hasattr(self, 'settings_prefix'), 'No settings prefix specified.'

    def __getattr__(self, attr):
        """
        Return Django setting `PREFIX_SETTING` if explicitly specified, otherwise
        return `PREFIX_SETTING_DEFAULT` if specified.
        """

        if attr.isupper():
            # Require settings to have uppercase characters

            setting = getattr(
                django_settings,
                '%s_%s' % (self.settings_prefix, attr),
                None
            )

            if not setting and not attr.startswith('DEFAULT_'):
                setting = getattr(self, 'DEFAULT_%s' % attr)

            return setting

        else:
            # Default behaviour
            raise AttributeError


class EditorSettings(Settings):
    """ django-editor specific settings. """
    settings_prefix = 'EDITOR'

    # Default set of presets in order of preference
    DEFAULT_PRESETS = (
        'editor.presets.imperavi',
        'editor.presets.tinymce'
    )

    def _get_preset_instance(self, preset):
        """
        Return the preset class instance from a dot-seperated import path.
        """

        module, attr = preset.rsplit(".", 1)

        try:
            mod = import_module(module)

        except Exception as e:
            # Catch ImportError and other exceptions too
            # (e.g. user sets setting to an integer)
            raise ImproperlyConfigured(
                "Error while importing '%s': %s" % (
                    preset, e
                )
            )

        return getattr(mod, attr)

    @property
    def PRESET(self):
        """
        Editor preset is a selection from several available preset configurations
        for editors. Returns a preset object.
        """

        # Get preset from Django settings
        try:
            configured_preset = super(EditorSettings, self).PRESET

            return self._get_preset_instance(configured_preset)

        except AttributeError:
            # No preset configured, pick the first one that's available
            # in PRESETS configuration
            presets = self.PRESETS

            # Return the first one that's available
            for preset in presets:
                preset_instance = self._get_preset_instance(preset)

                if preset_instance.is_available():
                    return preset_instance

            # No available preset found. Complain!
            raise ImproperlyConfigured(
                "No available editor preset found. "
                "Please make sure at least one of '%s' is available." % (
                    ', '.join(presets)
                )
            )


editor_settings = EditorSettings()
