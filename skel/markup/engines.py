from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str, force_unicode
from django.utils.html import escape, urlize


# Global engine registry. Used to look up engines by name.
registered_engines = {}

    
class EngineBase(type):
    """Creates and registers an ``Engine`` class."""
    def __new__(cls, name, bases, attrs):
        global registered_engines
        engine = super(EngineBase, cls).__new__(cls, name, bases, attrs)
        if name == 'Engine':
            return engine
        engine_name = getattr(engine, 'name')
        registered_engines[engine_name] = engine
        return engine


class Engine(object):
    __metaclass__ = EngineBase
    name = 'engine_name'
    label = 'Engine Label'
    default_options = {}
    
    def _finalize_options(self, options):
        if options is None:
            return self.default_options
        final_options = self.default_options
        final_options.update(options)
        return final_options

    def render(self, source, options=None):
        options = self._finalize_options(options)
        markup = self._render(smart_str(source), options)
        return mark_safe(force_unicode(markup))
        
    def _render(self, source, options=None):
        raise NotImplementedError('MarkUps must provide a "_render" method.')


class PlainText(Engine):
    name = 'text'
    label = 'Plain Text'
    
    def _render(self, source, options=None):
        return urlize(escape(source))


class Markdown(Engine):
    name = 'markdown'
    label = 'Markdown'
    default_options = {
        'safe_mode': False,
    }
    
    def _render(self, source, options=None):
        import markdown
        extensions = options.get('extensions', [])
        return markdown.markdown(source, extensions, safe_mode=options['safe_mode'])

        
class RestructuredText(Engine):
    name = 'rest'
    label = 'reStructuredText'
    default_options = {
        'writer_name': 'html4css1',
        'doctitle_xform': False,
        'cloak_email_addresses': True,
    }

    def _render(self, source, options=None):
        from docutils.core import publish_parts
        writer_name = options.pop('writer_name')
        parts = publish_parts(source=source, 
                              writer_name=writer_name,
                              settings_overrides=options)
        return parts['fragment']


class XHTML(Engine):
    name = 'xhtml'
    label = 'XHTML'
    
    def _render(self, source, options=None):
        return source