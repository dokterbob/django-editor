from django.utils import unittest
from django.test.utils import override_settings

from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django.db import models
from django import forms
from django.contrib import admin

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

    def assertModelField(self, field):
        self.assertEquals(field, self.preset.get_model_field())


class CommonTests(EditorTestBase):
    def test_settings(self):
        """ Common tests of default test setup (all editors available). """

        # Default presets available
        self.assertEquals(
            editor_settings.PRESETS,
            ('editor.presets.imperavi', 'editor.presets.tinymce')
        )

        # Nonexistent settings should yield an AttributeError
        self.assertRaises(AttributeError, lambda: editor_settings.BANANA)

        # Nonsetting (non-uppercased) attrbutes should do the same
        self.assertRaises(AttributeError, lambda: editor_settings.baNANA)

    def test_preset_classes(self):
        """ Test preset classes. """

        # Current preset instance of EditorPreset
        self.assertIsInstance(editor_settings.PRESET, EditorPreset)

        # Assert widget class
        self.assertIsSubclass(
            editor_settings.PRESET.get_widget(), forms.Widget
        )

        # Assert model field
        self.assertIsSubclass(
            editor_settings.PRESET.get_model_field(), models.TextField
        )

        # Assert admin
        self.assertIsSubclass(
            editor_settings.PRESET.get_admin(), admin.ModelAdmin
        )

        # Assert inlines, if defined
        if editor_settings.PRESET.get_tabularinline_admin() != NotImplemented:
            self.assertIsSubclass(
                editor_settings.PRESET.get_tabularinline_admin(),
                admin.TabularInline
            )

        if editor_settings.PRESET.get_stackedinline_admin() != NotImplemented:
            self.assertIsSubclass(
                editor_settings.PRESET.get_stackedinline_admin(),
                admin.StackedInline
            )

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
        # self.test_preset_override()

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


@unittest.skipUnless(
    # Only run tests when TinyMCE is available
    'tinymce' in settings.INSTALLED_APPS,
    'django-tinymce not available for testing.'
)
@override_settings(
    # Filter imperavi from editors so just tinymce is left
    INSTALLED_APPS=filter(
        lambda app: app != 'imperavi', settings.INSTALLED_APPS
    )
)
class TinyMCETests(EditorTestBase):
    """ Tests with just TinyMCE available. """

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

    def test_classes(self):
        """
        Test whether all classes for TinyMCE are as they should be.
        """
        from tinymce.widgets import TinyMCE
        from tinymce.models import HTMLField

        self.assertWidget(widget=TinyMCE)

        self.assertAdmin(
            admin=admin.ModelAdmin,
            stackedinline=admin.StackedInline,
            tabularinline=admin.TabularInline
        )

        self.assertModelField(field=HTMLField)


@unittest.skipUnless(
    # Only run tests when TinyMCE is available
    'imperavi' in settings.INSTALLED_APPS,
    'django-imperavi not available for testing.'
)
@override_settings(
    # Filter tinymce from editors so just imparavi is left
    INSTALLED_APPS=filter(
        lambda app: app != 'tinymce', settings.INSTALLED_APPS
    )
)
class ImperaviTests(EditorTestBase):
    """ Tests with just Imperavi available. """

    def test_default_preset(self):
        """ Default preset should be imperavi. """

        # Current instance name Imperavi
        self.assertEquals(editor_settings.PRESET.name, 'django-imperavi')

    @override_settings(EDITOR_PRESETS=('editor.presets.imperavi', ))
    def test_presets_override(self):
        """ Test preset override. """

        # Presets should be overridden
        self.assertEquals(
            editor_settings.PRESETS,
            ('editor.presets.imperavi', )
        )

        # Current preset instance of EditorPreset
        self.assertIsInstance(editor_settings.PRESET, EditorPreset)

        # This should cause TinyMCE to be used
        self.assertEquals(editor_settings.PRESET.name, 'django-imperavi')

    @override_settings(EDITOR_PRESET='editor.presets.imperavi')
    def test_preset_override(self):
        """ Test preset override. """

        # Override should be set
        self.assertEquals(
            settings.EDITOR_PRESET,
            'editor.presets.imperavi'
        )

        # Current preset instance of EditorPreset
        self.assertIsInstance(editor_settings.PRESET, EditorPreset)

        # This should cause TinyMCE to be used
        self.assertEquals(editor_settings.PRESET.name, 'django-imperavi')

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

        # Assert field widget
        model_field = self.preset.get_model_field()
        form_field = model_field().formfield()

        self.assertIsInstance(
            form_field.widget,
            ImperaviWidget
        )
