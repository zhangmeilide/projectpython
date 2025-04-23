from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, SmallInteger,DateTime
from db import Base

class Website(Base):
    __tablename__ = 'tb_website'
    __table_args__ = {'comment': '网站表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    website_name = Column(String(128), comment='网站名称')
    domain = Column(String(255), comment='域名')
    website_url = Column(String(1000), nullable=False, comment='链接')
    website_licence = Column(String(255), comment='网站备案信息')
    company_id = Column(Integer, nullable=False, server_default='0', comment='主体id')
    province = Column(String(128), comment='省')
    province_id = Column(Integer, nullable=False, server_default='0', comment='省id')
    city = Column(String(128), comment='城市')
    city_id = Column(Integer, nullable=False, server_default='0', comment='市机构id')
    county = Column(String(128), comment='区县')
    county_id = Column(Integer, nullable=False, server_default='0', comment='区机构id')
    area_id = Column(Integer, nullable=False, server_default='0', comment='区域id')
    street_id = Column(Integer, nullable=False, server_default='0', comment='所属街道id')
    company_name = Column(String(255), comment='主体名称')
    created_at = Column(TIMESTAMP, comment='创建时间')
    updated_at = Column(TIMESTAMP, comment='修改时间')
    deleted_at = Column(TIMESTAMP, comment='删除时间')
    label_names = Column(String(500), nullable=False, server_default='', comment='标签名称')
    unusual_flag = Column(SmallInteger, nullable=False, server_default='1', comment='1：正常  2：异常')
    collect_flag = Column(SmallInteger, nullable=False, server_default='0', comment='1：收藏')
    licence_flag = Column(SmallInteger, nullable=False, server_default='0', comment='亮照标识')
