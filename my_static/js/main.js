Fortuitus = {};

Fortuitus.initEditTestcaseForm = function() {
    var btn = $('<button class="btn btn-mini"><i class="icon-pencil"></i></button>');
    btn.click(function() {
        $('.testcase-header').hide();
        $('.testcase-info-form').show();
    });
    if ($('.testcase-info-form.js_show').length) {
        btn.click();
    }

    var delbtn = $('<button class="btn-delete-testcase btn btn-mini btn-danger"><i class="icon-trash icon-white"></i></button>');
    delbtn.click(function() {
        if (confirm('Really delete?')) {
            $('.delete_form').submit();
        }
    });

    $('.testcase-header small').before(btn);
    $('.testcase-header small').before(delbtn);
};

Fortuitus.initEditTestStep = function() {
    $('.teststeps .head').each( function() {
        var $this = $(this);
        var btn = $('<button class="btn btn-mini btn-edit-testcase"><i class="icon-pencil"></i></button>');
        btn.click(function() {
            EditableTable.editMode($this.closest('form'), true);
            $this.parent().find('.js_edit').show();
            $this.parent().find('.js_show').hide();
            btn.hide();
            return false;
        });

        $this.append(btn);
    });

    var $form = $('.add_step_form');
    EditableTable.editMode($form, true);
    $form.find('.js_edit').show();
    $form.find('.js_show').hide();

    $('.add-test').click(function(){
        $('.add_step_form').show();
        return false;
    });
    $('.btn-cancel-add').click(function(){
        $('.add_step_form').hide();
        return false;
    });
};

Fortuitus.initEditAssert = function() {
    $('.js-btn-add-assert').click(function(){
        $('.js-add-assert-form').show();
        return false;
    });
    $('.js-btn-cancel-assert').click(function(){
        $('.js-add-assert-form').hide();
        return false;
    });
}
