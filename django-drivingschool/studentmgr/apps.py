from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class StudentmgrConfig(AppConfig):
    name = 'studentmgr'
    verbose_name = '驾校'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
