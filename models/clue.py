from sqlalchemy import Column, Integer, String,Text,Float,SmallInteger,DateTime,TIMESTAMP,ForeignKey
from sqlalchemy.orm import relationship
from db import Base
class Clue(Base):
    __tablename__ = "tb_clue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False, default=0, comment="任务id")
    clue_target_id = Column(Integer, nullable=False, default=0, comment="线索存储地id 结合data_source")
    status = Column(SmallInteger, nullable=False, default=0, comment="线索状态 0:未处理 1：已处理")
    disposal_confirm_flag = Column(SmallInteger, nullable=False, default=3, comment="是否被选进结案线索")
    clue_disposal_id = Column(Integer, nullable=False, default=0, comment="线索处置id 结合clue_disposal")
    disposal_id = Column(Integer, default=0, comment="处置id")
    behavior_id = Column(Integer, nullable=False, default=0, comment="违法行为id")
    behavior_name = Column(String(200), default="", comment="违法行为")
    data_source = Column(SmallInteger, nullable=False, default=1, comment="线索存储来源")
    work_source_flag = Column(SmallInteger, nullable=False, comment="线索业务来源")
    clue_type_id = Column(SmallInteger, nullable=False, default=0, comment="线索类型id")
    clue_url = Column(String(255), nullable=False, default="", comment="线索网址")
    clue_name = Column(String(255), nullable=False, default="", comment="线索名称")
    company_id = Column(Integer, default=0, comment="企业id")
    company_name = Column(String(255), default="", comment="企业名称")
    org_id = Column(Integer, nullable=False, default=0, comment="当前所属管辖单位")
    dept_id = Column(Integer, nullable=False, default=0, comment="当前所属部门id")
    user_id = Column(Integer, nullable=False, default=0, comment="当前所属人")
    judge_id = Column(Integer, nullable=False, default=0, comment="判定id")
    judge_user_id = Column(Integer, nullable=False, default=0, comment="判定uid")
    remark = Column(String(255), nullable=False, default="", comment="备注")
    law_name = Column(String(255), nullable=False, default="", comment="疑似违法分类")
    is_illegal = Column(SmallInteger, default=None, comment="是否违法")
    law_id = Column(Integer, nullable=False, default=0, comment="法律id")
    rule_content = Column(String(255), nullable=False, default="", comment="疑似违法内容")
    judge_describe = Column(String(500), default="", comment="检查描述")
    current_assign_id = Column(Integer, nullable=False, default=0, comment="目前所处分派流程id")
    work_source = Column(String(50), nullable=False, default="", comment="线索业务来源")
    updated_at = Column(DateTime, comment="修改时间")
    deleted_at = Column(DateTime, comment="删除时间")
    created_at = Column(DateTime, comment="创建时间")
    clue_behavior_id = Column(Integer, nullable=False, comment="线索可疑违法行为id")
    clue_behavior_name = Column(String(150), default=None, comment="线索可疑违法行为名称")
    clue_behavior_content = Column(String(500), default="", comment="线索可疑违法行为描述")
    clue_keyword = Column(String(500), default="", comment="线索关键词")
    illegal_judge_id = Column(Integer, nullable=False, default=0, comment="违法判定id")
    illegal_judge_user_id = Column(Integer, nullable=False, default=0, comment="违法判定uid")
    illegal_judge_org_id = Column(Integer, nullable=False, default=0, comment="违法判定机构id")
    evidence_tsa_status = Column(SmallInteger, nullable=False, default=3, comment="时间戳固证状态")
    evidence_seria_no = Column(String(100), default="", comment="证据唯一标示")
    evidence_tsa_id = Column(Integer, nullable=False, default=0, comment="时间戳固证id")
    evidence_type_name = Column(String(100), default="", comment="证据类型名称")
    evidence_source = Column(SmallInteger, nullable=False, default=1, comment="取证来源")
    unusual_type = Column(SmallInteger, nullable=False, default=1, comment="异常类型")
    feedback_content = Column(String(300), default=None, comment="反馈内容")
    feedback_file = Column(String(300), default=None, comment="反馈文件")
    feedback_flag = Column(SmallInteger, default=0, comment="是否反馈")
    feedback_user = Column(Integer, default=0, comment="反馈人")
    feedback_time = Column(DateTime, comment="反馈时间")
    data_import_log_id = Column(Integer, default=0, comment="导入线索id")
    behavior_keywords = Column(String(500), default="", comment="行为关键词")
    clue_goods_name = Column(String(255), default=None, comment="线索商品名称")
    clue_goods_category = Column(String(255), default=None, comment="线索商品分类")
    ad_illegal_postion = Column(String(255), default=None, comment="广告违法对象")
    original_org_id = Column(Integer, default=0, comment="原始所属管辖单位")
    original_dept_id = Column(Integer, default=0, comment="原始所属部门id")
    original_user_id = Column(Integer, default=0, comment="原始所属人")
    clue_disposal_confirm_flag = Column(SmallInteger, default=0, comment="处置确认状态")
    clue_case_id = Column(Integer, default=0, comment="案件反馈信息id")
    create_org_id = Column(Integer, default=0, comment="创建单位")
    create_dept_id = Column(Integer, default=0, comment="创建部门id")
    create_user_id = Column(Integer, default=0, comment="创建人")
    clue_flag = Column(SmallInteger, default=0, comment="线索标示")
    evidence_origin_url = Column(String(500), default="", comment="证据地址")
    category_name = Column(String(100), default="", comment="线索类别")
    rule_id = Column(Integer, default=0, comment="法规id")
    rule_name = Column(String(100), default="", comment="法规名称")
    behavior_describe = Column(String(500), default="", comment="违规说明")
    evidence_img = Column(String(500), default="", comment="截图")
    behavior_one_name = Column(String(500), default="", comment="违法行为一级分类名称")
    behavior_one_id = Column(Integer, default=0, comment="违法行为一级分类id")
    task_category_id = Column(Integer, default=0, comment="任务分类")
    dataclear_flag = Column(SmallInteger, default=0, comment="数据清除标识")
    is_accept = Column(SmallInteger, default=-1, comment="广告线索是否接收")
    illegal_flag = Column(SmallInteger, default=None, comment="违法标志")

    # 一对多关系，关联 tb_clue_org
    clue_org = relationship('ClueOrg', back_populates='clue', cascade="all, delete-orphan")

