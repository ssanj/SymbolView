from typing import List
from typing import Optional

class SymbolDetailSetting:
  def __init__(self, prefix: str, suffixes: List[str]) -> None:
    self.prefix = prefix
    self.suffixes = suffixes


  def __str__(self) -> str:
    prefix = self.prefix
    suffixes = self.suffixes
    return f"SymbolDetailSetting(prefix={prefix}, suffixes={suffixes})"

  def __repr__(self) -> str:
    return self.__str__()

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
  #   return text

  def parse_function(self, text) -> str:
    line_without_spaces = text.lstrip().rstrip()
    syntax_settings = self.get_syntax_settings()
    if syntax_settings:
      splits = line_without_spaces.split(syntax_settings.prefix)
      if len(splits) == 1: # does not match prefix
        parameters_and_return = splits[0]
      elif len(splits) == 2: # matched on prefix
        before = splits[0] # text before prefix
        after = splits[1] # text after prefix
        parameters_and_return = after if len(before.lstrip()) == 0 else f"{before} {after}"
      else: # invalid number of splits
        return text.lstrip().rstrip()

      for end in syntax_settings.suffixes:
         if parameters_and_return.endswith(end):
          parameters_and_return = parameters_and_return.replace(end, "")

      return parameters_and_return
    else:
      return text.lstrip().rstrip()

  def get_syntax_settings(self) -> Optional[SymbolDetailSetting]:
    syntax = self.syntax
    if syntax == "Scala" or syntax == "Scala-Sensory-Underload":
      return SymbolDetailSetting("def ", ["{", "="])
    elif syntax == "Rust":
      return SymbolDetailSetting("fn ", ["{"])
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
    details = self.details
    return f"SymbolWithLine(name={name}, line={line}, text={text}, details={details})"

  def __repr__(self) -> str:
    return self.__str__()
