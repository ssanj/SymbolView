from typing import NamedTuple
from typing import Optional

class SymbolDetail(NamedTuple):
  detail: str
  annotation: Optional[str] = None
