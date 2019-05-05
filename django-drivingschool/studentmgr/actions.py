import unicodecsv
from django.http import HttpResponse
from django.utils.formats import date_format


def export_students_as_csv_action():
    def export_students_as_csv(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=hongming_students.csv'

        writer = unicodecsv.writer(response, encoding='gbk')
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
            if obj.classType:
                row.append(obj.classType.name)
            else:
                row.append('-')
            row.append(obj.get_currentStage_display())
            row.append(date_format(obj.enrollDate, 'SHORT_DATETIME_FORMAT'))
            if obj.enroller:
                if obj.enroller.channel:
                    row.append(obj.enroller.channel.get_channelType_display())
                    row.append(obj.enroller.channel.name)
                else:
                    row.append('-')
                    row.append('-')
                row.append(obj.enroller.name)
            else:
                row.append('-')
                row.append('-')
                row.append('-')
            note = obj.note
            if note:
                note = note.replace('\n', ' ')
                note = note.replace('\r', ' ')
            row.append(note)
            writer.writerow(row)
        return response

    export_students_as_csv.short_description = '导出为电子表格'
    return export_students_as_csv


def export_fees_as_csv_action():
    def export_fees_as_csv(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=hongming_fees.csv'

        writer = unicodecsv.writer(response, encoding='utf-8')
        header = [
            '序号',
            '姓名',
            '证件号',
            '手机号',
            '驾照类型',
            '报名班型',
            '班型价格',
            '招生代表',
            '费用编号',
            '费用类型',
            '备注',
            '费用金额',
            '登记时间',
            '支付方式',
        ]
        writer.writerow(header)
        for obj in queryset:
            row = []
            row.append(obj.id)
            row.append(obj.student.name)
            row.append(obj.student.idNo)
            row.append(obj.student.mobile)
            row.append(obj.student.get_licType_display())
            row.append(obj.student.classType.name)
            row.append(obj.student.classType.price)
            row.append(obj.student.enroller.name)
            row.append(obj.feeId)
            row.append(obj.get_feeType_display())
            row.append(obj.note)
            row.append(obj.money)
            row.append(date_format(obj.createTime, 'SHORT_DATETIME_FORMAT'))
            row.append(obj.get_paymentMethod_display())
            writer.writerow(row)
        return response

    export_fees_as_csv.short_description = '导出为电子表格'
    return export_fees_as_csv
