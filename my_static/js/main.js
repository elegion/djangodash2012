function init_edit_testcase_form() {
    var btn = $('<button class="btn btn-mini"><i class="icon-pencil"></i></button>');
    btn.click(function(){
       $('.testcase-header').hide();
       $('.testcase-info-form').show();
    });
    if($('.testcase-info-form.js_show').length) {
        btn.click();
    }

    var delbtn = $('<button class="btn-delete-testcase btn btn-mini btn-danger"><i class="icon-trash icon-white"></i></button>');
    delbtn.click(function (){
        if(confirm('Really delete?')) {
            $('.delete_form').submit();
        }
    });

    $('.testcase-header small').before(btn);
    $('.testcase-header small').before(delbtn);
};

$(function(){
   init_edit_testcase_form();
});