from .settings import editor_settings


"""
Note: these are legacy API's and should be replaced by direct calls to
the relevant editor_settings methods.
"""

EditorWidget = editor_settings.PRESET.get_widget()
