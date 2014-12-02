#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import

import re,time,sys,os
import json
from orgnote import config
from orgnote import util

class OrgNote(object):
    def __init__(self):
        self.cfg = config.Config()
        self.notes_db = dict()

        self.dirs = ["./notes/public.org","./notes/nopublic.org"]

        self.notes = list()
        self.localnotes = list()
        self.archives = list()


        self.menus = [
            ["/public/minyi.html","归档","fa fa-sitemap","MinYi"],
            ["/public/archive.html","归档","fa fa-archive","归档"],
            ["/public/about.html","关于","fa fa-user","关于"],
        ]


        self.menus_map = {
            "MinYi":"minyi",
            "归档": "archive",
            "关于": "about"
        }


        self.minyi = [
            ["/public/tags/nopublic.html","fa fa-link","暂不公开"]
        ]
        self.keywords = list()
        self.tags = dict()
        self.page_tags = dict()
        self.timetags = dict()



    def header_prefix(self,deep=1,title=""):
        """
        gen the header of each html
        """
        
        if deep == 1:
            path = "."
        elif deep == 2:
            path = ".."
            
        return """
        <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        
        <title>%s</title>
        <meta name="author" content="%s">
        <meta name="description" content="%s">
        <meta property="og:site_name" content="%s"/>
        <meta name="Keywords" content="%s">
        
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <meta property="og:image" content="undefined"/>
        <link href="/favicon.ico" rel="icon">
        
        
        <link rel="stylesheet" href="/theme/freemind/css/bootstrap.min.css" media="screen" type="text/css">
        <link rel="stylesheet" href="/theme/freemind/css/font-awesome.css" media="screen" type="text/css">
        <link rel="stylesheet" href="/theme/freemind/css/style.css" media="screen" type="text/css">
        <link rel="stylesheet" href="/theme/freemind/css/highlight.css" media="screen" type="text/css">
        </head>
        """ % (self.cfg.cfg["general"]["title"], self.cfg.cfg["general"]["author"], self.cfg.cfg["general"]["description"], self.cfg.cfg["general"]["title"],self.cfg.cfg["general"]["keywords"])

    def body_prefix(self):
        return """
        <body>  
        <nav id="main-nav" class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        
        <div class="container">
        
        <button type="button" class="navbar-header navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        </button>
    
        <a class="navbar-brand" href="/index.html">%s</a>
        """ % self.cfg.cfg["general"]["title"]


    def gen_tag_href(self,name=""):
        if name not in ["MinYi","归档","关于"]:
            return "<a href=\"/public/tags/%s.html\"><i class=\"%s\"></i>%s</a>" % (name,name,name)
        else:
            return "<a href=\"/public/%s.html\"><i class=\"%s\"></i>%s</a>" % (self.menus_map[name],name,name)

    def gen_href(self,line=list()):
        if len(line) == 4:          # menu
            if "rss" in line[0]:
                return "<li><a href=\"%s\" title=\"%s\" target=\"_blank\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2],line[3])
            else:
                return "<li><a href=\"%s\" title=\"%s\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2],line[3])
        elif len(line) == 3:        # archive
            return "<li><a href=\"%s\" target=\"_blank\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2])
        else:
            return ""

    def body_menu(self,menus=list()):
        """
        each menu's layout: link,title,fa-name,name
        """

        output = ""
        
        output += """
        <div class="collapse navbar-collapse nav-menu">
        
        <ul class="nav navbar-nav">
        """
    
        for menu in menus:
            output += self.gen_href(menu)

        output +="""
        </ul>
        
        </div> <!-- navbar -->
        </div> <!-- container -->
        </nav>
        """

        return output


    def contain_prefix(self,tags=[],name=""):
        output =  """
        <div class="clearfix"></div>
        <div class="container">
        <div class="content">
        
        <div class="page-header">                   <!-- page-header begin -->
        <h1>%s</h1>
        </div>                                      <!-- page-header end -->
        
        <div class="row page">                      <!-- row-page begin -->
        <div class="col-md-9">                      <!-- col-md-9 begin -->
        <div class="mypage">                        <!-- mypage begin -->
        
        <div class="slogan">                        <!-- slogan begin -->
        <i class="fa fa-heart"></i>
        """ % self.cfg.cfg["general"]["subtitle"]

        if not tags:
            output += "主页君: " + self.cfg.cfg["general"]["author"]
        elif len(tags) == 1:
            output += name
            output += self.gen_tag_href(tags[0])
        else:
            output += name
            for tag in tags:
                output += self.gen_tag_href(tag)
                if tag != tags[-1]: output += " , "

            
        output += """
        </div>                                     <!-- slogan end -->
        """

        return output

    def gen_notes(self,dirs=list()):
        """
        gen each note from blog list
        """
        import os
        #global __notes__,__localnotes__
        for notedir in dirs:
            for line in open(notedir):
                line = line.strip()
                if line.startswith("#"): continue
                public = False
                local  = False
                if "- [[" in line: public = True
                if "+ [[" in line: local  = True
            
                if public or local:
                    line = line.replace("]","")
                    line = line.split('[')[2:]
                    
                    if line[0][0] == ".":
                        link = line[0]
                    else:
                        link = line[0]
                        
                    name = line[1]
            
                    if public:
                        self.notes += [[link,name]]
                    if local:
                        self.localnotes += [[link,name]]

    def contain_notes(self,data=list(),num=0,lastone=0):
        # each note

        output = ""

        for item in data:
            output += """
            <h3 class="title">
            <a href="%s">%s</a>
            <span class="date">%s </span>
            </h3>
            """ % (self.gen_public_link(item[0],"/public/"),item[1],self.gen_date(item[0]))

        
            output += """
            <div class="entry">
            <div class="row">
            <div class="col-md-12">
            """

        
            output += self.contain_note(item[0])

            sub_title = sub_title = "<h1 class=\"title\">%s</h1>" % util.gen_title(item[0])
            output = output.replace(sub_title,"")
            
            output += """
            </div> <!-- entry -->
            """
        

        if num == 0:
            prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>Newer</a></li>'
        elif num == 1:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>Newer</a></li>' % ("/index.html")
        else:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>Newer</a></li>' % ("/public/page"+str(num-1)+".html")

        if lastone == len(self.notes):
            next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>Older</a></li>'
        else:
            next_page = '<li class="next"><a href="%s" class="alignright next">Older<i class="fa fa-arrow-circle-o-right"></i></a></li>' % ("/public/page"+str(num+1)+".html")

        output += """
        <div>
        <center>
        <div class="pagination">
        <ul class="pagination">
        %s
        <li><a href="/public/archive.html" target="_blank"><i class="fa fa-archive"></i>Archive</a></li>
        %s
        </ul>
        </div>
        </center>
        </div>
        """ % (prev_page,next_page)
        
        output += self.duosuo()
        
        output += """
        </div> <!-- mypage -->
        </div> <!-- col-md-9 -->
        """ 

        return output

    def gen_prev(self,num=0):
        if num == 0:
            return ""
        else:
            return self.gen_public_link(self.notes[num-1][0],"/public/")

    def gen_next(self,num=0):
        if num == len(self.notes) - 1:
            return ""
        else:
            return self.gen_public_link(self.notes[num+1][0],"/public/")

    def gen_tag_list(self,public=True):
        if not public: return
        for num,link in enumerate(self.notes):
            keywords = self.gen_category(link[0])

            self.page_tags[link[0]] = keywords

            for key in keywords:
                if key not in self.keywords:
                    self.keywords.append(key)
                if not self.tags.has_key(key):
                    self.tags[key] = list()
                else: pass

                self.tags[key].append([link[0], link[1].strip()])

    def gen_timetag_list(self,public=True):
        if not public: return
        for num,link in enumerate(self.notes):
            # save each page in a yymm dict
            yyyymm = ''.join(self.gen_date(link[0]).split('-')[:2])
            if not self.timetags.has_key(yyyymm):self.timetags[yyyymm] = list()
            self.timetags[yyyymm].append(link)

    def contain_page(self,link="",num=0, public=True):
        #global __archives__

        output = ""
        
        data = open(link).read()
        data = re.search("(<div id=\"content\">.*</div.).*</body>",data.replace('\n','TMD')) 
        data = data.groups()[0]
        
        data = data.replace(re.search(r'<div id="postamble">.*?</div>',data).group(),'')
        data = data.replace('TMD','\n')

        if public:
            self.archives.append([self.gen_public_link(self.notes[num][0],"/public/"),"fa fa-file-o",self.notes[num][1].strip()])
            
            if num == 0:
                prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>'
            else:
                prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>' % self.gen_prev(num)
                
            if num == len(self.notes) - 1:
                next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>下一页</a></li>' 
            else:
                next_page = '<li class="next"><a href="%s" class="alignright next">下一页<i class="fa fa-arrow-circle-o-right"></i></a></li>' % self.gen_next(num)

            page_order = """
            <div>
            <center>
            <div class="pagination">
            <ul class="pagination">
            %s
            <li><a href="/public/archive.html" target="_blank"><i class="fa fa-archive"></i>Archive</a></li>
            %s
            </ul>
            </div>
            </center>
            </div>
            """ % (prev_page,next_page)
        else:
            page_order = ""

            
        if "<div class=\"ds-thread\">" in data:
            index = data.find("<div class=\"ds-thread\">")
            data = data[:index] + page_order + data[index:]
        elif "</body>" in data:
            index = data.find("</body>")
            data = data[:index] + page_order + self.duosuo() + data[index:]
        elif "<div id=\"postamble\">" in data:
            index = data.find("<div id=\"postamble\">")
            data = data[:index] + page_order + self.duosuo() + data[index:]
        else:
            pass #print "ignore prev"


        output += data
        output += "</div> <!-- col-md-12 -->"
        output += "</div> <!-- row -->"
        
        return output
    
    def contain_note(self,link=""):
        import re
        
        output = ""
        
        alldata = open(link).read()
        
        data=re.search("(<div id=\"content\">.*<div id=\"outline-container-1\" class=\"outline-2\">).*</body>",alldata.replace('\n','TMD'))
        data2=re.search("(<div id=\"content\">.*<div class=\"ds-thread\"></div>).*</body>",alldata.replace('\n','TMD'))
        data3=re.search("(<div id=\"content\">.*<div id=\"postamble\">).*</body>",alldata.replace('\n','TMD'))
        
        if data:
            data = data.groups()[0].replace('TMD','\n')
            data = data.replace("<div id=\"outline-container-1\" class=\"outline-2\">","</div>")
            data = data.replace("#sec",self.gen_public_link(link,"/public/") + "#sec")
            output += data
        else:
            if data2:
                data = data2
            elif data3:
                data = data3

            data = data.groups()[0].replace('TMD','\n')
            data = data.replace('TMD','\n')
            data = data.split('</p>')[:5]
            output += '</p>'.join(data)
            output += "</div>"

        

        output +=  """
        <footer>
        <div class="alignleft">
        <a href="%s#more" class="more-link">阅读全文</a>
        </div>
        <div class="clearfix"></div>
        </footer>
        """ % self.gen_public_link(link,"/public/")
        
        output += "</div> <!-- col-md-12 -->"
        
        output += "</div> <!-- row -->"
        
        return output

    def contain_archive(self,data=list()):
        
        output = ""
        

        output += """
        <!-- display as entry -->
        <div class="entry">
        <div class="row">
        <div class="col-md-12">
        """
        
        for archive in data:
            if len(archive) == 2:
                newarchive = ["/public/"+archive[0].split('/')[-1],'fa fa-file-o',archive[1]]
                output += self.gen_href(newarchive)
            else:
                output += self.gen_href(archive)

        output += """
        </div>
        </div>
        </div>
        """
        
        output += """
        </div> <!-- mypage -->
        </div> <!-- col-md-9 -->
        """
        
        return output
    
    def contain_about(self):
        """about me page"""

        output = ""

        output += """
        <!-- display as entry -->
        <div class="entry">
        <div class="row">
        <div class="col-md-12">
        
        <p>这是一个建立在<code><a class="i i1 fc01 h" hidefocus="true" href="https://www.github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a></code>上的博客.</p>
        </div>
        </div>
        </div>             
        """

        output += self.duosuo()

        output += """
        </div> <!-- mypage -->
        </div> <!-- col-md-9 -->
        """
        
        return output

    def duosuo(self):
        return """
        """
        
    def contain_sidebar(self):
        return """
        <div class="col-md-3">
        <div id="sidebar">
        """

    def sidebar_tags(self):
    
        output = ""
        
        output += """
        <div class="widget">
        <h4>标签云</h4>
        <ul class="tag_box inline list-unstyled">
        """
        
        for key in self.keywords:
            output += "<li><a href=\"/public/tags/%s.html\">%s<span>%s</span></a></li>" % (key,key,len(self.tags[key]))

        output += """
        </ul>
        </div>
        """

        return output

    def sidebar_date(self):
        output = ""
        output += """
        <div class="widget">
        <h4>时间机器</h4>
        <ul class="tag_box inline list-unstyled">
        """
        tot = 0
        for key in sorted(self.timetags.keys(),reverse=True):
            output += "<li><a href=\"/public/tags/%s.html\">%s<span>%s</span></a></li>" % (key,key,len(self.timetags[key]))
            tot += len(self.timetags[key])
        output += "<li><a href=\"/public/archive.html\">All<span>%s</span></a></li>" % (tot)
        
        output += """
        </ul>
        </div>
        """
        return output

    def sidebar_latest(self,notes=list(), num=6):
        """
        each note layout: link,name
        """
        output = ""
        
        output += """
        <div class="widget">
        <h4>最新文章</h4>
        <ul class="entry list-unstyled">
        """
        
        for note in notes[:num]:
            output += "<li><a href=\"%s\"><i class=\"fa fa-file-o\"></i>%s</a></li>" % (self.gen_public_link(note[0].replace('"',""),"/public/"),note[1])
            
        output += """
        </ul>   
        </div> 
        """
        
        return output

    def sidebar_weibo(self):
        return """
        """

    def sidebar_link(self):
        return """
        <div class="widget">
        <h4>快速链接</h4>
        <ul class="entry list-unstyled">
        <li><a href="http://lesliezhu.github.com" title="LeslieZhu's Github" target="_blank"><i class="fa fa-github"></i>Leslie Zhu</a></li>
        <li><a href="https://github.com/LeslieZhu/OrgNote" title="OrgNote" target="_blank"><i class="fa fa-github"></i>OrgNote</a></li>
        <li><a href="https://github.com/LeslieZhu/orgnote-theme-freemind" title="OrgNote" target="_blank"><i class="fa fa-github"></i>orgnote-theme-freemind</a></li>
        </ul>
        </div>
        """

    def contain_suffix(self):
        return """
        </div> <!-- sidebar -->
        </div> <!-- col-md-3 -->
        </div> <!-- row-fluid -->
        </div>
        </div>
        """

    def header_suffix(self):
        return """
        <div class="container-narrow">
        <footer>
        <p>&copy; 2014 %s
        with help from <a href="https://github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a>. Theme by <a href="https://github.com/LeslieZhu/orgnote-theme-freemind">orgnote-theme-freemind</a>.  Published with GitHub Pages. 
        </p> </footer>
        </div> <!-- container-narrow -->
        
        <a id="gotop" href="#">   
        <span>▲</span> 
        </a>
        
        <!--<link rel="stylesheet" href="./fancybox/jquery.fancybox.css" media="screen" type="text/css">-->
        
        </body>
        </html>
        """ % self.cfg.cfg["general"]["author"]

    def gen_public_link(self,link="",prefix="public/"):
        return prefix+link.split('/')[-1]

    def gen_archive(self):
        output = open("./public/archive.html","w")
        print >> output,self.header_prefix(title="归档")
        print >> output,self.body_prefix()
        print >> output,self.body_menu(self.menus)
        print >> output,self.contain_prefix(["归档"],"")
        print >> output,self.contain_archive(self.archives)              # auto gen
        print >> output,self.contain_sidebar()
        print >> output,self.sidebar_latest(self.notes)            # auto gen
        print >> output,self.sidebar_tags()
        print >> output,self.sidebar_date()
        print >> output,self.sidebar_weibo()
        print >> output,self.sidebar_link()
        print >> output,self.contain_suffix()
        print >> output,self.header_suffix()
        output.close()
        
    def gen_page(self,note=list(),num=0,public=True):
        output = open(self.gen_public_link(note[0]),"w")
        print >> output,self.header_prefix(2,note[1].strip())
        print >> output,self.body_prefix()
        print >> output,self.body_menu(self.menus)
        if public:
            print >> output,self.contain_prefix(self.page_tags[note[0]],"标签: ")
        else:
            print >> output,self.contain_prefix(['nopublic'],"标签: ")
        print >> output,self.contain_page(note[0],num,public)              # auto gen
        print >> output,self.contain_sidebar()
        print >> output,self.sidebar_latest(self.notes)            # auto gen
        print >> output,self.sidebar_tags()
        print >> output,self.sidebar_date()
        print >> output,self.sidebar_weibo()
        print >> output,self.sidebar_link()
        print >> output,self.contain_suffix()
        print >> output,self.header_suffix()
        output.close()
        
    def gen_public(self):
        for i,note in enumerate(self.notes):
            self.gen_page(note,i)
        for i,note in enumerate(self.localnotes):
            self.gen_page(note,i,False)

    def split_index(self,num,b_index,e_index):
        """
        split index.html as page1,page2,page3...,so do not need display all notes in homepage
        """
        if num == 0:
            output = open("index.html","w")
        else:
            output = open("public/page"+str(num)+".html","w")

        print >> output,self.header_prefix(title=self.cfg.cfg["general"]["title"])
        print >> output,self.body_prefix()
        print >> output,self.body_menu(self.menus)
        print >> output,self.contain_prefix()    
        print >> output,self.contain_notes(self.notes[b_index:e_index],num,e_index)              # auto gen
        print >> output,self.contain_sidebar()
        print >> output,self.sidebar_latest(self.notes)            # auto gen
        print >> output,self.sidebar_tags()
        print >> output,self.sidebar_date()
        print >> output,self.sidebar_weibo()
        print >> output,self.sidebar_link()
        print >> output,self.contain_suffix()
        print >> output,self.header_suffix()
        output.close()

    def gen_index(self,note_num=6):
        """
        each split page hold `num` notes
        """

        num = 0
        b_index = 0
        e_index = b_index + note_num
        tot = len(self.notes)

        while num <= tot:
            if b_index > tot:
                break
            elif b_index <= tot and e_index > tot:
                self.split_index(num,b_index,tot)
            else:
                self.split_index(num,b_index,e_index)
                
            num += 1
            b_index += note_num
            e_index = b_index + note_num
            
    def gen_about(self):
        output = open("./public/about.html","w")
        print >> output,self.header_prefix(title="关于")
        print >> output,self.body_prefix()
        print >> output,self.body_menu(self.menus)
        print >> output,self.contain_prefix(["关于"],"")
        print >> output,self.contain_about()
        print >> output,self.contain_sidebar()
        print >> output,self.sidebar_latest(self.notes)
        print >> output,self.sidebar_tags()
        print >> output,self.sidebar_date()
        print >> output,self.sidebar_weibo()
        print >> output,self.sidebar_link()
        print >> output,self.contain_suffix()
        print >> output,self.header_suffix()
        output.close()

    def gen_minyi(self):
        output = open("./public/minyi.html","w")
        print >> output,self.header_prefix(title="MinYi")
        print >> output,self.body_prefix()
        print >> output,self.body_menu(self.menus)
        print >> output,self.contain_prefix(["MinYi"],"")
        print >> output,self.contain_archive(self.minyi)
        print >> output,self.contain_sidebar()
        print >> output,self.sidebar_latest(self.notes)
        print >> output,self.sidebar_tags()
        print >> output,self.sidebar_date()
        print >> output,self.sidebar_weibo()
        print >> output,self.sidebar_link()
        print >> output,self.contain_suffix()
        print >> output,self.header_suffix()
        output.close()

    def gen_tags(self):
        for key in self.keywords:
            output = open("./public/tags/" + key + ".html","w")
            print >> output,self.header_prefix(title=key)
            print >> output,self.body_prefix()
            print >> output,self.body_menu(self.menus)
            print >> output,self.contain_prefix([key],"分类: ")
            #print >> output,self.contain_notes(__tags__[key])
            print >> output,self.contain_archive(self.tags[key])              # auto gen
            print >> output,self.contain_sidebar()
            print >> output,self.sidebar_latest(self.notes)
            print >> output,self.sidebar_tags()
            print >> output,self.sidebar_date()
            print >> output,self.sidebar_weibo()
            print >> output,self.sidebar_link()
            print >> output,self.contain_suffix()
            print >> output,self.header_suffix()
            output.close()
            
    def gen_timetags(self):
        for key in sorted(self.timetags.keys(),reverse=True):
            output = open("./public/tags/" + key + ".html","w")
            print >> output,self.header_prefix(title=key)
            print >> output,self.body_prefix()
            print >> output,self.body_menu(self.menus)
            print >> output,self.contain_prefix([key],"月份: ")
            print >> output,self.contain_archive(self.timetags[key])
            print >> output,self.contain_sidebar()
            print >> output,self.sidebar_latest(self.notes)
            print >> output,self.sidebar_tags()
            print >> output,self.sidebar_date()
            print >> output,self.sidebar_weibo()
            print >> output,self.sidebar_link()
            print >> output,self.contain_suffix()
            print >> output,self.header_suffix()
            output.close()

    def gen_nopublic(self):
        output = open("./public/tags/nopublic.html","w")
        print >> output,self.header_prefix(title="nopublic")
        print >> output,self.body_prefix()
        print >> output,self.body_menu(self.menus)
        print >> output,self.contain_prefix(["nopublic"],"分类: ")
        print >> output,self.contain_archive(self.localnotes)              # auto gen
        print >> output,self.contain_suffix()
        print >> output,self.header_suffix()
        output.close()
    
    def gen_date(self,link=""):
        """ Filter Publish data from HTML metadata>"""

        for line in open(link).readlines():
            if "<meta name=\"generated\"" in line:
                line = line.strip()
                #pattern="([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])"
                pattern="\"([0-9].*[/-]?[0-9].*[/-]?[0-9].*)\""
                try:
                    pubdate=re.search(pattern,line).groups(1)[0]
                except Exception,e:
                    print e
                    sys.exit(-1)
                    break
        if "/" in pubdate:
            try:
                pubdate=time.strptime(pubdate, "%m/%d/%Y")
            except ValueError:
                pubdate=time.strptime(pubdate, "%Y/%m/%d")
            except exp,e:
                print e
                sys.exit(-1)
                
        elif "-" in pubdate:
            try:
                pubdate=time.strptime(pubdate, "%Y-%m-%d")
            except ValueError:
                pubdate=time.strptime(pubdate, "%m-%d-%Y")
            except exp,e:
                print e
                sys.exit(-1)
        else:
            pubdate=time.strptime(pubdate, "%Y%m%d")

        pubdate=time.strftime("%Y-%m-%d %a",pubdate)
        return pubdate



    def gen_category(self,link=""):
        """ Filter Keywords from HTML metadata """
    
        keywords = ""
        for line in open(link).readlines():
            if "<meta name=\"keywords\"" in line:
                line = line.strip()
                keywords=re.search("content=\"(.*)\"",line).groups(1)[0].strip()
                break

        if len(keywords) > 0:
            return [i.strip() for i in keywords.split(",")]
        else:
            return ["札记"]

    
    def do_server(self,port="8080"):
        try:
            os.system("python -m SimpleHTTPServer %s" % port)
        except Exception,ex:
            print str(ex)
            usage()

    def do_deploy(self):
        #if not os.path.exists("./.git/"):
        #    print "please config git-url in _config.ini, and run:"
        #    print "git init"
        #else:
        print "run:"
        print "git add index.html _config.ini notes/ public/ scripts/ theme/"
        print "git commit -m \"update\""
        print "git push origin master"
            #cmd = "git add index.html _config.ini notes/ public/ scripts/ theme/;git commit -m \"update\";git push origin master"
            #os.system(cmd)

    def do_generate(self):
        self.cfg.update()
        self.gen_notes(self.dirs)
        self.gen_tag_list()
        self.gen_timetag_list()
        self.gen_public()
        self.gen_index()
        self.gen_about()
        self.gen_minyi()
        self.gen_archive()
        self.gen_tags()
        self.gen_timetags()
        self.gen_nopublic()
        print "notes generate done" 

    def do_new(self,notename=""):
        return util.add_note(notename)

    def do_page(self,notename=""):
        return util.to_page(notename)

    def do_publish(self,notename=""):
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]
        publish_line = util.publish_note(notename)

        nopublish_data = open(nopublish_list,"r").readlines()
        nopublish_data = [i.strip().replace("+ [[","- [[") for i in nopublish_data]

        if not os.path.exists(publish_list):
            output = open(publish_list,"w")
            self.scan()
            for _note in reversed(sorted(self.notes_db.keys())):
                publish_line = util.publish_note(self.notes_db[_note])
                
                if publish_line in nopublish_data: 
                    continue
                print >> output,publish_line
            output.close()
        else:
            publish_line = util.publish_note(notename)

            if publish_line == None:
                print "ERROR: Can not publish note: %s, are you sure it exists?" % notename
                return

            data = open(publish_list,"r").readlines()
            data = [i.strip() for i in data]

            if publish_line in data or publish_line in nopublish_data:
                print "publish done"
                return
            output = open(publish_list,"w")
            print >> output,publish_line
            for line in data:
                if line in nopublish_data: 
                    continue
                print >> output,line
            output.close()
        print "publish done"

    def scan(self,note_dir = "./notes"):
        """
        scan the note_dir, build a dict with notes
        """

        for path,dirs,files in os.walk(note_dir):
            for _file in files:
                if not _file.endswith(".org"):continue
                _path = path + '/' + _file
                if _path == "./notes/public.org" or _path == "./notes/nopublic.org": continue
                if _path.endswith(".html"):continue
                self.notes_db[_path] = _file

    def do_list(self):
        """
        list all notes
        """
        self.scan()
        for _note in reversed(sorted(self.notes_db.keys())):
            print _note

    def do_status(self):
        
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]
        
        publish_data = open(publish_list,"r").readlines()
        publish_data = [i.strip() for i in publish_data]

        nopublish_data = open(nopublish_list,"r").readlines()
        nopublish_data = [i.strip().replace("+ [[","- [[") for i in nopublish_data]
        
        all_publish = True
        self.scan()
        for _note in reversed(sorted(self.notes_db.keys())):
            publish_line = util.publish_note(self.notes_db[_note])
            if publish_line not in publish_data and publish_line not in nopublish_data:
                print "%s not publish yet!" % _note
                all_publish = False

        if all_publish:
            print "all notes published!"
            
        

