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

    var feeType = feeDiv.find('div.field-feeType').find('select option:selected').text();
    var note = feeDiv.find('div.field-note').find('input.vTextField').val();
    if (note !== "") {
        feeType = note;
    }

    var classType = $('select#id_classType option:selected').text();
    var money = feeDiv.find('div.field-money').find('input.vTextField').val();

    console.log(money);
}
