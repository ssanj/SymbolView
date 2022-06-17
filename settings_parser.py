from typing import List
from . import symbol_detail_setting as SDS

class SettingsParser:

  def get_syntaxes(self) -> List[SDS.SymbolDetailSetting]:
    return []

  def get_max_line_length(self) -> int:
    return 10

