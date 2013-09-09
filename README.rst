Django-editor
==========================

.. image:: https://travis-ci.org/littlepea/django-editor.png?branch=master
    :target: http://travis-ci.org/littlepea/django-editor

Allows pluggable WYSIWYG editors in django admin without hard dependencies.

Currently supported editors (both optional):

* `django-imperavi`_
* `django-tinycme`_

Installation
------------

1. Install with pip::

    pip install django-editor

2. Add `imperavi` or `tinymce` to your INSTALLED_APPS in `settings.py`::

    INSTALLED_APPS = (
        ...
        # Imperavi (or tinymce) rich text editor is optional
        'imperavi',
    )

Usage
-----

`editor` package gives you the following replacement classes:

* `django.forms.widgets.Textarea` => `editor.widgets.EditorWidget` (becomes `ImperaviWidget` or `TinyMCE`)
* `django.contrib.admin.ModelAdmin` => `editor.admin.EditorAdmin` (becomes `ImperaviAdmin` or stays as `ModelAdmin`)
* `django.contrib.admin.StackedInline` => `editor.admin.EditorStackedInline` (becomes `ImperaviStackedInline` or stays as `StackedInline`)

Here are some examples on how to easily turn your Textareas into WYSIWYG editors::

    # admin.py
    from django.db import models
    from django.contrib import admin
    from editor.admin import EditorAdmin, EditorStackedInline
    from editor.widgets import EditorWidget


    class MyInlineAdmin(EditorStackedInline): # StackedInline example
        model = Model1


    class MyModel2Admin(EditorAdmin): # ModelAdmin example
        inlines = [MyInlineAdmin]

    admin.site.register(Model2, MyModel2Admin)


    class MyModel3Admin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {'widget': EditorWidget},
        }

    admin.site.register(Model3, MyModel3Admin)

Optional configuration
----------------------
By default, `django-editor` checks for available editors, preferring imperavi
over TinyMCE. This mechanism is however fully configurable and extendable
through settings:

`EDITOR_PRESETS`
    An ordered list of EditorPreset modules defining usable editors.
    Defaults to: `('editor.presets.imperavi', 'editor.presets.tinymce')`

`EDITOR_PRESET`
    Setting used to set the preset, bypassing the `EDITOR_PRESETS` setting
    altogether. When not set explicitly, the first available preset from
    `EDITOR_PRESETS` is used.

Credits
-------

- `django-imperavi`_
- `django-tinycme`_
- `modern-package-template`_
- `django-newsletter`_ for providing pluggable editor code idea

.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
.. _django-imperavi: https://github.com/vasyabigi/django-imperavi
.. _django-tinycme: https://github.com/aljosa/django-tinymce
.. _django-newsletter: https://github.com/dokterbob/django-newsletter
