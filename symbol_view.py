import sublime_plugin
import sublime
import re

class SymbolWithLine:
  def __init__(self, symbol, line, text) -> None:
    self.symbol = symbol
    self.line = line
    self.name = symbol.name
    self.tpe = symbol.type
    self.kind = symbol.kind
    self.syntax = symbol.syntax
    self.region = symbol.region
    self.text = text
    self.details = self.parse_function(text)

   # def parse_function(self, text):
   #   line_without_spaces = text.lstrip().rstrip()
   #   # TODO: Make this customisable per syntax type
   #   function_start = "def"
   #   function_ends = ["{", "="]
   #   parameters_and_return = line_without_spaces.replace(function_start, "") .lstrip()
   #   for end in function_ends:
   #       parameters_and_return = parameters_and_return.replace(end, "")
   #   return parameters_and_return

  def parse_function(self, text):
     # TODO: Make this customisable per syntax type
    function_reg = '^.*def\\s+([a-zA-Z0-9_]+\\(.*\\))(\\s*:[^=}]*)?'
    matches = re.match(function_reg, text)
    if matches and len(matches.groups()) > 0:
      if len(matches.groups()) == 1: # have only name + params
       groups = matches.groups()
       func_parameters = groups[0].lstrip()
       return func_parameters
      else: # have name + params + return type
       groups = matches.groups()
       func_parameters = groups[0].lstrip()
       maybe_return_type = groups[1]
       return_type = maybe_return_type.lstrip().rstrip() if maybe_return_type else ""
       return f"{func_parameters}{return_type}"
    else:
      return text.lstrip().rstrip() + "..."

  def __str__(self) -> str:
    name = self.name
    line = self.line
    text = self.text
    details = self.details
    return f"{name}:{line} -> {text} ->> {details}"

  def __repr__(self) -> str:
    return self.__str__()

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
    return sublime.QuickPanelItem("f:"+ symbol_with_line.details, "<u>{}:{}</u>".format(symbol_with_line.name, symbol_with_line.line), "", sublime.KIND_FUNCTION)

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
       SymbolWithLine(symbol, self.calculate_line(symbol.region), self.get_text_at_region(symbol.region))
       for symbol in symbol_regions
       if symbol.type == type_defintion and symbol.kind[2] == function_kind
    ]
    return type_symbols
