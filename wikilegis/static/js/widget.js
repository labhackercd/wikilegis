<<<<<<< HEAD
var domain = 'http://wikilegis-staging.labhackercd.net/';
=======
var domain = 'http://wikilegis.labhackercd.net/';
>>>>>>> add decode string to show username
var bill_id = $('.wikilegis-widget').attr('bill-id')

function loadScript(url){    
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    head.appendChild(script);
}

loadScript(domain + 'static/js/lodash.min.js');
loadScript(domain + 'static/js/diff.min.js');
loadScript(domain + 'static/js/jquery.cookie.js');

$('head').append('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">');
$('head').append('<link rel="stylesheet" type="text/css" href="' + domain + 'static/css/widget.css">');

$(document).ready(function() {
	loadBill(bill_id);
});

$('.wikilegis-widget').wrap("<div class='wikilegis-widget-wrapper'></div>")

$('.wikilegis-widget-wrapper')
	.prepend($(document.createElement('p'))
		.addClass('widget-briefing')
		.html('Contribua diretamente no Projeto de Lei da C&acirc;mara do Deputados:')
	);
$('.widget-briefing')
	.before($(document.createElement('img'))
		.addClass('wikilegis-logo')
		.attr('src', domain + 'static/img/nav-logo.png')
);

$('.wikilegis-widget').append($(document.createElement('div')).attr('id', 'loadingDiv'));

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
}

$('.wikilegis-widget').append($(document.createElement('div'))
								.addClass('login-form')
								.attr('id', 'login-wikilegis'))

if(getCookie('wikilegis-token') == ''){
	$('#login-wikilegis').append($(document.createElement('input'))
							.attr('type', 'email')
							.attr('name','username'))
						 .append($(document.createElement('input'))
							.attr('type', 'password')
							.attr('name','password'))
						 .append($(document.createElement('button'))
							.attr('id', 'btn-login')
							.attr('onclick', 'loginWikilegis()')
							.text('Login'));
}else{
	$('#login-wikilegis').append($(document.createElement('p'))
							 	.html('Bem vindo, '+decodeURI(getCookie('wikilegis-user'))))
						.append($(document.createElement('button'))
								.attr('id', 'logout-wikilegis')
								.attr('onclick', 'logoutWikilegis()')
								.text("Sair"));
};
function createForms() {
	$.each($('.create-comment'), function(index, form) {
			var segment_id = $(form).parent().attr('segment-id')
			$(form).html('').append($(document.createElement('textarea'))
									.attr('name', 'comment')
									.attr('id', 'comment-'+segment_id)
									.attr('cols', '40')
									.attr('rows', '10'))
								.append($(document.createElement('button'))
									.attr('id', 'btn-comment')
									.text('Enviar')
									.attr('rows', '10')
									.attr('onclick', 'comment('+segment_id+')'))
		});
		$.each($('.create-proposal'), function(index, form) {
			var segment_id = $(form).parent().attr('segment-id')
			var bill_id = $(form).parent().attr('bill-id')
			$(form).html('').append($(document.createElement('textarea'))
								.attr('name', 'proposal')
								.attr('id', 'proposal-'+segment_id)
								.attr('cols', '40')
								.attr('rows', '10')
								.val($('.original.segment-'+segment_id).attr('data-raw-content')))
							.append($(document.createElement('button'))
								.attr('id', 'btn-proposal')
								.text('Enviar')
								.attr('rows', '10')
								.attr('onclick', 'proposal('+bill_id+','+segment_id+')'))
		});
};
function hideForms() {
	$.each($('.create-comment'), function(index, form) {
		$(form).html('').append($(document.createElement('p')).html('Fa&ccedil;a o login para comentar.'));
	});
	$.each($('.create-proposal'), function(index, form) {
		$(form).html('').append($(document.createElement('p')).html('Fa&ccedil;a o login para sugerir uma proposta.'));
	});
};
function logoutWikilegis() {
	$.cookie('wikilegis-token', '');
	$.cookie('wikilegis-user', '');
	$('#login-wikilegis').html('').append($(document.createElement('input'))
										.attr('type', 'email')
										.attr('name','username'))
								  .append($(document.createElement('input'))
										.attr('type', 'password')
										.attr('name','password'))
								  .append($(document.createElement('button'))
										.attr('id', 'btn-login')
										.attr('onclick', 'loginWikilegis()')
										.text('Login'));
    hideForms();
};
function loginWikilegis() {
	var username = $("#login-wikilegis input[name=username]").val();
	var password = $("#login-wikilegis input[name=password]").val();
	$.post(domain + 'accounts/api-token-auth/', {username: username, password: password}, function(data) {
		$.cookie('wikilegis-token', data['token']);
		$.cookie('wikilegis-user', data['user'].first_name+' '+data['user'].last_name);
	})
	.done(function(data) {
		$('#login-wikilegis').html('')
							 .append($(document.createElement('p'))
							 	.text('Bem vindo, '+$.cookie('wikilegis-user')))
							 .append($(document.createElement('button'))
								.attr('id', 'logout-wikilegis')
								.attr('onclick', 'logoutWikilegis()')
								.text("Sair"));
		createForms();
	})
	.error(function() {
		$('#login-wikilegis').append($(document.createElement('p')).html('Usu&aacute;rio ou senha inv&aacute;lidos!'));
	})
};

