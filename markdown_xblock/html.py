"""This XBlock help creating a secure and easy-to-use HTML blocks in edx-platform."""

import logging
import os
from pathlib import Path

import markdown2
from django.conf import settings as django_settings
from xblock.core import XBlock
from xblock.fields import List, Scope, String
from web_fragments.fragment import Fragment
from xblock.utils.resources import ResourceLoader
from xblock.utils.settings import XBlockWithSettingsMixin
from xblock.utils.studio_editable import StudioEditableXBlockMixin, loader

from .utils import _

log = logging.getLogger(__name__)  # pylint: disable=invalid-name
xblock_loader = ResourceLoader(__name__)  # pylint: disable=invalid-name

SETTINGS_KEY = 'markdown'
DEFAULT_EXTRAS = [
    "code-friendly",
    "fenced-code-blocks",
    "footnotes",
    "tables",
    "use-file-vars"
]
DEFAULT_SETTINGS = {
    "extras": DEFAULT_EXTRAS,
    "safe_mode": 'replace'
}


def get_xblock_settings():
    """Extract xblock settings."""
    try:
        xblock_settings = django_settings.XBLOCK_SETTINGS
        settings = xblock_settings.get(
            SETTINGS_KEY, DEFAULT_SETTINGS)
    except AttributeError:
        settings = DEFAULT_SETTINGS

    return settings


