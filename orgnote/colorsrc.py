from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def get_hightlight_src(code,srcname,linenos=False,stripall=True):
    try:
        lexer = get_lexer_by_name(srcname, stripall=stripall)
    except:
        return code
    
    formatter = HtmlFormatter(linenos=linenos, cssclass="source")
    result = highlight(code, lexer, formatter)
    return result

