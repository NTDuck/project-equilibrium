
$(document).ready(function() {
  // make body fade in on reload
  $("nav").fadeIn(300);
  $("main").fadeIn(300);
  $("footer").fadeIn(300);
  $("#flash-message-container").fadeIn(500);

  // make flash messages disappear when clicked
  $("button.flash-message").click(function() {
    $(this).hide();
  });
})