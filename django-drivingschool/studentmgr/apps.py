from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class StudentmgrConfig(AppConfig):
    name = 'studentmgr'
    verbose_name = '驾校'


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
    menu = (
        ParentItem('人员管理', children=[
            ChildItem('学员报名', url='admin:studentmgr_student_add'),
            ChildItem('学员管理', model='studentmgr.student'),
            ChildItem('用户管理', model='auth.user')
        ]),
        ParentItem('教学管理', children=[
            ChildItem('班型管理', model='studentmgr.classtype'),
            ChildItem('教练管理', model='studentmgr.coach')
        ]),
        ParentItem('考务管理', children=[
            ChildItem('考试计划', model='studentmgr.exam'),
            ChildItem('考试成绩', model='studentmgr.grade')
        ]),
        ParentItem('招生管理', children=[
            ChildItem('渠道管理', model='studentmgr.channel')
        ]),
        ParentItem('车辆管理', children=[
            ChildItem('车辆信息', model='studentmgr.vehicle'),
            ChildItem('车辆加油', model='studentmgr.fuel'),
            ChildItem('车辆维修', model='studentmgr.maintenance'),
            ChildItem('车辆保险', model='studentmgr.insurance'),
            ChildItem('车辆年审', model='studentmgr.examination'),
        ]),
        ParentItem('财务管理', children=[
            ChildItem('费用登记', model='studentmgr.student'),
            ChildItem('费用查询', model='studentmgr.fee')
        ])
    )
