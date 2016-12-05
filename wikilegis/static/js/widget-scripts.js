function wlDiff(a, b) {
    return JsDiff.diffWords(a, b);
}

function changeToMarkup(change) {
    var value = change.value;
    if (change.added) {
        value = '<span class="added">' + value + '</span>';
    } else if (change.removed) {
        value = '<span class="removed">' + value + '</span>';
    }
    return value;
}

function linebreaks(text) {
    var linePattern = /(?:\r\n|\r|\n)/g;
    var paragraphPattern = /(?:\r\n|\r|\n){2}/g;
    return _.map(text.split(paragraphPattern), function (p) {
        return p.replace(linePattern, '<br />');
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