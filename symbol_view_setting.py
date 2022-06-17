from typing import NamedTuple
from typing import List

        # "syntax_names": ["Scala", "Scala-Sensory-Underload"],
        # "function_start": "def ",
        # "function_ends": ["{", "="],


class SymbolViewSettingSyntax(NamedTuple):
  syntax_names: List[str]
  function_start: str
  function_ends: List[str]

class SymbolViewSettingLabeledSyntax(NamedTuple):
  syntax_label: str
  syntax_values: SymbolViewSettingSyntax


class SymbolViewSetting(NamedTuple):
  max_line_length: int
  syntaxes: List[SymbolViewSettingLabeledSyntax] = []

