from __future__ import absolute_import

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlencode

from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailsnippets.views.chooser import choose
from wagtail.wagtailsnippets.views.snippets import get_content_type_from_url_params, get_snippet_type_name
from wagtail.wagtailadmin.forms import SearchForm


@permission_required('wagtailadmin.access_admin')
def wagtail_choose_snippet_by_content_type_id(request, content_type_id):
    content_type = ContentType.objects.get(id=content_type_id)
    return choose(request, content_type.app_label, content_type.model)


def get_querystring(request):
    return urlencode({
        'page_type': request.GET.get('page_type', ''),
        'allow_external_link': request.GET.get('allow_external_link', ''),
        'allow_email_link': request.GET.get('allow_email_link', ''),
        'prompt_for_link_text': request.GET.get('prompt_for_link_text', ''),
    })


@permission_required('wagtailadmin.access_admin')
def wagtail_search_snippet(request, content_type_app_name, content_type_model_name):
    content_type = get_content_type_from_url_params(content_type_app_name, content_type_model_name)
    model = content_type.model_class()
    snippet_type_name = get_snippet_type_name(content_type)[0]
    desired_class = content_type.model_class()
    is_searching = False
    items = model.objects.all()

    if 'q' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid() and search_form.cleaned_data['q']:
            items = desired_class.objects.all().filter(content__icontains=search_form.cleaned_data['q'])
            total_items = items.count()
            is_searching = True

    p = request.GET.get("p", 1)
    paginator = Paginator(items, 25)

    try:
        paginated_items = paginator.page(p)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)

    if not is_searching:
        search_form = SearchForm()

    if is_searching:
        return render(request, 'wagtail_extras/snippet_search/_search_results.html', {
            'querystring': get_querystring(request),
            'searchform': search_form,
            'snippets': paginated_items,
            'snippet_type_name': snippet_type_name,
            'snippet_type': desired_class,
            'app_name': content_type_app_name,
            'model_name': content_type_model_name,
            'total_results': total_items
        })
    return render_modal_workflow(request, 'wagtail_extras/snippet_search/browse.html', 'wagtail_extras/snippet_search/browse.js', {
        'querystring': get_querystring(request),
        'search_form': search_form,
        'snippets': paginated_items,
        'snippet_type_name': snippet_type_name,
        'snippet_type': desired_class,
        'app_name': content_type_app_name,
        'model_name': content_type_model_name
    })
