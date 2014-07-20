"""code renderer module."""

import pygments
import pygments.lexers
import pygments.formatters

from mfr import config as core_config, RenderResult

from mfr_code_pygments.configuration import config as module_config


def render_to_html(fp, *args, **kwargs):
    """Generate an html representation of the file

    :param fp: filepointer
    :return: RenderResult object containing the content html and its assets
    """
    formatter = pygments.formatters.HtmlFormatter(cssclass=module_config['CSS_CLASS'])
    content = fp.read()
    lexer = pygments.lexers.guess_lexer_for_filename(fp.name, content)
    content = pygments.highlight(content, lexer, formatter)
    if core_config['INCLUDE_STATIC']:
        link = get_stylesheet()
        # return '\n'.join([link, content])
        assets = {"css": link}
        return RenderResult(content=content, assets=assets)
    else:
        return content


def get_stylesheet():
    """Generate an html link to a stylesheet"""
    
    return '<link rel="stylesheet" href="{static_url}/mfr_code_pygments/css/{theme}.css" />'\
        .format(static_url=core_config['STATIC_URL'], theme=module_config['PYGMENTS_THEME'])