function romanize(num) {
    if (!+num)
        return false;
    var digits = String(+num).split(""),
        key = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM",
               "","X","XX","XXX","XL","L","LX","LXX","LXXX","XC",
               "","I","II","III","IV","V","VI","VII","VIII","IX"],
        roman = "",
        i = 3;
    while (i--)
        roman = (key[+digits.pop() + (i * 10)] || "") + roman;
    return Array(+digits.join("") + 1).join("M") + roman;
};
function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
};
function wlDiff(a, b) {
	return JsDiff.diffWordsWithSpace(a, b);
};
function changeToMarkup(change) {
	var value = change.value;
	if (change.added) {
		value = '<span class="added">' + value + '</span>';
	} else if (change.removed) {
		value = '<span class="removed">' + value + '</span>';
	}
	return value;
};
function linebreaks(text) {
	var linePattern = /(?:\r\n|\r|\n)/g;
	var paragraphPattern = /(?:\r\n|\r|\n){2}/g;
	return _.map(text.split(paragraphPattern), function (p) {
		return '<p>' + p.replace(linePattern, '<br />') + '</p>';
	}).join('\n\n');
};
function changesToMarkup(changes) {
	changes = _.map(changes, changeToMarkup);
	return linebreaks(changes.join(''));
};
function addDiff() {
	$('.original').each(function(){
        var div_original = this;
        var original = $(div_original).attr('data-raw-content');
        $(div_original).children('.proposals').children('.segment-proposal').children('.content').each(function(i, cur) {
            var $cur = $(cur);
            var current = $cur.attr('data-raw-content');
            $cur.find('.pp').html(changesToMarkup(wlDiff(original, current)));
        });
        $('.pp').next('p').remove();
    });
};
function get_votes(votes, segment_id){
	var up_votes = 0;
	var down_votes = 0;
	$.each(votes, function(index, vote) {
		if (vote.vote == true){
			up_votes++;		
		} else {
			down_votes++;
		};
	});
	return $(document.createElement('div'))
				.addClass('votes')
				.html('<i class="material-icons" onclick=vote("up",'+segment_id+');>thumb_up</i>' + up_votes  + 
					  ' <i class="tiny material-icons" onclick=vote("down",'+segment_id+');>thumb_down</i>' + down_votes)
}
function vote(bool, segment_id){
	if(bool=="up"){
		bool='True';
	}else if(bool="down"){
		bool='False';
	}
	$.post(domain + 'api/votes/', {vote: bool, object_id: segment_id, token: $.cookie('wikilegis-token')})
		.done(function(data){
			var up_votes = 0,
				down_votes = 0;
			$.each(data, function(index, vote) {
				if (vote.vote == true){
					up_votes++;		
				} else {
					down_votes++;
				};
			});
			$('.segment-'+segment_id)
				.children()
				.children('.actions')
				.children('.votes')
				.html('<i class="material-icons" onclick=vote("up",'+ segment_id + ');>thumb_up</i>' +
					  up_votes  + ' <i class="tiny material-icons" onclick=vote("down",'+ segment_id +
					  ');>thumb_down</i>' + down_votes)
		})
		.error(function(){
			alert('Faca o login para votar.');
		});
};
function segmentNotEditable(type, name, number, content){
	return $(document.createElement('h5'))
				.addClass('heading ' + type)
				.append(name)
				.append($(document.createElement('span'))
					.addClass('heading-number')
					.append(romanize(number)))
				.append($(document.createElement('span'))
					.addClass('heading-title')
					.append($(document.createElement('p'))
					.addClass('segment-content')
					.append(content)))
}
function segmentEditable(name, number, content, votes, bill, id){
	return $(document.createElement('div'))
            	.addClass(name)
            	.append($(document.createElement('p'))
            	.addClass('segment-content')
            	.append($(document.createElement('span'))
            		.addClass('number')
            		.html(number))
            	.append(content)
            	.append($(document.createElement('div'))
					.addClass('actions')
					.append(get_votes(votes, id))
            		.append($(document.createElement('a'))
	    				.addClass('link')
	    				.attr('href', domain + 'bill/'+ bill +'/segments/'+ id +'/')
	    				.attr('title', 'Ver no Wikilegis')
	    				.html('<i class="material-icons">call_made</i>')))
}
function numberingByType(typeDispositive, number, content, votes, bill, id, flag_paragraph){
	if (typeDispositive == 1){
		if (number <= 9){
			return segmentEditable('artigo', 'Art. ' + number + '&ordm; ', content, votes, bill, id)
		}else{
            return segmentEditable('artigo', 'Art. ' + number + ' ', content, votes, bill, id)
		}
	}else if(typeDispositive == 2){
		return segmentNotEditable('titulo', 'T&Iacute;TULO ', number, content);
	}else if(typeDispositive == 3){
		return segmentEditable('inciso', romanize(number) + ' - ', content, votes, bill, id)
	}else if(typeDispositive == 4){
		if (number <= 9){
			if(flag_paragraph){
				return segmentEditable('paragrafo', 'Par&aacute;grafo &uacute;nico. ', content, votes, bill, id)
			}else{
				return segmentEditable('paragrafo', '&#167; ' + number + '&ordm; ', content, votes, bill, id)
			}
		}else{
			return segmentEditable('paragrafo', '&#167; ' + number + ' ', content, votes, bill, id)
		}
	}else if(typeDispositive == 5){
		return segmentEditable('alinea', String.fromCharCode(96 + number) + ') ', content, votes, bill, id)
	}else if(typeDispositive == 6){
		return segmentEditable('item', number + '. ', content, votes, bill, id)
	}else if(typeDispositive == 7){
		return segmentNotEditable('capitulo', 'CAP&Iacute;TULO ', number, content);
	}else if(typeDispositive == 8){
		return segmentNotEditable('livro', 'LIVRO ', number, content);
	}else if(typeDispositive == 9){
		return segmentNotEditable('secao', 'Se&ccedil;&atilde;o ', number, content);
	}else if(typeDispositive == 10){
		return segmentNotEditable('subsecao', 'Subse&ccedil;&atilde;o ', number, content);
	}else if(typeDispositive == 11){
		return $(document.createElement('div'))
					.addClass('citacao')
					.append($(document.createElement('p'))
					.addClass('segment-content')
					.append(content)
					.append($(document.createElement('div'))
						.addClass('actions')
						.append(get_votes(votes, id))
	            		.append($(document.createElement('a'))
		    				.addClass('link')
		    				.attr('href', domain + 'bill/'+ bill +'/segments/'+ id +'/')
		    				.attr('title', 'Ver no Wikilegis')
		    				.html('<i class="material-icons">call_made</i>')))
	}
};
function comment(segment_id){
	$.post(domain + 'api/comments/', {comment: $('#comment-'+segment_id).val(), object_id: segment_id, token: $.cookie('wikilegis-token')})
		.done(function(data){
			$(document.createElement('div'))
				.addClass('comment comment-'+ data.id)
				.append($(document.createElement('span'))
					.addClass('author')
					.html(data.user.first_name + ' ' + data.user.last_name + ' - '))
				.append(data.comment)
			.insertBefore($('.comments[segment-id='+segment_id+']').children('.create-comment'));
			$('#comment-'+segment_id).val('');
			var total_comment = Number($('.segment-'+segment_id)
									.children('.commentCountWrapper')
									.children('.commentCount')
									.text().match(/\d+/)) + 1
			$('.segment-'+segment_id)
				.children('.commentCountWrapper')
				.children('.commentCount')
				.html('<i class="material-icons">forum</i> '+total_comment+' coment&aacute;rios')
		});
};
function listComments(comments, segment_id){
	var commentHtml = $(document.createElement('div')).addClass('comments').attr('segment-id', segment_id)
	$.each(comments, function(index, comment) {
		commentHtml.append($(document.createElement('div'))
							.addClass('comment comment-'+ comment.id)
							.append($(document.createElement('span'))
								.addClass('author')
								.html(comment.user.first_name + ' ' + comment.user.last_name + ' - '))
							.append(comment.comment))
	});	
	commentHtml.append($(document.createElement('div')).addClass('create-comment'));
	return commentHtml
};
function proposal(bill_id, segment_id){
	$.post(domain + 'api/segments/', {content: $('#proposal-'+segment_id).val(), replaced: segment_id, bill: bill_id, token: $.cookie('wikilegis-token')})
		.done(function(data){
			$(document.createElement('div'))
				.addClass('segment-proposal segment-' + data.id)
				.append($(document.createElement('span'))
					.addClass('author')
					.html(data.author.first_name + ' ' + data.author.last_name + ' - '))
				.append($(document.createElement('div'))
					.addClass('content')
					.attr('data-raw-content', data.content)
					.append($(document.createElement('p'))
						.addClass('pp')
						.html(data.content))
					.append($(document.createElement('div'))
						.addClass('actions')
						.append(get_votes(data.votes, data.id))
						.append($(document.createElement('a'))
							.addClass('link')
							.attr('href', domain + 'bill/'+ data.bill +'/segments/'+ data.replaced +'/#amendment-'+ data.id)
							.attr('title', 'Ver no Wikilegis')
							.html('<i class="material-icons">call_made</i>'))))
    			.append($(document.createElement('div'))
							.addClass('commentCountWrapper')
							.append($(document.createElement('div'))
								.addClass('commentCount')
								.append('<i class="material-icons">forum</i> '+ data.comments.length +' coment&aacute;rios ')))
				.append(listComments(data.comments, data.id))
			.insertBefore($('.proposals[segment-id='+segment_id+']').children('.create-proposal'));
			$('#proposal-'+segment_id).val($('.original.segment-'+segment_id).attr('data-raw-content'));
			var total_comment = Number($('.original.segment-'+segment_id)
									.children('.propCount')
									.text().match(/\d+/)) + 1
			$('.original.segment-'+segment_id)
				.children('.propCount')
				.html('<i class="material-icons">note_add</i> '+total_comment+' propostas');
			addDiff();
			createForms();
			$('.comments[segment-id='+data.id+']').hide();
			$('.segment-proposal.segment-'+data.id).children(".commentCountWrapper").children(".commentCount").on('click', function() {
			    $(this).parent().next(".comments").toggle();
			});
		});
};
function listProposals(proposals, bill_id, segment_id){
	var propHtml = $(document.createElement('div')).addClass('proposals').attr('segment-id', segment_id).attr('bill-id', bill_id)
	$.each(proposals, function(index, proposal) {
		propHtml.append($(document.createElement('div'))
							.addClass('segment-proposal segment-' + proposal.id)
							.append($(document.createElement('span'))
								.addClass('author')
								.html(proposal.author.first_name + ' ' + proposal.author.last_name + ' - '))
							//Placeholder code (swapped div for link and added attr) for alpha widget release! XXX
							.append($(document.createElement('a'))
								.addClass('content')
								.attr('data-raw-content', proposal.content)
								.attr('href', domain + 'bill/'+ proposal.bill +'/segments/'+ proposal.replaced +'/#amendment-'+ proposal.id)
								.attr('title', 'Ver no Wikilegis')
								.append($(document.createElement('p'))
									.addClass('pp')
									.html(proposal.content))
								.append($(document.createElement('div'))
									.addClass('actions')
									.append(get_votes(proposal.votes, proposal.id))
									.append($(document.createElement('a'))
										.addClass('link')
										.attr('href', domain + 'bill/'+ proposal.bill +'/segments/'+ proposal.replaced +'/#amendment-'+ proposal.id)
										.attr('title', 'Ver no Wikilegis')
										.html('<i class="material-icons">call_made</i>'))))
			    			.append($(document.createElement('div'))
										.addClass('commentCountWrapper')
										.append($(document.createElement('div'))
											.addClass('commentCount')
											.append('<i class="material-icons">forum</i> '+ proposal.comments.length +' coment&aacute;rios ')))
							.append(listComments(proposal.comments, proposal.id)))
	});	
	propHtml.append($(document.createElement('div')).addClass('create-proposal'));
	return propHtml
};
function loadBill(bill_id){
	$.getJSON(domain + 'api/bills/'+ bill_id +'?format=json', function(data) {
		$('.wikilegis-widget')
					.append($(document.createElement('div'))
								.addClass('widget-header')
								.append($(document.createElement('h1'))
											.addClass('title')
											.append(data.title)
											.append($(document.createElement('a'))
						    				.addClass('link')
						    				.attr('href', domain + 'bill/'+ data.id)
						    				.attr('title', 'Ver no Wikilegis')
											.html('<i class="material-icons">call_made</i>')))
								.append($(document.createElement('h4')).addClass('epigraph').html(data.epigraph))
								.append($(document.createElement('div')).addClass('description').append($(document.createElement('p')).html(data.description))))
		var segments = sortByKey(data.segments, 'order')
		$.each(segments, function(index, obj) {
		    if(obj.original == true){
	    		var flag_paragraph = false
		    	if(obj.type == 4 && obj.number == 1){
		    		var i = j = index;
		    		var count_paragraph = 0;
	    			while(segments[i].type != 1){
	    				if(segments[i].type == 4 && segments[i].original == true){
				    		++count_paragraph;
					    };
	    				++i;
	    			};
	    			while(segments[j].type != 1){
	    				--j;
	    				if(segments[j].type == 4 && segments[j].original == true){
				    		++count_paragraph;
					    };
	    			};
					if(count_paragraph == 1){
						flag_paragraph = true;
					};
		    	}
		    	$('.wikilegis-widget').append(
		    		$(document.createElement('div'))
		    			.addClass('segment original segment-' + obj.id)
		    			.attr('segment-id', obj.id)
		    			.attr('data-raw-content', obj.content)
		    			.append(numberingByType(obj.type, obj.number, obj.content, obj.votes, obj.bill, obj.id, flag_paragraph))
	    		);
		    	var comments = sortByKey(obj.comments, 'id');
		  
				$('.segment-'+ obj.id).append($(document.createElement('div'))
												.addClass('commentCountWrapper')
												.append($(document.createElement('div'))
													.addClass('commentCount')
													.append('<i class="material-icons">forum</i> '+ comments.length +' coment&aacute;rios ')))
									  .append(listComments(comments, obj.id));
				
		    	var proposals = [];
		    	for (var i = 0; i < segments.length; ++i) {
					var segment = segments[i];
					if(segment.type == obj.type && segment.number == obj.number && segment.original == false){
						proposals.push(segment);
					};
				};
				proposals = sortByKey(proposals, 'id')
				
				$('.segment-'+ obj.id)
					.append($(document.createElement('div'))
						.addClass('propCount')
						.append('<i class="material-icons">note_add</i> '+ proposals.length +' propostas '))
				  	.append(listProposals(proposals, obj.bill, obj.id));
				
		    };
	    });
		//Placeholder code for alpha widget release! XXX
		$('.wikilegis-widget .segment-content').wrap( "<a href='" + domain + "bill/" + data.id + "' class='placeholder-link' title='Ver no Wikilegis'></a>" );
		$('.wikilegis-widget .title').wrap( "<a href='" + domain + "bill/" + data.id + "' class='placeholder-link' title='Ver no Wikilegis'></a>" );
		$('.wikilegis-widget .link').remove();
	})
	.done(function() {
		if(getCookie('wikilegis-token') == ''){
			hideForms();
		}else{
			createForms();
		};
		$(".comments").hide();
		$(".proposals").hide();	
		$(".commentCount").on('click', function() {
		    $(this).parent().next(".comments").toggle();
		});
		$(".propCount").on('click', function() {
		    $(this).next(".proposals").toggle();
		});

    $('.original').each(function(){
        var div_original = this;
        var original = $(div_original).attr('data-raw-content');
        $(div_original).children('.proposals').children('.segment-proposal').children('.content').each(function(i, cur) {
            var $cur = $(cur);
            var current = $cur.attr('data-raw-content');
            $cur.find('.pp').html(changesToMarkup(wlDiff(original, current)));
        });
        $('.pp').next('p').remove();
    });

    // 20 or more segments, add "read more" button
    if ($('.wikilegis-widget .segment').length > 19) {

    	var firstSegmentsHeight = 0;

    	$('.segment.original:lt(21)').each(function() {
    	   firstSegmentsHeight += $(this).outerHeight(true);
    	});

    	$('.wikilegis-widget')
    		.css('height', firstSegmentsHeight + 'px')
    		.css('overflow', 'hidden')

    	$('.wikilegis-widget')
    		.append($(document.createElement('a'))
    		.addClass('read-more')
    		.attr('href', domain + 'bill/'+ bill_id)
    		.html('Ver todo o projeto no Wikilegis')
    	);
    } else {
    	$('.wikilegis-widget')
    		.css('height', 'auto')
    		.css('overflow', 'visible');
    }

    /*
    $('.wikilegis-widget .read-more').click(function() {
    	$('.wikilegis-widget')
    		.css('height', 'auto')
    		.css('overflow', 'visible');

    	$('.wikilegis-widget .read-more')
    		.css('display', 'none');				
    })
    */

    $('#loadingDiv').hide();
	});
};

