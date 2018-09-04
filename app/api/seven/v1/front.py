# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/22 
"""
from flask import g, jsonify

from app.libs.model_base import db
from app.libs.token_auth import auth
from app.libs.redprint import Redprint
from app.validators.front import JobExperienceForm, EduExperienceForm,ProjectExperienceForm
from app.api.seven.models.user import JobExperience, User, EduExperience, Resume,ProjectExperience

api = Redprint('front')


@api.route('/get/resume', methods=['GET'])
@auth.login_required
def get_resume():
    data = Resume.query.filter_by(user_id=g.user.uid).first_or_404()
    return jsonify({'job_experience': data['job_experiences']})


@api.route('/add/resume', methods=['POST'])
@auth.login_required
def add_resume():
    data = Resume()
    with db.auto_commit():
        data.user_id = g.user.uid
        db.session.add(data)
    return jsonify({'message': '可以创建简历了'})


@api.route('/add/job_experience', methods=['POST'])
@auth.login_required
def add_job_experience():
    form = JobExperienceForm().validate_for_api()
    with db.auto_commit():
        data = JobExperience()
        ss = Resume.query.filter_by(user_id=g.user.uid).first_or_404()
        data.resume_id = ss.id
        form.populate_obj(data)
        db.session.add(data)
    return jsonify({'message': '工作经历添加成功!'})


@api.route('/add/edu_experience', methods=['POST'])
@auth.login_required
def add_edu_experience():
    form = EduExperienceForm().validate_for_api()
    with db.auto_commit():
        data = EduExperience()
        ss = Resume.query.filter_by(user_id=g.user.uid).first_or_404()
        data.resume_id = ss.id
        form.populate_obj(data)
        db.session.add(data)
    return jsonify({'message': '教育经历添加成功!'})


@api.route('/add/pro_experience', methods=['POST'])
@auth.login_required
def add_pro_experience():
    form = ProjectExperienceForm().validate_for_api()
    with db.auto_commit():
        data = ProjectExperience()
        ss = Resume.query.filter_by(user_id=g.user.uid).first_or_404()
        data.resume_id = ss.id
        form.populate_obj(data)
        db.session.add(data)
    return jsonify({'message': '工作经历添加成功!'})
