from dataclasses import dataclass


@dataclass
class ApiInfo:
    path: str
    method: str
    hash: str
    header_params: dict
    query_params: dict
    body_params: str
    response: str
