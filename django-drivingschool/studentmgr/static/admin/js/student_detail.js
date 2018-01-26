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
            $(this).append("<input type='button' class='printBtn' style='float: right;' value='打印培训费' />");
        }
    });
    $('input.printBtn').each(function () {
        $(this).unbind('click');
        $(this).click(onPrintBtnClicked);
    })
}

function onPrintBtnClicked() {
    console.log("button click.");
}
