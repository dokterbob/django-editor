from .settings import editor_settings


"""
Note: these are legacy API's and should be replaced by direct calls to
the relevant editor_settings methods.
"""

EditorAdmin = editor_settings.PRESET.get_admin()
EditorStackedInline = editor_settings.PRESET.get_stackedinline_admin()
EditorTabularInline = editor_settings.PRESET.get_tabularinline_admin()
