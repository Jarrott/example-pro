# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20
"""
from flask import g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.data_scope import (admin_scope, company_scope, user_scope,
                                 literacy_scope, property_scope, merchants_cope,
                                 get_defualt)
from app.libs.error_code import AuthFailed, UserNotExistException
from app.libs.model_base import (db, Base,
                                 MixinModelJSONSerializer)

user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
)


class User(Base, MixinModelJSONSerializer):
    id = db.Column(db.Integer, primary_key=True, comment="用户自增ID")
    auth = db.Column(db.SmallInteger, default=100, comment="默认组")
    username = db.Column(db.String(24), unique=True, nullable=True, comment="用户名")
    nickname = db.Column(db.String(24), unique=True, nullable=False, comment="用户昵称")
    email = db.Column(db.String(30), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), comment="用户权限组")
    _image = db.Column('image', db.String(50), comment="图片地址")
    _password = db.Column('password', db.String(100), nullable=True, comment="用户密码")
    # 根据用户在网站上填写的内容生成的简历
    collect_jobs = db.relationship('Job', secondary=user_job)
    # 用户上传的简历或者简历链接
    resume = db.relationship('Resume', uselist=False)
    # 企业用户详情
    detail = db.relationship('CompanyDetail', uselist=False)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, filename):
        self._image = filename

    def _set_fields(self):
        """
        数据序列化要隐藏的字段
        """
        self._exclude = ['password']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def register_by_username(username, password, nickname):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.username = username
            user.password = password
            db.session.add(user)

    @staticmethod
    def verify(username, password):
        """
        验证用户的作用域
        """
        user = User.query.filter_by(username=username).first_or_404()
        if not user:
            raise UserNotExistException(message="当前用户不存在 ~ !")
        if not user.check_password(password):
            raise AuthFailed()
        is_auth = {
            777: admin_scope,
            755: company_scope,
            707: merchants_cope,
            706: property_scope,
            705: literacy_scope,
            100: user_scope
        }
        scope = is_auth.get(user.auth, get_defualt)()
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def change_password(old_password, new_password):
        """
        修改密码
        """
        uid = g.user.uid
        with db.auto_commit():
            user = User.query.get(uid)
            if not user:
                return False
            if user.check_password(old_password):
                user.password = new_password
                return True
            return False

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({
            'id': self.id
        }).decode('utf-8')


class Resume(Base, MixinModelJSONSerializer):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    job_experiences = db.relationship('JobExperience')
    edu_experiences = db.relationship('EduExperience')
    project_experiences = db.relationship('ProjectExperience')

    def profile(self):
        pass


class JobExperience(Base, MixinModelJSONSerializer):
    __tablename__ = 'job_experience'

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    company = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class EduExperience(Base, MixinModelJSONSerializer):
    __tablename__ = 'edu_experience'

    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(32), nullable=False)
    # 所学专业
    specialty = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(16))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class ProjectExperience(Base, MixinModelJSONSerializer):
    __tablename__ = 'preject_experience'

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    name = db.Column(db.String(32), nullable=False)
    # 在项目中扮演的角色
    role = db.Column(db.String(32))
    # 多个技术用逗号隔开
    technologys = db.Column(db.String(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


#
# class Resume(Base, MixinModelJSONSerializer):
#     __tablename__ = 'resume'
#
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
#     job_ex_id = db.Column(db.Integer, db.ForeignKey('job_experience.id', ondelete='CASCADE'))
#     edu_ex_id = db.Column(db.Integer, db.ForeignKey('edu_experience.id', ondelete='CASCADE'))
#     pro_ex_id = db.Column(db.Integer, db.ForeignKey('project_experience.id', ondelete='CASCADE'))
#
#     def profile(self):
#         pass
#
#
# class JobExperience(Base, MixinModelJSONSerializer):
#     __tablename__ = 'job_experience'
#
#     id = db.Column(db.Integer, primary_key=True)
#     begin_at = db.Column(db.DateTime)
#     end_at = db.Column(db.DateTime)
#     company = db.Column(db.String(32), nullable=False)
#     city = db.Column(db.String(32), nullable=False)
#     _rel_pro_experience = db.relationship('Resume',
#                                           collection_class=attribute_mapped_collection('edu_experience'),
#                                           cascade='all,delete-orphan',
#                                           backref='job_experience'
#                                           )
#     pro = association_proxy('_rel_pro_experience', 'resume')
#
#
# class EduExperience(Base, MixinModelJSONSerializer):
#     __tablename__ = 'edu_experience'
#
#     id = db.Column(db.Integer, primary_key=True)
#     begin_at = db.Column(db.DateTime)
#     end_at = db.Column(db.DateTime)
#     school = db.Column(db.String(32), nullable=False)
#     # 所学专业
#     specialty = db.Column(db.String(32), nullable=False)
#     degree = db.Column(db.String(16))
#
#     _rel_pro_experience = db.relationship('Resume',
#                                           collection_class=attribute_mapped_collection('job_experience'),
#                                           cascade='all,delete-orphan',
#                                           backref='edu_experience'
#                                           )
#     pro = association_proxy('_rel_pro_experience', 'resume')
#
#
# class ProjectExperience(Base, MixinModelJSONSerializer):
#     __tablename__ = 'project_experience'
#
#     id = db.Column(db.Integer, primary_key=True)
#     begin_at = db.Column(db.DateTime)
#     end_at = db.Column(db.DateTime)
#     name = db.Column(db.String(32), nullable=False)
#     # 在项目中扮演的角色
#     role = db.Column(db.String(32))
#     # 多个技术用逗号隔开
#     technologys = db.Column(db.String(64))
#     resumes = db.relationship('Resume', backref='project_experience')


class CompanyDetail(Base, MixinModelJSONSerializer):
    __tablename__ = 'company_detail'

    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(256), nullable=False)
    site = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    # 一句话描述
    description = db.Column(db.String(100))
    # 关于我们，公司详情描述
    about = db.Column(db.String(1024))
    # 公司标签，多个标签用逗号隔开，最多10个
    tags = db.Column(db.String(128))
    # 公司技术栈，多个技术用逗号隔开，最多10个
    stack = db.Column(db.String(128))
    # 团队介绍
    team_introduction = db.Column(db.String(256))
    # 公司福利，多个福利用分号隔开，最多 10 个
    welfares = db.Column(db.String(256))
    # 公司领域
    field = db.Column(db.String(128))
    # 融资进度
    finance_stage = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', backref=db.backref('company_detail', uselist=False))


class Job(Base, MixinModelJSONSerializer):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    # 职位名称
    name = db.Column(db.String(24))
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(24))
    description = db.Column(db.String(1500))
    # 职位标签，多个标签用逗号隔开，最多10个
    tags = db.Column(db.String(128))
    experience_requirement = db.Column(db.String(32))
    degree_requirement = db.Column(db.String(32))
    is_fulltime = db.Column(db.Boolean, default=True)
    # 是否在招聘
    is_open = db.Column(db.Boolean, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('job', lazy='dynamic'))
    views_count = db.Column(db.Integer, default=0)
    is_disable = db.Column(db.Boolean, default=False)

    @property
    def tag_list(self):
        return self.tags.split(',')

    @property
    def current_user_is_applied(self):
        d = Delivery.query.filter_by(job_id=self.id, user_id=g.user.uid).first()
        return d is not None


class Delivery(Base, MixinModelJSONSerializer):
    __tablename__ = 'delivery'

    # 等待企业审核
    STATUS_WAITING = 1
    # 被拒绝
    STATUS_REJECT = 2
    # 被接收，等待通知面试
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    company_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)
    # 企业回应
    response = db.Column(db.String(256))

    @property
    def user(self):
        return User.query.get(self.user_id)

    @property
    def job(self):
        return Job.query.get(self.job_id)


class AdminAuth(Base, MixinModelJSONSerializer):
    """权限模快"""
    id = db.Column(db.Integer, primary_key=True, comment="权限自增ID")
    auth_name = db.Column(db.String(100), comment="权限名称")
    url = db.Column(db.String(200), comment="权限地址")
    auth = db.relationship('Module')
    sec_module_id = db.Column(db.Integer, db.ForeignKey('sec_module.id'))
    module = db.relationship('SecModule', uselist=False)


class Role(Base, MixinModelJSONSerializer):
    """角色模块"""
    id = db.Column(db.Integer, primary_key=True, comment="自增ID")
    name = db.Column(db.String(100), unique=True, comment="角色名")
    auth = db.Column(db.String(255), comment="权限列表")
    role = db.relationship("User", backref='role')


class SecModule(Base, MixinModelJSONSerializer):
    """二级菜单"""
    id = db.Column(db.Integer, primary_key=True, comment="自增ID")
    name = db.Column(db.String(100), unique=True, comment="角色名")


class Module(Base, MixinModelJSONSerializer):
    """三级菜单"""
    id = db.Column(db.Integer, primary_key=True, comment="自增ID")
    name = db.Column(db.String(100), unique=True, comment="角色名")
    auth_id = db.Column(db.Integer, db.ForeignKey('admin_auth.id'))
    sec_module_id = db.Column(db.Integer, db.ForeignKey('sec_module.id'))
    module = db.relationship('SecModule', uselist=False)

