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

  def parse_function(self, text):
    return text

   # def parse_function(self, text):
   #   line_without_spaces = text.lstrip().rstrip()
   #   # TODO: Make this customisable per syntax type
   #   function_start = "def"
   #   function_ends = ["{", "="]
   #   parameters_and_return = line_without_spaces.replace(function_start, "") .lstrip()
   #   for end in function_ends:
   #       parameters_and_return = parameters_and_return.replace(end, "")
   #   return parameters_and_return

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
    return f"{name}:{line} -> {text} ->> {details}"

  def __repr__(self) -> str:
    return self.__str__()
