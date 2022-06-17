from typing import List

class SymbolDetailSetting:
  def __init__(self, function_start: str, function_ends: List[str]) -> None:
    self.function_start = function_start
    self.function_ends = function_ends

  def __str__(self) -> str:
    function_start = self.function_start
    function_ends = self.function_ends
    return f"SymbolDetailSetting(function_start={function_start}, function_ends={function_ends})"

  def __repr__(self) -> str:
    return self.__str__()
