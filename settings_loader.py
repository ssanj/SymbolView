import sublime

from typing import Optional
from . import symbol_with_line as SWL
from . import symbol_view_setting as SVS

class SettingsLoader:

  def __init__(self, settings: sublime.Settings) -> None:
    self.settings = settings

  def load_symbol_view_settings(self) -> SVS.SymbolViewSetting:
    settings = self.settings
    if settings.has('max_line_length') and settings.has('syntaxes'):

      max_line_length = settings.get("max_line_length")
      syntax_values_list = settings.get("syntaxes")
      syntaxes = list(map(lambda syntax_value: self.load_single_syntax(syntax_value), syntax_values_list))

      valid_syntaxes = [syntax for syntax in syntaxes if syntax]

      # TODO: Add a default if the max_line_length is negative etc
      return SVS.SymbolViewSetting(max_line_length, valid_syntaxes)
      # return OpenTabSettings(settings.get('truncation_line_length'), settings.get('truncation_preview_length'))
    else:
      print(
        """
        Could not find 'max_line_length' and/or 'syntaxes' settings.
         Defaulting max_line_length: 80
         Defaulting syntaxes: []
         Update symbol_view.sublime-settings to change the above values.
        """
      )
      return SVS.SymbolViewSetting(80)

  def load_single_syntax(self, syntax: dict) -> Optional[SVS.SymbolViewSettingLabeledSyntax]:
    if syntax and len(syntax) >= 1:
      (key, values) = next(iter(syntax.items()))
      return self.load_syntax(key, values)
    else:
      print("No syntaxes to load")
      return None

  def load_syntax(self, key: str, syntax: dict) -> Optional[SVS.SymbolViewSettingLabeledSyntax]:
    syntax_names = syntax.get('syntax_names') #list -> can't be empty
    function_start = syntax.get('function_start') # str -> can't be empty
    function_ends = syntax.get('function_ends') #list -> can be empty

    if syntax_names and function_start and function_ends != None :
      return SVS.SymbolViewSettingLabeledSyntax(key, SVS.SymbolViewSettingSyntax(syntax_names, function_start, function_ends))
    else:
      print(f"Could find not required values for 'syntax_names','function_start','function_ends' for key: {key} from {syntax}")
      return None
