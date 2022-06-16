from typing import Optional
from . import symbol_detail_setting as SDS
from . import symbol_detail as SD
import sublime

class SymbolWithLine:

  def __init__(self, symbol, line, text) -> None:
    self.symbol: sublime.SymbolRegion = symbol
    self.line: int = line
    self.name: str = symbol.name
    self.tpe: int = symbol.type
    self.kind: int = symbol.kind
    self.syntax: sublime.Syntax = symbol.syntax
    self.region: sublime.Region = symbol.region
    self.text: str = text
    self.symbol_details: SD.SymbolDetail = self.parse_function(text)


  def parse_function(self, text: str) -> SD.SymbolDetail:
    line_without_spaces = text.lstrip().rstrip()
    syntax_settings = self.get_syntax_settings()
    default_detail = SD.SymbolDetail(text.lstrip().rstrip())
    if syntax_settings:
      splits = line_without_spaces.split(syntax_settings.prefix)
      if len(splits) == 1: # does not match prefix
        return SD.SymbolDetail(splits[0])
      elif len(splits) == 2: # matched on prefix
        before = splits[0] # text before prefix
        after = splits[1] # text after prefix
        detail = after

        for end in syntax_settings.suffixes:
          detail = detail.rstrip() # remove any leading space
          if detail.endswith(end):
            detail = detail.replace(end, "")

        return SD.SymbolDetail(detail, None if len(before.lstrip()) == 0 else before.lstrip())
      else: # invalid number of splits
        return default_detail
    else:
      return default_detail

  def get_syntax_settings(self) -> Optional[SDS.SymbolDetailSetting]:
    syntax = self.syntax
    if syntax == "Scala" or syntax == "Scala-Sensory-Underload":
      return SDS.SymbolDetailSetting("def ", ["{", "="])
    elif syntax == "Rust":
      return SDS.SymbolDetailSetting("fn ", ["{"])
    elif syntax == "Python":
      return SDS.SymbolDetailSetting("def ", [":"])
    else:
      return None

  # def parse_function(self, text):
  #    # TODO: Make this customisable per syntax type
  #   function_reg = '^.*def\\s+([a-zA-Z0-9_]+\\(.*\\))(\\s*:[^=}]*)?'
  #   matches = re.match(function_reg, text)
  #   if matches and len(matches.groups()) > 0:
  #     if len(matches.groups()) == 1: # have only name + params
  #      groups = matches.groups()
  #      func_parameters = groups[0].lstrip()
  #      return func_parameters
  #     else: # have name + params + return type
  #      groups = matches.groups()
  #      func_parameters = groups[0].lstrip()
  #      maybe_return_type = groups[1]
  #      return_type = maybe_return_type.lstrip().rstrip() if maybe_return_type else ""
  #      return f"{func_parameters}{return_type}"
  #   else:
  #     return text.lstrip().rstrip() + "..."

  def __str__(self) -> str:
    name = self.name
    line = self.line
    text = self.text
    symbol_details = self.symbol_details
    return f"SymbolWithLine(name={name}, line={line}, text={text}, symbol_details={symbol_details})"

  def __repr__(self) -> str:
    return self.__str__()
