from __future__ import absolute_import, unicode_literals

import json

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel
from wagtail.wagtailsnippets.widgets import AdminSnippetChooser


class BaseSnippetSearchPanel(BaseChooserPanel):
    object_type_name = 'item'

    _content_type = None

    @classmethod
    def widget_overrides(cls):
        return {cls.field_name: CustomAdminSnippetChooser(
            content_type=cls.content_type(), snippet_type_name=cls.snippet_type_name)}

    @classmethod
    def content_type(cls):
        if cls._content_type is None:
            cls._content_type = ContentType.objects.get_for_model(cls.snippet_type)

        return cls._content_type

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(render_to_string(self.field_template, {
            'field': self.bound_field,
            self.object_type_name: instance_obj,
            'snippet_type_name': self.snippet_type_name,
        }))


class SnippetSearchPanel(object):
    def __init__(self, field_name, snippet_type):
        self.field_name = field_name
        self.snippet_type = snippet_type

    def bind_to_model(self, model):
        return type(str('_SnippetSearchPanel'), (BaseSnippetSearchPanel,), {
            'model': model,
            'field_name': self.field_name,
            'snippet_type_name': force_text(self.snippet_type._meta.verbose_name),
            'snippet_type': self.snippet_type,
        })


class CustomAdminSnippetChooser(AdminSnippetChooser):

    def render_js_init(self, id_, name, value):
        content_type = self.target_content_type

        return "createSnippetSearchChooser({id}, {content_type});".format(
            id=json.dumps(id_),
            content_type=json.dumps('{app}/{model}'.format(
                app=content_type.app_label,
                model=content_type.model)))
