function(modal) {

    var searchUrl = $('form.search-form', modal.body).attr('action');
    var listingUrl = $('#snippet-chooser-list', modal.body).data('url');

    function search() {
        $.ajax({
            url: searchUrl,
            data: {
                q: $('#id_q', modal.body).val(),
                results_only: true
            },
            success: function(data, status) {
                $('.page-results', modal.body).html(data);
                ajaxifyLinks();
            }
        });
        return false;
    }

    function ajaxifyLinks(context) {
        $('a.snippet-choice', context).click(function() {
            var pageData = $(this).data();
            modal.respond('snippetChosen', $(this).data());
            modal.close();
            return false;
        });

        $('.pagination a', context).click(function() {
            var page = this.getAttribute('data-page');
            setPage(page);
            return false;
        });
    }

    function setPage(page) {
        $.ajax({
            url: listingUrl,
            data: {
                p: page
            },
            dataType: 'html',
            success: function(data, status, xhr) {
                var response = eval('(' + data + ')');
                $(modal.body).html(response.html);
                if (response.onload) {
                    response.onload(self);
                }
                ajaxifyLinks($('#snippet-chooser-list'));
            }
        });

        return false;
    }

    $('#id_q', modal.body).on('input', function() {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 200);
        $(this).data('timer', wait);
    });

    modal.ajaxifyForm($('form.search-form', modal.body));

    ajaxifyLinks(modal.body);

    $('#id_q', modal.body).focus();
}