class ClueOrg(Base):
    __tablename__ = 'tb_clue_org'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    clue_id = Column(Integer, ForeignKey('tb_clue.id'), nullable=False, default=0, comment='线索id 关联clue表')  # 外键定义
    clue_type_id = Column(Integer, nullable=False, default=0, comment='线索类型id')
    org_id = Column(Integer, nullable=False, default=0, comment='机构id')
    dept_id = Column(Integer, nullable=True, comment='部门id')
    created_at = Column(TIMESTAMP, nullable=True, default=None, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=True, default=None, comment='更新时间')
    deleted_at = Column(TIMESTAMP, nullable=True, default=None, comment='删除时间')
    assign_status = Column(Integer, nullable=True, default=1000, comment='线索最终流转状态')
    disposal_access_flag = Column(Integer, nullable=True, default=0, comment='处置按钮是否显示 0不显示 1显示')
    disposaledit_access_flag = Column(Integer, nullable=True, default=0, comment='修改处置按钮是否显示 0不显示 1显示')
    feedback_access_flag = Column(Integer, nullable=True, default=0, comment='反馈按钮是否显示 0不显示 1显示')
    back_access_flag = Column(SmallInteger, nullable=True, default=0, comment='退回按钮 1显示 0不显示')
    clue_disposal_flag = Column(SmallInteger, nullable=True, default=0, comment='1 已处置 0 未处置')
    task_category_id = Column(Integer, nullable=True, default=0, comment='线索任务大分类id')
    clue_task_id = Column(Integer, nullable=True, default=0, comment='线索任务id')
    company_id = Column(Integer, nullable=True, comment='主体id')
    work_source_flag = Column(SmallInteger, nullable=True, comment='线索来源')
    task_type = Column(SmallInteger, nullable=True, default=0, comment='任务类型')
    create_org_id = Column(Integer, nullable=True, default=0, comment='线索创建机构')
    create_dept_id = Column(Integer, nullable=True, default=0, comment='线索创建部门')
    create_user_id = Column(Integer, nullable=True, default=0, comment='线索创建人')
    clue_assign_id = Column(Integer, nullable=True, default=0, comment='关联的分派id')
    clue_assign_at = Column(TIMESTAMP, nullable=True, default=None, comment='分派时间或退回时间')

    # 多对一关系，关联 tb_clue
    clue = relationship('Clue', back_populates='clue_org')











