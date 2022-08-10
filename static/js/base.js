/* jshint esversion: 8, jquery: true, scripturl: true */
$(document).ready(function () {
  $('.carousel').carousel();
  // set bootstrap carousel to stop autoplaying
  $('.carousel').carousel({
    ride: true
  });
  // Function controls messages's display
  setTimeout(() => {
    let messages = $('#messages-notes');
    if (messages) {
      $('#messages-notes').remove();
    }
  }, 2500);
});