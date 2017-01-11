# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ProxyProxy(Base):
    __tablename__ = 'proxy_proxy'
    __table_args__ = (
        Index('proxy_proxy_addr_90457308_uniq', 'addr', 'port', 'type', unique=True),
    )

    id = Column(Integer, primary_key=True)
    addr = Column(String(20), nullable=False)
    port = Column(String(20), nullable=False)
    io = Column(Integer, nullable=False)
    locate = Column(String(100), nullable=False)
    level = Column(String(20), nullable=False)
    type = Column(String(20), nullable=False)
    live_time = Column(String(20))
    dateline = Column(DateTime, nullable=False)


class ProxyProxychecked(Base):
    __tablename__ = 'proxy_proxychecked'
    __table_args__ = (
        Index('proxy_proxychecked_site_id_fb66f63b_uniq', 'site_id', 'proxy_id', unique=True),
    )
    id = Column(Integer, primary_key=True)
    connect_time = Column(String(20))
    check_time = Column(DateTime)
    proxy_id = Column(ForeignKey(u'proxy_proxy.id'), nullable=False, index=True)
    site_id = Column(ForeignKey(u'proxy_targetsite.id'), nullable=False, index=True)

    proxy = relationship(u'ProxyProxy')
    site = relationship(u'ProxyTargetsite')


class ProxyTargetsite(Base):
    __tablename__ = 'proxy_targetsite'
    __table_args__ = (
        Index('proxy_targetsite_site_10aed6a7_uniq', 'site', 'site_name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    site = Column(String(100), nullable=False)
    site_name = Column(String(100), nullable=False)
    status = Column(Boolean, nullable=False)

__all__ = ('ProxyProxy', 'ProxyProxychecked', 'ProxyTargetsite')
