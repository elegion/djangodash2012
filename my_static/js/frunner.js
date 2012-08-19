"use strict";

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

    $('pre code').each(function(i, e) {
      var $e = $(e),
          language = hljs.highlightAuto($e.text()).language;
      if (language == 'json') {
        $e.text(vkbeautify.json($e.text()));
      } else if (language == 'xml' || language == 'html') {
        $e.text(vkbeautify.xml($e.text()));
      }
      hljs.highlightBlock(e);
    });
  }
};
