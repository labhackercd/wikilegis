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

function linebreaks(text) {
    var linePattern = /(?:\r\n|\r|\n)/g;
    var paragraphPattern = /(?:\r\n|\r|\n){2}/g;
    return _.map(text.split(paragraphPattern), function (p) {
        return p.replace(linePattern);
    }).join('\n\n');
}

function changesToMarkup(changes) {
    changes = _.map(changes, changeToMarkup);
    return linebreaks(changes.join(''));
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


/// Toggle action boxes

/**  If clicked on an action that is not a vote or already a toggled box,
  *  untoggle itself and all others.
  */
$('.wikilegis-widget__action').click(function(){
    if (!$(this).is('.wikilegis-widget__action--vote, .wikilegis-widget__action--amendment, .active')) {
        $('.wikilegis-widget__action').removeClass('active');
        $('.wikilegis-widget__action-box').removeClass('active');
    }
});

/** Toggle unique comment box
  */
$('.wikilegis-widget__action--comments').click(function(){
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
$('.wikilegis-widget__action--amendments').click(function(){
    var segmentId = $(this).data('segment-id');
    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $(`.wikilegis-widget__action-box--amendments[data-segment-id='${segmentId}'`).removeClass('active');
    } else {
        $(this).addClass('active');
        $(`.wikilegis-widget__action-box--amendments[data-segment-id='${segmentId}'`).addClass('active');

        $('html, body').animate({
            scrollTop: ($(`.wikilegis-widget__action-box--amendments[data-segment-id='${segmentId}'`).parent().offset().top - 16)
        }, 300);
    }
});