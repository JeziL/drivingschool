import unicodecsv
from django.http import HttpResponse
from django.utils.formats import date_format


def export_students_as_csv_action():
    def export_students_as_csv(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=hongming_students.csv'

        writer = unicodecsv.writer(response, encoding='utf-8')
        header = [
            '序号',
            '姓名',
            '性别',
            '证件号',
            '手机号',
            '地址',
            '驾照类型',
            '报名班型',
            '当前状态',
            '录入日期',
            '渠道类型',
            '渠道名称',
            '招生代表',
            '备注',
        ]
        writer.writerow(header)
        for obj in queryset:
            row = []
            row.append(obj.id)
            row.append(obj.name)
            row.append(obj.get_sex_display())
            row.append(obj.idNo)
            row.append(obj.mobile)
            row.append(obj.addr)
            row.append(obj.get_licType_display())
            row.append(obj.classType.name)
            row.append(obj.get_currentStage_display())
            row.append(date_format(obj.enrollDate, 'SHORT_DATETIME_FORMAT'))
            row.append(obj.enroller.channel.get_channelType_display())
            row.append(obj.enroller.channel.name)
            row.append(obj.enroller.name)
            row.append(obj.note)
            writer.writerow(row)
        return response

    export_students_as_csv.short_description = '导出为电子表格'
    return export_students_as_csv
