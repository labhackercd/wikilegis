import $ from 'jquery';
import './content/events';


$('.js-login-button').click(function(e){
  e.preventDefault();
  var target = $(e.target);
  var popup = window.open(target.attr('href'), 'Login e-Democracia', 'height=500,width=600');

  function checkWindow() {
    if(!popup.closed) {
      setTimeout(checkWindow, 100);
      return;
    } else {
      $('.widget-loader').addClass('show');
      document.location.reload(true);
    }
  }

  checkWindow();
});
