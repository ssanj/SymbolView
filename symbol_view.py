import sublime
import sublime_plugin
import os

class SymbolWithLine:

  def __init__(self, symbol, line) -> None:
    self.symbol = symbol
    self.line = line
    self.name = symbol.name
    self.tpe = symbol.type
    self.kind = symbol.kind
    self.syntax = symbol.syntax
    self.region = symbol.region

  def __str__(self) -> str:
    name = self.name
    line = self.line
    return f"{name}:{line}"


class SymbolViewCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    symbol_regions = self.view.symbol_regions()
    # TODO: Generalize for other types of symbols
    functions = self.get_functions(symbol_regions)
    window = self.view.window()
    if window:
      panel_items = self.create_panel_items(functions)
      window.show_quick_panel(
        items = panel_items,
        on_select = lambda index: self.on_symbol_selected(functions, index),
        placeholder = "Functions: {}".format(len(panel_items)),
      )

  def on_symbol_selected(self, items, index) -> None:
    if index != -1 and len(items) > index:
      item = items[index]
      self.view.show_at_center(item.region)

  def create_panel_items(self, items):
    return list(map(lambda content: self.create_symbol_with_line_panel(content), items))


  def create_symbol_with_line_panel(self, symbol_with_line):
    return sublime.QuickPanelItem(symbol_with_line.name, "<u>{}:{}</u>".format(symbol_with_line.name, symbol_with_line.line), "", sublime.KIND_FUNCTION)

    # for f in functions:
    #   print(f)

  def calculate_line(self, region):
    (zero_based_line, col) = self.view.rowcol_utf8(region.begin())
    line = zero_based_line + 1
    return line

  def get_functions(self, symbol_regions):
    type_defintion = 1
    function_kind = 'Function'
    type_symbols = [
        SymbolWithLine(symbol, self.calculate_line(symbol.region))
        for symbol in symbol_regions
        if symbol.type == type_defintion and symbol.kind[2] == function_kind
    ]

    return type_symbols
