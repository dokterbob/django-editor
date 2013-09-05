from .utils import Singleton


class EditorPreset(object):
    __metaclass__ = Singleton

    def is_available(self):
        """ Return whether or not the editor is available. """

        assert self.app_name, \
            'Please configure the app/module name for this preset.'

        from django.conf import settings

        if self.app_name in settings.INSTALLED_APPS:
            return True

    def get_admin(self):
        """ Get admin base class. """

        from django.contrib import admin

        return admin.ModelAdmin

    def get_stackedinline_admin(self):
        """ Get StackedInline admin base class. """

        from django.contrib import admin

        return admin.TabularInline

    def get_tabularinline_admin(self):
        """ Get TabularInline admin base class. """

        from django.contrib import admin

        return admin.StackedInline

    def get_widget(self):
        """ Get Widget class for editor. """

        from django.forms.widgets import Textarea

        return Textarea

    def __str__(self):
        """ String representation is the name. """
        assert hasattr(self, 'name'), 'No name configured for preset.'

        return self.name


class ImperaviPreset(EditorPreset):
    """ Preset for django-imperavi PyPI package. """
    name = 'django-imperavi'
    app_name = 'imperavi'

    def get_admin(self):
        """ Get admin base class. """

        from imperavi.admin import ImperaviAdmin

        return ImperaviAdmin

    def get_stackedinline_admin(self):
        """ Get StackedInline admin base class. """

        from imperavi.admin import ImperaviStackedInlineAdmin

        return ImperaviStackedInlineAdmin

    def get_tabularinline_admin(self):
        """ Not implemented. """

        return NotImplemented

    def get_widget(self):
        """ Return ImperaviWidget. """

        from imperavi.widget import ImperaviWidget

        return ImperaviWidget


class TinyMCEPreset(EditorPreset):
    """ Preset for djanog-tinymce PyPI package. """
    name = 'django-tinymce'
    app_name = 'tinymce'

    def _admin_wrapper(self, admin):
        """ Common wrapper for inline and normal admin. """

        from django.db import models

        class TinyMCEAdmin(admin):
            formfield_overrides = {
                models.TextField: {'widget': self.get_widget()}
            }

        return TinyMCEAdmin

    def get_admin(self):
        """ Get admin base class. """

        super_admin = super(TinyMCEPreset, self).get_admin()

        return self._admin_wrapper(super_admin)

    def get_widget(self):
        """ Return TinyMCE widget. """

        from tinymce.widgets import TinyMCE

        return TinyMCE


# Instances of preset singletons
imperavi = ImperaviPreset()
tinymce = TinyMCEPreset()
