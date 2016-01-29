(function($) {
    $(document).ready(function($) {
        $('div#segments-group > div > fieldset > table > tbody > tr.add-row > td')
        .html('<a id="add_segment" href="javascript:add_new_segment()">Adicionar outro(a) Segment</a>');
    });

})(django.jQuery);

function add_new_segment(){
    var form = $('#bill_form');
    form.append("<input type='hidden' name='_newsegment' value='True' />");
    form.submit();
};