def usage():
    import sys
    
    print """
    Usage: orgnote <command>

    Commands:
    init       Create a new OrgNote folder
    new        Create a new .org post
    list       List this blog notes
    status     Status of those notes
    publish    Publish a note
    generate   Generate static files
    server     Start the server
    deploy     Deploy your website
    help       Get help on a command
    version    Display version information
    
    For more help, you can check the docs:  http://lesliezhu.github.io/OrgNote/
     """
    sys.exit()
            



def main(args=None):
    import sys,os
    import orgnote
    import orgnote.parser
    import orgnote.init

    blog = orgnote.parser.OrgNote()

    if len(sys.argv) == 2:
        if sys.argv[1] == "server":
            blog.do_server()
        elif sys.argv[1] == "init":
            print "init...."
            orgnote.init.main()
        elif sys.argv[1] == "deploy":
            blog.do_deploy()
        elif sys.argv[1] == "version":
            print orgnote.__version__
        elif sys.argv[1] == "generate":
            blog.do_generate()
        elif sys.argv[1] == "list":
            blog.do_list()
        elif sys.argv[1] == "status":
            blog.do_status()
        else:
            usage()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "server":
            blog.do_server(sys.argv[2])
        elif sys.argv[1] == "new":
            blog.do_new(sys.argv[2])
        elif sys.argv[1] == "publish":
            blog.do_publish(sys.argv[2])
        else:
            usage()
    else:
        usage()

if __name__ == "__main__":
    import sys
    sys.exit(main())
