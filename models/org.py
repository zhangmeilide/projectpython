from sqlalchemy import Column, Integer, String,ForeignKey, TIMESTAMP,Boolean
from sqlalchemy.sql import func
from db import Base


class Org(Base):
    __tablename__ = "tb_org"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    org_name = Column(String(255), nullable=False, server_default="", comment="机构名称")
    org_alias = Column(String(255), nullable=True, comment="机构别名")
    parent_id = Column(Integer, ForeignKey("tb_org.id"), nullable=True, comment="父级机构ID")
    org_code = Column(String(255), nullable=True, comment="机构编号")
    org_level = Column(Integer, nullable=True, comment="机构级别")
    description = Column(String(255), nullable=False, server_default="", comment="机构描述")
    org_type = Column(Integer, nullable=True, comment="机构类型")
    order = Column(Integer, nullable=True, comment="排序")
    province_id = Column(Integer, nullable=False, server_default="0", comment="省ID")
    city_id = Column(Integer, nullable=False, server_default="0", comment="市ID")
    county_id = Column(Integer, nullable=False, server_default="0", comment="区县ID")
    street_id = Column(Integer, nullable=False, server_default="0", comment="第五级街道ID")
    road_id = Column(Integer, nullable=False, server_default="0", comment="第六级街道ID")
    area_id = Column(Integer, nullable=False, server_default="0", comment="区域ID")
    company_count = Column(Integer, nullable=False, server_default="0", comment="企业主体数")
    company_online_count = Column(Integer, nullable=False, server_default="0", comment="企业在网数")
    website_count = Column(Integer, nullable=False, server_default="0", comment="网站数")
    website_company_count = Column(Integer, nullable=False, server_default="0", comment="网站主体数")
    shop_count = Column(Integer, nullable=False, server_default="0", comment="网店数")
    shop_company_count = Column(Integer, nullable=False, server_default="0", comment="网店主体数")
    takeout_count = Column(Integer, nullable=False, server_default="0", comment="餐饮数")
    takeout_company_count = Column(Integer, nullable=False, server_default="0", comment="餐饮主体数")
    platform_count = Column(Integer, nullable=False, server_default="0", comment="平台数")
    platform_company_count = Column(Integer, nullable=False, server_default="0", comment="平台主体数")
    evidence_total_count = Column(Integer, nullable=False, server_default="0", comment="取证总次数")
    evidence_surplus_count = Column(Integer, nullable=False, server_default="0", comment="取证剩余次数")
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, nullable=True, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除时间")
    systems = Column(String(50), nullable=False, server_default="", comment="系统权限")
    unit_id = Column(Integer, nullable=False, server_default="1", comment="所属委办局")
    gxdw_code = Column(Integer, nullable=False, server_default="0", comment="管辖单位code")
    gxdw_name = Column(String(255), nullable=True, comment="管辖单位名称")
    gxdw_sjcode = Column(Integer, nullable=False, server_default="0", comment="管辖单位上级code")
    regorg_code = Column(Integer, nullable=False, server_default="0", comment="登记机关code")
    tsa_mobile_open_flag = Column(Boolean, nullable=False, server_default="1", comment="开通手机取证状态1：默认未开通 2：开通")
  