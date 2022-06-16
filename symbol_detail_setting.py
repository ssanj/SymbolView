from typing import List

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
