"use strict";

Fortuitus.frunner = {
  TEST_PROGRESS_UPDATE_INTERVAL: 1000,
  _progress_need_html: false,

  /**
   * Initializes TestRun screen
   */
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
  },

  /**
   * Starts AJAX progress watcher for pending TestRun
   */
  startProgressWatch: function(need_html) {
    Fortuitus.frunner._progress_need_html = need_html;
    $('.js_toggle_request, .js_toggle_response').hide();
    setTimeout(Fortuitus.frunner._updateTestProgress, Fortuitus.frunner.TEST_PROGRESS_UPDATE_INTERVAL);
  },

  /**
   * Performs ajax requests for TestRun progress information
   * @private
   */
  _updateTestProgress: function() {
    $.getJSON(document.location, {'html': Fortuitus.frunner._progress_need_html}, function(data) {
      console.log(data);

      // Update current testcase results, if finished
      if (data.html) {
        Fortuitus.frunner._progress_need_html = undefined;
        $('.js_testcase_wrapper').html(data.html);
        Fortuitus.frunner.initTestrun();
      }
      // Update sidebar's testcases statuses
      for (var key in data.testcase_statuses) {
        if (data.testcase_statuses.hasOwnProperty(key)) {
          console.log(key, data.testcase_statuses[key])
          $('.js-testcase-list-' + key)
              .removeClass('result-pending result-success result-error result-fail result-')
              .addClass('result-' + data.testcase_statuses[key]);
        }
      }
      // Update favicon, if finished. Else - request new progress information
      if (data.testrun_status != 'pending') {
        var $favicon = $('link[rel=icon]'),
            $testrun_name = $('.js-testrun-human-name');
        if (data.testrun_status == 'success') {
          $favicon.attr('href', $favicon.attr('href').replace('_pending', ''));
        } else {
          $favicon.attr('href', $favicon.attr('href').replace('_pending', '_fail'));
        }
        $testrun_name
            .text($testrun_name.text().replace(/\(.*\)/, '(' + data.testrun_status + ')'))
            .removeClass('result-pending');
      } else {
        setTimeout(Fortuitus.frunner._updateTestProgress, Fortuitus.frunner.TEST_PROGRESS_UPDATE_INTERVAL);
      }
    });
  }
};
