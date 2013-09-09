from django.test.utils import override_settings

from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .settings import editor_settings
from .presets import EditorPreset


class EditorTestBase(TestCase):
    def setUp(self):
        super(EditorTestBase, self).setUp()

        # Make current preset available in test case
        self.preset = editor_settings.PRESET

    def assertIsSubclass(self, cls, parent_cls):
        self.assertTrue(
            issubclass(cls, parent_cls),
            '%s not a subclass of %s, bases: %s' % (
                cls, parent_cls, cls.__bases__
            )
        )
        assert issubclass(cls, parent_cls)

    def assertAdmin(self, admin, stackedinline=None, tabularinline=None):
        self.assertIsSubclass(
            self.preset.get_admin(), admin
        )

        if stackedinline:
            self.assertIsSubclass(
                self.preset.get_stackedinline_admin(), stackedinline
            )

        if tabularinline:
            self.assertIsSubclass(
                self.preset.get_tabularinline_admin(), tabularinline
            )

    def assertWidget(self, widget):
        self.assertEquals(widget, self.preset.get_widget())


class PresetTests(TestCase):
    def test_settings(self):
        """ Common tests of default test setup (all editors available). """

        # Default presets available
        self.assertEquals(
            editor_settings.PRESETS,
            ('editor.presets.imperavi', 'editor.presets.tinymce')
        )

        # Current preset instance of EditorPreset
        self.assertIsInstance(editor_settings.PRESET, EditorPreset)

        # Current instance name Imperavi
        self.assertEquals(editor_settings.PRESET.name, 'django-imperavi')

        # Nonexistent settings should yield an AttributeError
        self.assertRaises(AttributeError, lambda: editor_settings.BANANA)

        # Nonsetting (non-uppercased) attrbutes should do the same
        self.assertRaises(AttributeError, lambda: editor_settings.baNANA)

    @override_settings(EDITOR_PRESETS=('editor.presets.tinymce', ))
    def test_presets_override(self):
        """ Test preset override. """

        # Presets should be overridden
        self.assertEquals(
            editor_settings.PRESETS,
            ('editor.presets.tinymce', )
        )

        # Current preset instance of EditorPreset
        self.assertIsInstance(editor_settings.PRESET, EditorPreset)

        # This should cause TinyMCE to be used
        self.assertEquals(editor_settings.PRESET.name, 'django-tinymce')

    @override_settings(EDITOR_PRESETS=())
    def test_no_presets(self):
        """ Test with no presets. """

        # Presets should be overridden
        self.assertEquals(
            editor_settings.PRESETS,
            ()
        )

        # Should raise an error
        self.assertRaises(ImproperlyConfigured, lambda: editor_settings.PRESET)

        # Still, overriding the preset should work, ignoring presets
        self.test_preset_override()

    @override_settings(EDITOR_PRESET='editor.presets.tinymce')
    def test_preset_override(self):
        """ Test preset override. """

        # Override should be set
        self.assertEquals(
            settings.EDITOR_PRESET,
            'editor.presets.tinymce'
        )

        # Current preset instance of EditorPreset
        self.assertIsInstance(editor_settings.PRESET, EditorPreset)

        # This should cause TinyMCE to be used
        self.assertEquals(editor_settings.PRESET.name, 'django-tinymce')

    @override_settings(EDITOR_PRESET='banana.juice')
    def test_wrong_preset(self):
        """ Test nonexistent preset. """

        # Override should be set
        self.assertEquals(
            settings.EDITOR_PRESET,
            'banana.juice'
        )

        # Should raise an error
        self.assertRaises(ImproperlyConfigured, lambda: editor_settings.PRESET)


# List of apps with just tinymce as editor
tinymce_installed_apps = [
    app for app in settings.INSTALLED_APPS if app != 'imperavi'
]


@override_settings(INSTALLED_APPS=tinymce_installed_apps)
class TinyMCETests(EditorTestBase):
    """ Tests with just TinyMCE available. """

    def test_classes(self):
        """
        Test whether all classes for TinyMCE are as they should be.
        """
        from tinymce.widgets import TinyMCE

        self.assertWidget(widget=TinyMCE)

        from django.contrib import admin

        self.assertAdmin(
            admin=admin.ModelAdmin,
            stackedinline=admin.StackedInline,
            tabularinline=admin.TabularInline
        )


# List of apps with just imperavi as editor
imperavi_installed_apps = [
    app for app in settings.INSTALLED_APPS if app != 'tinymce'
]


@override_settings(INSTALLED_APPS=imperavi_installed_apps)
class ImperaviTests(EditorTestBase):
    """ Tests with just Imperavi available. """

    def test_classes(self):
        """
        Test whether all classes for Imperavi are as they should be.
        """

        from imperavi.admin import (
            ImperaviAdmin,
            ImperaviStackedInlineAdmin,
            ImperaviWidget
        )

        self.assertAdmin(
            admin=ImperaviAdmin,
            stackedinline=ImperaviStackedInlineAdmin,
        )

        self.assertWidget(
            widget=ImperaviWidget,
        )

        # Tabular inlines are not available
        self.assertEquals(
            self.preset.get_tabularinline_admin(), NotImplemented
        )
