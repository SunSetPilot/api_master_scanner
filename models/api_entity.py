from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, JSON, LONGTEXT

from database.mysql import Base


class ApiEntity(Base):
    __tablename__ = 'api'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT)
    description = Column(String(255))
    method = Column(String(16))
    protocol = Column(String(16))
    path = Column(String(255))
    header_params = Column(JSON)
    query_params = Column(JSON)
    body_params = Column(LONGTEXT)
    response = Column(LONGTEXT)
