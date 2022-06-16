import sublime_plugin
import sublime
import html
from . import symbol_with_line as SWL

class SymbolViewCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    symbol_regions = self.view.symbol_regions()
    # TODO: Generalize for other types of symbols
    functions = self.get_functions(symbol_regions)
    for f in functions:
     print(f)
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

  def on_symbol_selected(self, items, index) -> None:
    if index != -1 and len(items) > index:
      item = items[index]
      self.view.run_command('goto_line', {'line': item.line})

  def create_panel_items(self, items):
    return list(map(lambda content: self.create_symbol_with_line_panel(content), items))

  def create_symbol_with_line_panel(self, symbol_with_line):
    max_line_length = 100 # TODO: move to config
    search_text = symbol_with_line.name
    details = symbol_with_line.details
    truncated_details = details[:max_line_length]
    suffix = "..." if len(details) > max_line_length else ""
    detail_text = html.escape(truncated_details + suffix)
    line_number = symbol_with_line.line
    return sublime.QuickPanelItem(search_text, f"<u>{detail_text}</u> <strong>{line_number}</strong>", "", sublime.KIND_FUNCTION)

  def calculate_line(self, region):
    (zero_based_line, _) = self.view.rowcol_utf8(region.begin())
    line = zero_based_line + 1
    return line

  def get_text_at_region(self, region):
    line_region = self.view.full_line(region)
    return self.view.substr(line_region)

  def get_functions(self, symbol_regions):
    type_defintion = 1
    function_kind = 'Function'
    type_symbols = [
       SWL.SymbolWithLine(symbol, self.calculate_line(symbol.region), self.get_text_at_region(symbol.region))
       for symbol in symbol_regions
       if symbol.type == type_defintion and symbol.kind[2] == function_kind
    ]
    return type_symbols
