jQuery(document).ready(function($) {
    $('.collapsible-comments').attr('data-show', function(event, qtd_to_show){
        var comments = $('.collapsible-comments-item');

        function hideComments(commentsList, maxComments){
            for (var i = commentsList.length - 1; i >= maxComments; i--) {
                $(commentsList[i]).hide();
            };
        }

        function showMoreComments(commentsList){
            $('.show-more').hide()
            for(var i = 0; commentsList.length > i; i++){
                if ($(commentsList[i]).css('display') == 'none') {
                    $(commentsList[i]).show();
                };
            }
        }

        if (comments.length > qtd_to_show) {
            hideComments(comments, qtd_to_show);
            $(comments[qtd_to_show - 1]).after('<a class="show-more" href="#" title="expand to show all comments on this post" onclick>show <b>'+ String(comments.length - qtd_to_show) +'</b> more comments</a>')
        };
        
        $('.show-more').click(function(event) {
            showMoreComments(comments)
            $(this).hide()
        });
    })

});