function init_edit_testcase_form() {
    var btn = $('<button class="btn btn-mini"><i class="icon-pencil"></i></button>');
    btn.click(function(){
       $('.testcase-header').hide();
       $('.testcase-info-form').show();
    });
    $('.testcase-header small').before(btn);
    if($('.testcase-info-form.js_show').length()) {
        btn.click();
    }
};

$(function(){
   init_edit_testcase_form();
});