$(document).ready(function () {
    var val = $('#id_applyType').val();
    if (val == 1) {
        $('.field-origLicType, .field-licChangeDate').show();
    } else {
        $('.field-origLicType, .field-licChangeDate').hide();
    }

    $('#id_applyType').change(function () {
        var val = this.value;
        if (val == 1) {
            $('.field-origLicType, .field-licChangeDate').slideDown('medium');
        } else {
            $('.field-origLicType, .field-licChangeDate').slideUp('medium');
        }
    });

    addPrintButton();
    $('div.add-row a').click(function () {
        var price_str = $('div.field-class_type_price p').text();
        $('div.field-money input').each(function () {
            if ($(this).val() === '') {
                $(this).val(price_str);
            }
        });
        addPrintButton();
    });
});

function addPrintButton() {
    $('div.dynamic-fee_set h3').each(function () {
        if ($(this).children().length === 3) {
            var feeId = $(this).children('span.inline_label').text();
            if (!feeId.match("^#")) {
                $(this).append("<input type='button' class='printBtn' style='float: right;' value='打印培训费' />");
            }
        }
    });
    $('input.printBtn').each(function () {
        $(this).unbind('click');
        $(this).click(onPrintBtnClicked);
    })
}

function onPrintBtnClicked(e) {
    var feeDiv = $(e.target).parent().parent();

    var dateStr = feeDiv.find('input.vDateField').val().replace(/\//g, "-");
    var feeId = feeDiv.find('span.inline_label').text();
    var enroller = $('select#id_enroller option:selected').text();
    var student = $('input#id_name').val();
    var stuId = $('input#id_idNo').val();
    var mobile = $('input#id_mobile').val();
    var licType = $('select#id_licType option:selected').text();
    var classType = $('select#id_classType option:selected').text();
    var money = feeDiv.find('div.field-money').find('input.vTextField').val();
    var payment = feeDiv.find('div.field-paymentMethod').find('select option:selected').text();
    var feeType = feeDiv.find('div.field-feeType').find('select option:selected').text();

    var note = feeDiv.find('div.field-note').find('input.vTextField').val();
    if (note !== "") {
        feeType = note;
    }

    printFee(dateStr, feeId, enroller, student, stuId, mobile, feeType, payment, classType, licType, money);
}

function printFee(date, feeId, enroller, name, stuId, mobile, feeType, payment, classType, licType, money) {
    var classTypeStr = classType + " " + licType;
    var moneyVal = parseFloat(money);
    var moneyUpStr = upDigit(moneyVal);
    console.log(moneyUpStr);
}

function upDigit(n) {
    var fraction = ['角', '分'];
    var digit = [
        '零',
        '壹',
        '贰',
        '叁',
        '肆',
        '伍',
        '陆',
        '柒',
        '捌',
        '玖'
    ];
    var unit = [
        [
            '元', '万', '亿'
        ],
        ['', '拾', '佰', '仟']
    ];
    var head = n < 0
        ? '欠'
        : '';
    n = Math.abs(n);

    var s = '';

    for (var i = 0; i < fraction.length; i++) {
        s += (digit[Math.floor(n * 10 * Math.pow(10, i)) % 10] + fraction[i]).replace(/零./, '');
    }
    s = s || '整';
    n = Math.floor(n);

    for (var i = 0; i < unit[0].length && n > 0; i++) {
        var p = '';
        for (var j = 0; j < unit[1].length && n > 0; j++) {
            p = digit[n % 10] + unit[1][j] + p;
            n = Math.floor(n / 10);
        }
        s = p.replace(/(零.)*零$/, '').replace(/^$/, '零') + unit[0][i] + s;
    }
    return head + s.replace(/(零.)*零元/, '元').replace(/(零.)+/g, '零').replace(/^整$/, '零元整');
}
