try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^tinymce\.models\.HTMLField'])
except ImportError:
    pass

from .settings import editor_settings


EditorField = editor_settings.PRESET.get_model_field()
