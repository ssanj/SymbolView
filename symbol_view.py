import sublime
import sublime_plugin
import os

class SymbolWithLine:
  def __init__(self, symbol, line):
    self.symbol = symbol
    self.line = line

  def get_name(self):
    return self.symbol.name

  def get_type(self):
    return self.type

  def get_kind(self):
    return self.kind

  def get_syntax(self):
    return self.syntax

  def get_region(self):
    return self.region()

  def get_line(self):
    return self.line

  def __str__(self):
    name = self.get_name()
    line = self.get_line()
    return f"{name}:{line}"


class SymbolViewCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    symbol_regions = self.view.symbol_regions()
    functions = self.get_functions(symbol_regions)
    for f in functions:
      print(f)


  def calculate_line(self, region):
    (zero_based_line, col) = self.view.rowcol_utf8(region.begin())
    line = zero_based_line + 1
    return line


  def get_functions(self, symbol_regions):
    type_defintion = 1
    function_kind = 'Function'
    type_symbols = [SymbolWithLine(symbol, self.calculate_line(symbol.region)) for symbol in symbol_regions if symbol.type == type_defintion and symbol.kind[2] == function_kind]

    return type_symbols


