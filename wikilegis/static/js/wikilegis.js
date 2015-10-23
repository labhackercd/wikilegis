function wlDiff(a, b) {
    return JsDiff.diffWordsWithSpace(a, b);
}

function changeToMarkup(change) {
    var value = change.value;
    if (change.added) {
        value = '<span style="background-color: #d1e1ad; color: #405a04; font-weight: bold">' + value + '</span>';
    } else if (change.removed) {
        value = '<span style="background-color: #e5bdb2; color: #a82400; text-decoration: line-through; font-weight: bold">' + value + '</span>';
    }
    return value;
}

function linebreaks(text) {
    var linePattern = /(?:\r\n|\r|\n)/g;
    var paragraphPattern = /(?:\r\n|\r|\n){2}/g;
    return _.map(text.split(paragraphPattern), function(p) {
        return '<p>' + p.replace(linePattern, '<br />') + '</p>';
    }).join('\n\n');
}

function changesToMarkup(changes) {
    changes = _.map(changes, changeToMarkup);
    return linebreaks(changes.join(''));
}