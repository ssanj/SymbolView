from typing import Optional
from . import symbol_detail_setting as SDS
from . import symbol_detail as SD
from . import symbol_view_setting as SVS
import sublime

class SymbolWithLine:

  def __init__(self, symbol: sublime.SymbolRegion, line: int, text: str, syntax_setting: Optional[SVS.SymbolViewSettingSyntax] = None) -> None:
    self.symbol = symbol
    self.line = line
    self.name: str = symbol.name
    self.tpe: int = symbol.type
    self.kind = symbol.kind # TODO: Find out this type
    self.syntax: sublime.Syntax = symbol.syntax
    self.region: sublime.Region = symbol.region
    self.text = text
    self.symbol_details: SD.SymbolDetail = self.parse_function(text, syntax_setting)
    self.syntax_setting = syntax_setting


  def parse_function(self, text: str, settings: Optional[SVS.SymbolViewSettingSyntax]) -> SD.SymbolDetail:
    line_without_spaces = text.lstrip().rstrip()
    syntax_settings = self.get_syntax_settings(settings)
    default_detail = SD.SymbolDetail(text.lstrip().rstrip())
    if syntax_settings:
      splits = line_without_spaces.split(syntax_settings.function_start)
      if len(splits) == 1: # does not match function start token
        return SD.SymbolDetail(splits[0])
      elif len(splits) == 2: # matched on function start token
        before = splits[0] # text before function start token
        after = splits[1] # text after function start token
        detail = after

        for end in syntax_settings.function_ends: # remove all ends and included spaces
          detail = detail.rstrip() # remove any leading space
          if detail.endswith(end):
            detail = detail.replace(end, "")

        annotation_hint = None if len(before.lstrip()) == 0 else before.lstrip()
        return SD.SymbolDetail(detail, annotation_hint)
      else: # invalid number of splits
        return default_detail
    else:
      return default_detail

  def get_syntax_settings(self, settings: Optional[SVS.SymbolViewSettingSyntax]) -> Optional[SDS.SymbolDetailSetting]:
    if settings:
       function_start = settings.function_start + " " # add a space to enable tokenizing
       function_ends = settings.function_ends
       return SDS.SymbolDetailSetting(function_start, function_ends)
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
