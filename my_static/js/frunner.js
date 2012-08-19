Fortuitus.frunner = {
  initTestrun: function() {
    $('.js_toggle_request').click(function() {
      $(this).parents('li').find('.js_request_wrapper').slideToggle();
      return false;
    });
    $('.js_toggle_response').click(function() {
      $(this).parents('li').find('.js_response_wrapper').slideToggle();
      return false;
    });
  }
}