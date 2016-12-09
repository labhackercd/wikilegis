function auto_grow(element) {
    element.style.height = "1px";
    element.style.height = (element.scrollHeight)+"px";
}

function wlDiff(a, b) {
    return JsDiff.diffWords(a, b);
}

function changeToMarkup(change) {
    var value = change.value;
    if (change.added) {
        value = '<span class="wikilegis-widget__diff--added">' + value + '</span>';
    } else if (change.removed) {
        value = '<span class="wikilegis-widget__diff--removed">' + value + '</span>';
    }
    return value;
}

function changesToMarkup(changes) {
    changes = _.map(changes, changeToMarkup);
    return changes.join('');
}

$('.wikilegis-widget__segment-text--amendment').each(function() {
  var originalText = $(this).closest('.wikilegis-widget__segment--original').find('.wikilegis-widget__segment-text--original').text();
  $(this).html(changesToMarkup(wlDiff(originalText, $(this).text())));
});

// Login & Signup Toggle
$('.wikilegis-widget__link--access-toggle').on('click', function(event){
   event.preventDefault();
  $('.wikilegis-widget__access-box').toggleClass('translatex--left');
});


$(document).ready(function() {
    /// Toggle action boxes

    /**  If clicked on an action that is not a vote or already a toggled box,
      *  untoggle itself and all others.
      */
    $('body').on('click', '.wikilegis-widget__action', function() {
        if (!$(this).is('.wikilegis-widget__action--vote, .wikilegis-widget__action--amendment, .active')) {
            $('.wikilegis-widget__action').removeClass('active');
            $('.wikilegis-widget__action-box').removeClass('active');
            $('.wikilegis-widget__segment').removeClass('active');
        }
    });

    /** Toggle unique comment box
      */
    $('body').on('click', '.wikilegis-widget__action--comments', function() {
        var segmentId = $(this).data('segment-id');
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).closest('.wikilegis-widget__segment').removeClass('active');
            $(`.wikilegis-widget__action-box--comments[data-segment-id='${segmentId}'`).removeClass('active');
        } else {
            $(this).addClass('active');
            $(`.wikilegis-widget__action-box--comments[data-segment-id='${segmentId}'`).addClass('active');
            $(this).closest('.wikilegis-widget__segment').addClass('active');

            $('html, body').animate({
                scrollTop: ($(`.wikilegis-widget__action-box--comments[data-segment-id='${segmentId}'`).parent().offset().top - 16)
            }, 300);
        }
    });

    /** Toggle unique amendment box
     */
    $('body').on('click', '.wikilegis-widget__action--amendments', function() {
        var segmentId = $(this).data('segment-id');
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).closest('.wikilegis-widget__segment').removeClass('active');
            $(`.wikilegis-widget__action-box--amendments[data-segment-id='${segmentId}'`).removeClass('active');
        } else {
            $(this).addClass('active');
            $(`.wikilegis-widget__action-box--amendments[data-segment-id='${segmentId}'`).addClass('active');
            $(this).closest('.wikilegis-widget__segment').addClass('active');

            $('html, body').animate({
                scrollTop: ($(`.wikilegis-widget__action-box--amendments[data-segment-id='${segmentId}'`).parent().offset().top - 16)
            }, 300);
        }
    })
})

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});