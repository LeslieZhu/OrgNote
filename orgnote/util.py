#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import
from bs4 import BeautifulSoup

import mistune
import re
from mistune.plugins import plugin_table,plugin_task_lists,plugin_url,plugin_strikethrough,plugin_footnotes,plugin_abbr
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html as py_html
 
 
class HighlightRenderer(mistune.HTMLRenderer):

    def __init__(self):
        super().__init__()
        self.toc = []
        self.anchor_count = {}
        self.level_counts = [0] * 10  # 假设最多支持 10 级标题
        self.last_level = 1

    def heading(self, text, level):
        # self.toc.append((level, text))
        # return super().heading(text, level)

        # 生成锚点 ID
        anchor_text = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-').lower()
        if anchor_text in self.anchor_count:
            self.anchor_count[anchor_text] += 1
            anchor_id = f'{anchor_text}-{self.anchor_count[anchor_text]}'
        else:
            self.anchor_count[anchor_text] = 0
            anchor_id = anchor_text

        # 处理标题序号
        while level > self.last_level:
            self.last_level += 1
        while level < self.last_level:
            self.last_level -= 1
            # 重置下级标题的计数
            for i in range(self.last_level, len(self.level_counts)):
                self.level_counts[i] = 0
                
        self.level_counts[level - 1] += 1
        
        # 生成序号
        number = '.'.join(map(str, self.level_counts[:level]))

        # 提取标题信息、锚点 ID 和序号
        self.toc.append((level, text, anchor_id, number))

        # 渲染标题并添加锚点 ID
        return f'<h{level} id="{anchor_id}">{number}. {text}</h{level}>'

    def block_code(self, code, lang="text"):
        lang = lang.strip()
        if lang == "":
            lang = "text"
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        elif lang == "mermaid":
            # 生成 Mermaid 专用的 HTML 结构
            return f'\n<div class="mermaid">\n{code}\n</div>\n'

        # 其他代码块使用默认渲染逻辑
        # return super().block_code(code, lang)

        # use highlight
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = py_html.HtmlFormatter()
        return highlight(code, lexer, formatter)


def gen_title(link=""):
    """ Filter Title from HTML metadata """

    import re
    html_data = BeautifulSoup(open(link,"r").read(),"html.parser")
    obj = html_data.find('h1',{'class':'title'})
    if obj:
        title = obj.text
    else:
        obj = html_data.find("title")
        if obj:
            title = obj.text
        else:
            obj = html_data.find_all('h1')
            title = obj[0].text if obj else link

    return title

def get_toc_html(toc=""):
    toc_html = '<h1>目录</h1><ul>'
    last_level = 1
    
    for level, text, anchor_id, number in toc:
        while level > last_level:
            toc_html += '<ul>'
            last_level += 1
        while level < last_level:
            toc_html += '</ul>\n'
            last_level -= 1
            
        toc_html += f'<li><a href="#{anchor_id}">{number}. {text}</a></li>\n'

    while last_level > 1:
        toc_html += '</ul>\n'
        last_level -= 1
    toc_html += '</ul>\n'
    return toc_html

def md2html(mdstr="", meta_text=""):
    #import markdown
    
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
            'markdown.extensions.tables','markdown.extensions.toc',
            'code-friendly', 'fenced-code-blocks', 'footnotes']

    html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    %s
    </head>
    <body>
    %s
    </body>
    </html>
    '''

    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer,plugins=[plugin_table,plugin_task_lists,plugin_url,plugin_strikethrough,plugin_footnotes,plugin_abbr])

    if "[TOC]" in mdstr:
        ret = markdown(mdstr.replace("[TOC]", ""))
        toc = markdown.renderer.toc
        toc_html = get_toc_html(toc)    
        ret = toc_html + ret
    else:
        ret = markdown(mdstr)
    
    return html % (meta_text,ret)

def to_page_mk2(notename=""):
    import codecs,os, time
    # from orgnote.markdown import Markdown


    css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
</style>
'''


    # print("to_page_mk2(%s)" % notename)

    meta_text = ""
    md_text = ""
    has_header = True
    in_header = False
    end_header = False
    with codecs.open(notename, mode="r", encoding="utf-8") as input_file:
        for line in input_file:
            if not end_header and not in_header and line.strip() and not line.strip().startswith("---"):
                has_header = False
                md_text += line
                continue

            if has_header and not end_header and not in_header and line.strip().startswith("---"):
                in_header = True
                continue

            if in_header and line.strip().startswith("---"):
                in_header = False
                end_header = True
                continue

            if in_header:
                line = [i.strip() for i in line.strip().split(":")]
                name = line[0] if line else ""
                text = ':'.join(line[1:]) if line else ""
                if name == "title":
                    meta_text += "<title>%s</title>\n" % text
                elif name == "tags":
                    meta_text += '<meta name="keywords" content="%s" />\n' % text
                elif name == "author":
                    meta_text += '<meta name="author" content="%s" />\n' % text
                elif name == "reading-mode" and text == "yes":
                    meta_text += '<meta name="reading-mode" content="yes" />\n'
                elif name == "date":
                    try:
                        text = time.strptime(text,"%Y/%m/%d")
                    except ValueError:
                        text = time.strptime(text,"%Y-%m-%d %H:%M:%S")
                    except Exception as e:
                        print(e)
                        text = time.strftime("%Y/%m/%d")
                    finally:
                        text = time.strftime("%Y/%m/%d",text)
                        
                    meta_text += '<meta name="generated" content="%s" />\n' % text
                else:
                    continue
            else:
                md_text += line
                # md_text += "\n"
            
    # mk = Markdown()
    # html = mk.mk2html(text)

    # print(text)
    # print("="*20)
    # print("="*20)
    # print("="*20)
    # print(meta_text)
    # print("="*20)
    # print(md_text)
    # print("="*20)
    
    html = md2html(md_text,meta_text)

    html_file = notename.replace(".md",".html")
    # print("save to " + html_file)
    
    with codecs.open(html_file, "w",encoding="utf-8",errors="xmlcharrefreplace") as output_file:
        output_file.write(html)
    

