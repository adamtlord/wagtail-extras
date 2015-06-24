from django.conf.urls import url

from wagtail.wagtailcore import hooks
from wagtail_extras.views import wagtail_search_snippet


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^snippets/search/(\w+)/(\w+)/$',
            wagtail_search_snippet,
            name='wagtail_search_snippet'),
    ]


@hooks.register('insert_editor_js')
def snippet_search_chooser_panel_js():
    return """
            <script>
                function createSnippetSearchChooser(id, contentType) {
                    var chooserElement = $('#' + id + '-chooser');
                    var docTitle = chooserElement.find('.title');
                    var input = $('#' + id);
                    var editLink = chooserElement.find('.edit-link');

                    $('.action-choose', chooserElement).click(function() {
                        ModalWorkflow({
                            url: '/admin/snippets/search/' + contentType + '/',
                            responses: {
                                snippetChosen: function(snippetData) {
                                    input.val(snippetData.id);
                                    docTitle.text(snippetData.title);
                                    chooserElement.removeClass('blank');
                                    editLink.attr('href', snippetData.editUrl);
                                }
                            }
                        });
                    });

                    $('.action-clear', chooserElement).click(function() {
                        input.val('');
                        chooserElement.addClass('blank');
                    });
                }
            </script>
    """
