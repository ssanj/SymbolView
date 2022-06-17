import sublime_plugin
import sublime
import html
from typing import List
from typing import Optional
from . import symbol_with_line as SWL
from . import symbol_view_setting as SVS

class SymbolViewCommand(sublime_plugin.TextCommand):

  def load_symbol_view_settings(self) -> SVS.SymbolViewSetting:
    settings = sublime.load_settings("symbol_view.sublime-settings")
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
    syntax_names = syntax.get('syntax_names')
    function_start = syntax.get('function_start')
    function_ends = syntax.get('function_ends')

    if syntax_names and function_start and function_ends:
      return SVS.SymbolViewSettingLabeledSyntax(key, SVS.SymbolViewSettingSyntax(syntax_names, function_start, function_ends))
    else:
      print(f"Could find not required values for 'syntax_names','function_start','function_ends' for key: {key} from {syntax}")
      return None


  def run(self, edit) -> None:
    self.settings = self.load_symbol_view_settings()
    print(self.settings)
    symbol_regions = self.view.symbol_regions()
    # TODO: Generalize for other types of symbols
    functions = self.get_functions(symbol_regions)
    window = self.view.window()

    if window:
     panel_items = self.create_panel_items(functions)
     if len(panel_items) > 0:
       window.show_quick_panel(
         items = panel_items,
         on_select = lambda index: self.on_symbol_selected(functions, index),
         on_highlight = lambda index: self.on_symbol_selected(functions, index),
         placeholder = "Functions: {}".format(len(panel_items)),
       )
     else:
       sublime.message_dialog("No functions to display")

  def on_symbol_selected(self, items: List[SWL.SymbolWithLine], index: int) -> None:
    if index != -1 and len(items) > index:
      item = items[index]
      self.view.run_command('goto_line', {'line': item.line})

  def create_panel_items(self, items: List[SWL.SymbolWithLine]) -> List[sublime.QuickPanelItem]:
    return list(map(lambda content: self.create_symbol_with_line_panel(content), items))

  def create_symbol_with_line_panel(self, symbol_with_line: SWL.SymbolWithLine) -> sublime.QuickPanelItem:
    max_line_length = self.settings.max_line_length
    search_text = symbol_with_line.name
    details = symbol_with_line.symbol_details.detail
    truncated_details = details[:max_line_length]
    suffix = "..." if len(details) > max_line_length else ""
    detail_text = html.escape(truncated_details + suffix)
    line_number = symbol_with_line.line
    annotation = symbol_with_line.symbol_details.annotation if symbol_with_line.symbol_details.annotation else ""

    return sublime.QuickPanelItem(search_text, f"<u>{detail_text}</u> <strong>{line_number}</strong>", annotation, sublime.KIND_FUNCTION)

  def calculate_line(self, region: sublime.Region) -> int:
    (zero_based_line, _) = self.view.rowcol_utf8(region.begin())
    line = zero_based_line + 1
    return line

  def get_text_at_region(self, region: sublime.Region) -> str:
    line_region = self.view.full_line(region)
    return self.view.substr(line_region)

  def get_functions(self, symbol_regions: List[sublime.SymbolRegion]) -> List[SWL.SymbolWithLine]:
    type_defintion = 1
    function_kind = 'Function'
    syntax_settings = self.get_syntax_settings()
    type_symbols = [
       SWL.SymbolWithLine(symbol, self.calculate_line(symbol.region), self.get_text_at_region(symbol.region), syntax_settings)
       for symbol in symbol_regions
       if symbol.type == type_defintion and symbol.kind[2] == function_kind
    ]
    return type_symbols

  def get_syntax_settings(self) -> Optional[SVS.SymbolViewSettingSyntax]:
    view_syntax = self.view.syntax()
    if view_syntax:
      syntax_of_file = view_syntax.name
      matches = [syntax.syntax_values for syntax in self.settings.syntaxes if syntax_of_file in syntax.syntax_values.syntax_names]
      return matches[0] if len(matches) > 0 else None
    else:
      return None