@XBlock.wants('settings')
class MarkdownXBlock(StudioEditableXBlockMixin, XBlockWithSettingsMixin, XBlock):
    """
    This XBlock provides content editing in Markdown and displays it in HTML.
    """

    display_name = String(
        display_name=_('Display Name'),
        help=_('The display name for this component.'),
        scope=Scope.settings,
        default=_('Markdown')
    )
    classes = List(
        display_name=_('Classes'),
        help=_('JSON list of strings representing custom CSS classes to add to this component'),
        scope=Scope.settings,
        default=[]
    )
    data = String(
        help=_('The Markdown content for this module'),
        default=u'',
        scope=Scope.content
    )
    editor = 'markdown'
    editable_fields = ('display_name', 'classes')
    show_in_read_only_mode = True

    @XBlock.supports('multi_device')
    def student_view(self, context=None):  # pylint: disable=unused-argument
        """
        Return a fragment that contains the html for the student view.
        """
        frag = Fragment()
        frag.content = xblock_loader.render_django_template('static/html/lms.html', {'self': self})

        frag.add_css_url(self.runtime.local_resource_url(self, 'public/plugins/codesample/css/prism.css'))
        frag.add_javascript_url(self.runtime.local_resource_url(self, 'public/plugins/codesample/js/prism.js'))

        frag.add_css_url(self.runtime.local_resource_url(self, 'static/css/pygments.css'))
        frag.add_css_url(self.runtime.local_resource_url(self, 'static/css/html.css'))

        return frag

    def studio_view(self, context=None):  # pylint: disable=unused-argument
        """
        Return a fragment that contains the html for the Studio view.
        """
        frag = Fragment()
        settings_fields = self.get_editable_fields()
        settings_page = loader.render_django_template('templates/studio_edit.html', {'fields': settings_fields})
        context = {
            'self': self,
            'settings_page': settings_page,
        }

        frag.content = xblock_loader.render_django_template('static/html/studio.html', context)

        self.add_stylesheets(frag)
        self.add_scripts(frag)

        js_data = {
            'editor': self.editor,
            'skin_url': self.runtime.local_resource_url(self, 'public/skin'),
            'external_plugins': self.get_editor_plugins()
        }
        frag.initialize_js('MarkdownXBlock', js_data)

        return frag

    @XBlock.supports("multi_device")
    def public_view(self, context=None):
        """
        Return the student_view when course is set to be public.
        """
        return self.student_view(context)

    @XBlock.json_handler
    def update_content(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Update the saved HTML data with the new HTML passed in the JSON 'content' field.
        """
        self.data = data['content']

        return {'content': self.data}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ('MarkdownXBlock',
             """<vertical_demo>
                    <markdown>
                        # This is h1
                        ## This is h2
                        ```
                        This is a code block
                        ```
                        * This is
                        * an unordered
                        * list
                        This is a regular paragraph
                        1. This is
                        1. an ordered
                        1. list
                        *This is italic*
                        **This is bold**
                    </markdown>
                </vertical_demo>
             """),
        ]

    def add_stylesheets(self, frag):
        """
        A helper method to add all necessary styles to the fragment.
        :param frag: The fragment that will hold the scripts.
        """
        frag.add_css_url(self.runtime.local_resource_url(self, 'static/css/html.css'))

        frag.add_css_url(self.runtime.local_resource_url(
            self, 'public/plugins/codemirror/codemirror-4.8/lib/codemirror.css'))

    def add_scripts(self, frag):
        """
        A helper method to add all necessary scripts to the fragment.
        :param frag: The fragment that will hold the scripts.
        """
        frag.add_javascript_url(self.runtime.local_resource_url(self, 'static/js/tinymce/tinymce.min.js'))
        frag.add_javascript_url(self.runtime.local_resource_url(self, 'static/js/tinymce/themes/modern/theme.min.js'))
        frag.add_javascript_url(self.runtime.local_resource_url(self, 'static/js/html.js'))
        frag.add_javascript(loader.load_unicode('public/studio_edit.js'))

        code_mirror_dir = 'public/plugins/codemirror/codemirror-4.8/'

        frag.add_javascript_url(self.runtime.local_resource_url(self, code_mirror_dir + 'lib/codemirror.js'))
        frag.add_javascript_url(self.runtime.local_resource_url(self, code_mirror_dir + 'mode/markdown/markdown.js'))

    def get_editor_plugins(self):
        """
        This method will generate a list of external plugins urls to be used in TinyMCE editor.
        These plugins should live in `public` directory for us to generate URLs for.

        const PLUGINS_DIR = "/resource/html5/public/plugins/";
        const EXTERNAL_PLUGINS = PLUGINS.map(function(p) { return PLUGINS_DIR + p + "/plugin.min.js" });

        :return: A list of URLs
        """
        plugin_path = 'public/plugins/{plugin}/plugin.min.js'
        plugins = ['codesample', 'image', 'link', 'lists', 'textcolor', 'codemirror']

        return {
            plugin: self.runtime.local_resource_url(self, plugin_path.format(plugin=plugin)) for plugin in plugins
        }

    def substitute_keywords(self, html):
        """
        Replaces all %%-encoded words using KEYWORD_FUNCTION_MAP mapping functions.

        Iterates through all keywords that must be substituted and replaces them by calling the corresponding functions
        stored in `keywords`. If the function throws a specified exception, the substitution is not performed.

        Functions stored in `keywords` must either:
            - return a replacement string
            - throw `KeyError` or `AttributeError`, `TypeError`.
        """
        data = html
        system = getattr(self, 'system', None)
        if not system:  # This shouldn't happen, but if `system` is missing, then skip substituting keywords.
            return data

        keywords = {
            '%%USER_ID%%': lambda: getattr(system, 'anonymous_student_id'),
            '%%COURSE_ID%%': lambda: getattr(system, 'course_id').html_id(),
        }

        for key, substitutor in keywords.items():
            if key in data:
                try:
                    data = data.replace(key, substitutor())
                except (KeyError, AttributeError, TypeError):
                    # Do not replace the keyword when substitutor is not present.
                    pass

        return data

    @property
    def html(self):
        """
        A property that returns the markdown content data as html.
        """
        settings = get_xblock_settings()
        extras = settings.get("extras",
                              DEFAULT_SETTINGS['extras'])
        safe_mode = settings.get("safe_mode",
                                 DEFAULT_SETTINGS['safe_mode'])

        html = markdown2.markdown(
            self.data,
            extras=extras,
            safe_mode=safe_mode
        )

        html = self.substitute_keywords(html)

        return html

    def get_editable_fields(self):
        """
        This method extracts the editable fields from this XBlock and returns them after validating them.

        Part of this method's copied from StudioEditableXBlockMixin#submit_studio_edits
        with some modifications..
        :return: A list of the editable fields with the information that
                the template needs to render a form field for them.

        """
        fields = []

        # Build a list of all the fields that can be edited:
        for field_name in self.editable_fields:
            field = self.fields[field_name]  # pylint: disable=unsubscriptable-object
            assert field.scope in (Scope.content, Scope.settings), (
                'Only Scope.content or Scope.settings fields can be used with '
                'StudioEditableXBlockMixin. Other scopes are for user-specific data and are '
                'not generally created/configured by content authors in Studio.'
            )
            field_info = self._make_field_info(field_name, field)
            if field_info is not None:
                fields.append(field_info)

        return fields

    @classmethod
    def parse_xml(cls, node, runtime, keys):
        """
        Use `node` to construct a new block.
        """
        block = runtime.construct_xblock_from_class(cls, keys)
        id_generator = runtime.id_generator

        # Read markdown content from file and add to editor.
        url_name = node.get('url_name', node.get('slug'))
        location = id_generator.create_definition(node.tag, url_name)

        filename = node.get('filename')
        pointer_path = "{category}/{url_path}".format(
            category='markdown',
            url_path=location.block_id.replace(':', '/')
        )
        base = str(Path(pointer_path).parent)
        filepath = u"{base}/{name}.md".format(base=base, name=filename)

        with runtime.resources_fs.open(filepath, encoding='utf-8') as infile:
            markdown = infile.read()
            block.data = markdown

        # Attributes become fields.
        for name, value in list(node.items()):  # lxml has no iteritems
            cls._set_field_if_present(block, name, value, {})

        return block

    def add_xml_to_node(self, node):
        """
        For exporting, set data on etree.Element `node`.
        """

        # Write markdown data to file
        pathname = self.url_name.replace(':', '/')
        filepath = u'{category}/{pathname}.md'.format(
            category=self.category,
            pathname=pathname
        )

        self.runtime.export_fs.makedirs(
            os.path.dirname(filepath),
            recreate=True)

        with self.runtime.export_fs.open(filepath, 'wb') as filestream:
            markdown_data = self.data.encode('utf-8')
            filestream.write(markdown_data)

        # Write out the markdown file name
        filename = Path(pathname).name

        node.tag = self.category
        node.set("filename", filename)
        node.set('xblock-family', self.entry_point)
        node.set('display_name', self.display_name)
        node.set('classes', str(self.classes))
