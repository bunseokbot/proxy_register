from sqlalchemy import Column, Integer, String
from route.db import Base

class Domain(Base):
    __tablename__ = "domain"
    idx = Column(Integer, primary_key=True)
    domain = Column(String(120), unique=True)
    ip = Column(String(15), unique=True)
    user = Column(String(120))

    def __init__(self, domain, ip, user):
        self.domain = domain
        self.ip = ip
        self.user = user
