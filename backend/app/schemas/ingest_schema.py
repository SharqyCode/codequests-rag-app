from pydantic import BaseModel
from typing import List, Dict, Any


class ExternalSourceRequest(BaseModel):
    source_type: str
    data: List[Dict[str, Any]]