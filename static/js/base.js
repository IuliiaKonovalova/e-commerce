/* jshint esversion: 8, jquery: true, scripturl: true */
$(document).ready(function () {
  $('.carousel').carousel();
  // set bootstrap carousel to stop autoplaying
  $('.carousel').carousel({

    ride: true
  });
});