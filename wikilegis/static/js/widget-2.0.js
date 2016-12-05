function auto_grow(element) {
    element.style.height = "1px";
    element.style.height = (element.scrollHeight)+"px";
}

$(document).ready(function(){
  /* Login & Signup Toggle */

  $('.wikilegis-widget__link--access-toggle').on('click', function(event){
     event.preventDefault();
    $('.wikilegis-widget__access-box').toggleClass('translatex--left');
  })
})