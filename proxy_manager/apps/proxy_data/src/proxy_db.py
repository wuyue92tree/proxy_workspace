# coding: utf-8
from sqlalchemy import Text
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, \
    String
from sqlalchemy.orm import relationship
from crwy.utils.sql.db import Base


class ProxyDataCheckdomain(Base):
    __tablename__ = 'proxy_data_checkdomain'

    id = Column(Integer, primary_key=True)
    domain = Column(String(255), nullable=False)
    check_url = Column(Text, nullable=False)
    status = Column(Boolean, nullable=False)
    site_id = Column(ForeignKey(u'proxy_data_targetsite.id'), nullable=False,
                     index=True)

    site = relationship(u'ProxyDataTargetsite')


class ProxyDataProxy(Base):
    __tablename__ = 'proxy_data_proxy'
    __table_args__ = (
        Index('proxy_data_proxy_addr_port_type_197accf1_uniq', 'addr', 'port',
              'type', unique=True),
    )

    id = Column(Integer, primary_key=True)
    source = Column(String(255), nullable=False)
    addr = Column(String(255), nullable=False)
    port = Column(String(255), nullable=False)
    io = Column(Integer, nullable=False)
    locate = Column(String(255), nullable=False)
    level = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    live_time = Column(String(255))
    dateline = Column(DateTime, nullable=False)


class ProxyDataProxychecked(Base):
    __tablename__ = 'proxy_data_proxychecked'
    __table_args__ = (
        Index('proxy_data_proxychecked_domain_id_proxy_id_ec88ab81_uniq',
              'domain_id', 'proxy_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    connect_time = Column(String(20))
    check_time = Column(DateTime)
    domain_id = Column(ForeignKey(u'proxy_data_checkdomain.id'),
                       nullable=False, index=True)
    proxy_id = Column(ForeignKey(u'proxy_data_proxy.id'), nullable=False,
                      index=True)

    domain = relationship(u'ProxyDataCheckdomain')
    proxy = relationship(u'ProxyDataProxy')


class ProxyDataTargetsite(Base):
    __tablename__ = 'proxy_data_targetsite'

    id = Column(Integer, primary_key=True)
    site_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Boolean, nullable=False)


__all__ = ('ProxyDataCheckdomain', 'ProxyDataProxy',
           'ProxyDataProxychecked', 'ProxyDataTargetsite')
