function wlDiff(a, b) {
    return JsDiff.diffWordsWithSpace(a, b);
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
    return _.map(text.split(paragraphPattern), function(p) {
        return '<p>' + p.replace(linePattern, '<br />') + '</p>';
    }).join('\n\n');
}

function changesToMarkup(changes) {
    changes = _.map(changes, changeToMarkup);
    return linebreaks(changes.join(''));
}

jQuery(document).ready(function($) {
    // Collapsable-comments
    $('.collapsible-comments').attr('data-show', function(event, qtd_to_show){
        var comments = $(this).find('.collapsible-comments-item');

        function hideComments(commentsList, maxComments){
            for (var i = commentsList.length - 1; i >= maxComments; i--) {
                $(commentsList[i]).hide();
            }

            $(commentsList[qtd_to_show - 1]).after('<a class="show-more" href="#" title="expand to show all comments on this post" onclick>show <b>'+ String(comments.length - qtd_to_show) +'</b> more comments</a>')
        }

        function showMoreComments(commentsList){
            for(var i = 0; commentsList.length > i; i++){
                if ($(commentsList[i]).css('display') == 'none') {
                    $(commentsList[i]).show();
                }
            }
        }

        if (comments.length > qtd_to_show) {
            hideComments(comments, qtd_to_show);
        }

        $(this).find('.show-more').click(function(event) {
            $(this).hide();
            showMoreComments(comments);
        });
    });

    // language-selector
    $( ".language-selector" ).change(function() {
        $('form', this).submit();
    });
});