import sublime_plugin
import sublime
import html
from typing import List
from typing import Optional
from . import symbol_with_line as SWL
from . import symbol_view_setting as SVS
from . import settings_loader as SL

class SymbolViewCommand(sublime_plugin.TextCommand):

  def run(self, edit: sublime.Edit) -> None:
    view = self.view
    selections = view.sel()
    selected_word = self.has_selected_word(selections)

    settings = sublime.load_settings("symbol_view.sublime-settings")
    settings_loader = SL.SettingsLoader(settings)
    self.settings = settings_loader.load_symbol_view_settings()
    print(self.settings)
    symbol_regions = view.symbol_regions()

    # TODO: Generalize for other types of symbols
    functions = self.get_functions(symbol_regions)

    user_selection_matches = [s for s in functions if s.name == selected_word]

    if len(user_selection_matches) > 0:
      user_selection = user_selection_matches[0]
      print(f"user selection: {user_selection}")
      view.run_command('goto_line', {'line': user_selection.line})
    else:
      window = view.window()

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

  def has_selected_word(self, selection: sublime.Selection) -> Optional[str]:
    if len(selection) > 0:
      view = self.view
      possible_word = view.substr(view.word(selection[0]))
      if possible_word and possible_word.lstrip():
        word = possible_word.lstrip()
      else:
        word = None
    else:
      word = None

    return word

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
       SWL.SymbolWithLine(self.fromSublimeSymbolRegion(symbol), syntax_settings)
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

  def fromSublimeSymbolRegion(self, sublime_region: sublime.SymbolRegion) -> SWL.SymbolRegion:
    line = SWL.SymbolRegionLine(self.calculate_line(sublime_region.region))
    text = SWL.SymbolRegionText(self.get_text_at_region(sublime_region.region))
    name = SWL.SymbolName(sublime_region.name)
    return SWL.SymbolRegion(line, text, name)

