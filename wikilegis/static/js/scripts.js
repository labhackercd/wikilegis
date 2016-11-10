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
    return _.map(text.split(paragraphPattern), function (p) {
        return p.replace(linePattern, '<br />');
    }).join('\n\n');
}

function changesToMarkup(changes) {
    changes = _.map(changes, changeToMarkup);
    return linebreaks(changes.join(''));
}

jQuery(document).ready(function ($) {

    //navbar

    var is_root = location.pathname == "/";

    if (is_root) {

        if ($(window).scrollTop() >= ($(window).height() - $('.wiki-navbar').height()))
            $('.wiki-navbar').addClass('fixed-top');

        $(window).scroll(function () {
            if ($(this).scrollTop() >= ($(window).height() - $('.wiki-navbar').height())) {
                if (!$('.wiki-navbar').hasClass('fixed-top'))
                    $('.wiki-navbar').hide().addClass('fixed-top').fadeIn(200);
            } else {
                if ($('.wiki-navbar').hasClass('fixed-top'))
                    $('.wiki-navbar').removeClass('fixed-top');
            }
        });

    } else {
        $('.wiki-navbar').addClass('fixed-top')
    }

    //mob-nav

    $('#open-menu').click(function (e) {
        e.preventDefault();
        var is_opened = $('.wiki-navbar').hasClass('opened');

        if (!is_opened) {
            open();
        } else {
            close();
        }

        $('#overlay').click(function() {
            close();
        });

    });

    function open() {
        $(document.body).append('<div id="overlay"></div>');
        $('.wiki-navbar').addClass('opened');
        $('.wiki-navbar').css('background-color', '#324545');
        $('.wiki-navbar').css('box-shadow', '0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12)');
        $('#menu-button').html('close');
        $('.wiki-navbar').css('height', 'auto');
        $('.opened-menu').removeClass('hide');
    }

    function close() {
        $('#overlay').remove();
        $('.wiki-navbar').removeClass('opened');
        $('.wiki-navbar').css('box-shadow','');
        $('.wiki-navbar').css('background-color', '');
        $('#menu-button').html('menu');
        $('.wiki-navbar').css('height', '');
        $('.opened-menu').addClass('hide');
    }



    //See projects

    $(".see-projects").click(function () {
        $('html, body').animate({
            scrollTop: $("#projects").offset().top
        }, 1000, 'easeOutCirc');
    });


    //Show more segments

    $('.show-more-segments').click(function() {
        $(this).parent().find('.bill-link').nextAll('.bill-link').show();
        $(this).remove();
    });


    //Add segment item

    $('.asi-link').click(function() {
        $(this).hide();
        $('.add-segment-form').removeClass('hide');
        $('.segment-content').focus();
    });

    var cancel = $('.add-segment-form').find('.cancel');

    cancel.click(function() {
        $('.add-segment-form').addClass('hide');
        $('.asi-link').show();
    });

    //View comments

    $('.view-comments').click(function(e) {
        e.preventDefault();
        //$(this).hide();
        console.log($(this).closest('.main').find('.holder').removeClass('hide'));
        /*$('.segment-content').focus();*/
    });


    // Collapsable-comments
    $('.collapsible-comments').attr('data-show', function (event, qtd_to_show) {
        var comments = $(this).find('.collapsible-comments-item');

        function hideComments(commentsList, maxComments) {
            for (var i = commentsList.length - 1; i >= maxComments; i--) {
                $(commentsList[i]).hide();
            }

            $(commentsList[qtd_to_show - 1]).after('<a class="show-more" href="#" title="expand to show all comments on this post" onclick>show <b>' + String(comments.length - qtd_to_show) + '</b> more comments</a>')
        }

        function showMoreComments(commentsList) {
            for (var i = 0; commentsList.length > i; i++) {
                if ($(commentsList[i]).css('display') == 'none') {
                    $(commentsList[i]).show();
                }
            }
        }

        if (comments.length > qtd_to_show) {
            hideComments(comments, qtd_to_show);
        }

        $(this).find('.show-more').click(function (event) {
            $(this).hide();
            showMoreComments(comments);
        });
    });

    // language-selector
    $(".language-selector").change(function () {
        $('form', this).submit();
    });

    // Dropdown Orderer\
    $(".dropdown-button").dropdown();

});