def to_page_mk(notename=""):
    '''
    convert markdown to html
    '''
    import os
    import markdown
    import codecs

    css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
</style>
'''
    
        
    input_file = codecs.open(notename, mode="r", encoding="utf-8")
    text = input_file.read()
    
    if notename.endswith(".md"):
        print(notename)
        print(text)

    html = markdown.markdown(text)
    output_file = codecs.open(notename.replace(".md",".html"), "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(css+html)

def to_page(notename=""):
    import os,os.path
    try:
        emacs_version = [int(i) for i in get_emacs_version()]
        if emacs_version[0] >= 24:
            #cmd = "emacs -l scripts/ox-html.el --batch %s --funcall org-html-export-to-html 2>/dev/null" % notename
            cmd = "emacs -l scripts/init-orgnote.el --batch '%s' --funcall org-html-export-to-html 2>/dev/null" % notename
        else:
            cmd = "emacs -l scripts/init-orgnote.el --batch '%s' --funcall org-export-as-html 2>/dev/null" % notename
            
        print("Run: %s" % cmd)
        os.system(cmd)
    except Exception as ex:
        print("emacs: to html",">>>>>",str(ex))
        
    html_file = notename.replace('.org','.html')

    #print("html:",html_file)
    #print("\033[32m[Note:]\033[0m: %s generated" % html_file)
    if not os.path.exists(html_file):
        print("\033[31m[ERROR]\033[0m: %s generate FAILED" % html_file)




def add_note(notename="",srcdir="notes/"):
    import os,os.path
    ### .md file
    if notename.endswith(".md"):
        if not notename.startswith(srcdir): notename = srcdir+"/"+notename
        if not os.path.exists(notename):
            import orgnote.init
            note_name = orgnote.init.create_md_note(notename)
            note_name = note_name.replace("././","./").replace("//","/")
            if note_name != None:
                print("%s init done" % note_name)
                return note_name
        else:
            print("%s exists, please use other name or delete it" % notename)
            return ""
    else:
        pass

    #### org-mode
    try:
        import os
        if not notename.endswith('.org'): notename += ".org"
        if not notename.startswith(srcdir): notename = srcdir+"/"+notename
        if not os.path.exists(notename):
            import orgnote.init
            note_name = orgnote.init.create_default_note(notename)
            note_name = note_name.replace("././","./").replace("//","/")
            if note_name != None:
                print("%s init done" % note_name)
                return note_name
        else:
            print("%s exists, please use other name or delete it" % notename)
            return ""
    except Exception as ex:
        print("add .org file:",">>>>>",str(ex))

            
def publish_note(notename="",srcdir="./notes/"):
    import glob,os.path
    if notename.startswith(srcdir):
        glob_re = notename
    else:
        glob_re = srcdir+"/????/??/??/%s" % os.path.basename(notename)
        
    for _file in reversed(sorted(glob.glob(glob_re))):
        try:
            if _file.endswith(".org"):
                _html = _file.replace(".org",".html")
                
                if not os.path.exists(_html) or os.stat(_file).st_mtime > os.stat(_html).st_mtime:
                    to_page(_file)                    
            else:
                _html = _file.replace(".md",".html")

                if not os.path.exists(_html) or os.stat(_file).st_mtime > os.stat(_html).st_mtime:
                    to_page_mk2(_file)
            return _file
        except Exception as ex:
            print(_file," >>>>> ",str(ex))
            
    return None
        


def get_emacs_version():
    import os

    return os.popen("emacs --version").readline().strip().split()[-1].split(".")
