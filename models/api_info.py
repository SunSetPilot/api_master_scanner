from dataclasses import dataclass
from typing import List


@dataclass
class ApiParamsInfo:
    name: str
    type: str
    position: int


@dataclass
class ApiInfo:
    path: str
    method: str
    params: List[ApiParamsInfo]
    repo_url: str
    repo_branch: str
