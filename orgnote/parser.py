#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import print_function
from __future__ import absolute_import

import re
import sys,os
import time,datetime
import calendar

#import subprocess,shlex
import json

#import socketserver
from bs4 import BeautifulSoup, Comment
from multiprocessing import Process
from functools import partial

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from orgnote import config
from orgnote import util
from orgnote.colorsrc import get_hightlight_src



if sys.version_info.major == 3:
    from imp import reload
    reload(sys)
else:
    reload(sys)                    
    sys.setdefaultencoding('utf-8')


class OrgNoteFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, orgobj,fn,port=""):
        super(OrgNoteFileSystemEventHander, self).__init__()
        self.restart = fn
        self.port = port
        self.orglist = [orgobj.calendar_jobfile, orgobj.links_file,orgobj.nopublic_file, orgobj.public_file, orgobj.slinks_file]

    def on_any_event(self, event):
        if event.src_path.endswith('.html') or os.path.basename(event.src_path) in self.orglist:
            print('orgnote source file changed: %s' % event.src_path)
            self.restart(self.port)
            
class OrgNote(object):
    def __init__(self):
        self.cfg = config.Config()
        self.emacs_version = [int(i) for i in util.get_emacs_version()]
        
        # update settings
        self.refresh_config()


    def refresh_config(self,homepage=""):
        self.notes_db = {}
        self.notes = []
        self.localnotes = []
        self.archives = []
        self.keywords = []
        self.tags = {}
        self.page_tags = {}
        self.timetags = {}
        
        self.slinks = []
        self.links_default_title = "其它"
        self.links_title_key = 'titles'
        self.links = {self.links_default_title:[],self.links_title_key:[]}

        self.job_today = []
        self.job_week = []
        self.job_prev = []      # last week jobs
        self.job_done = []      # all finished jobs
        
        self.__pagenames__ = {}
        self.cjk_num = 0



        # general option
        self.title = self.cfg.cfg.get("title","OrgNote")
        self.subtitle = self.cfg.cfg.get("subtitle","OrgNote")
        self.author = self.cfg.cfg.get("author","OrgNote")
        self.email = self.cfg.cfg.get("email","")
        self.description = self.cfg.cfg.get("description","")
        self._keywords = self.cfg.cfg.get("keywords","OrgNote")
        self.language = self.cfg.cfg.get("language","zh-CN")
        
        # blog option        
        self.homepage = self.cfg.cfg.get("url","https://github.com/LeslieZhu/OrgNote") if not homepage else homepage    
        self.blogroot = self.cfg.cfg.get("root","/")
        
        self.source_dir = "./" + self.cfg.cfg.get("source_dir","notes") +'/'

        self.images_dir = self.cfg.cfg.get("images_dir","images")
        self.files_dir = self.cfg.cfg.get("files_dir","data")

        self.public  = self.cfg.cfg.get("public_dir","public")
        self.public_dir = './' + self.public + '/'
        self.sync_dirs = self.cfg.cfg.get("sync_dirs",list())

        self.public_file = self.cfg.cfg.get("public_file","public.org")
        self.nopublic_file = self.cfg.cfg.get("nopublic_file","nopublic.org")
        
        self.tags_dir = self.public_dir + "/tags"
        
        #if not os.path.exists(self.tags_dir):os.makedirs(self.tags_dir)        
        #    os.makedirs(self.tags_dir)        
                
        self.deploy_type = self.cfg.cfg.get("deploy_type","git")
        self.deploy_url = self.cfg.cfg.get("deploy_url","")
        self.deploy_branch = self.cfg.cfg.get("deploy_branch","master")

        self.theme = self.cfg.cfg.get("theme","freemind")
        self.css_highlight = self.cfg.cfg.get("css_highlight","default")

        self.duoshuo_shortname = self.cfg.cfg.get("duoshuo_shortname",None)
        self.weibo_shortname = self.cfg.cfg.get("weibo_shortname",None)
        self.utteranc_repo = self.cfg.cfg.get("utteranc_repo",None)
        self.weixin_name = self.cfg.cfg.get("weixin_name",None)
        self.weixin_public = self.cfg.cfg.get("weixin_public",None)
        
        self.donate_name = self.cfg.cfg.get("donate_name","赞赏支持")
        self.donate_alipay = self.cfg.cfg.get("donate_alipay","")
        self.donate_wechatpay = self.cfg.cfg.get("donate_wechatpay","")

        self.rss_type = self.cfg.cfg.get("rss_type","ReadMore")
        if self.rss_type not in ["ReadMore","ReadAll"]:
            self.rss_type = "ReadMore"

        self.default_tag = self.cfg.cfg.get("default_tag", u"默认")
        self.default_tag_list = self.default_tag.split(',')
        self.nopublic_tag = self.cfg.cfg.get("nopublic_tag",u"暂不公开")
        
        self.ignore_tags = self.cfg.cfg.get("ignore_tags", u"")
        self.ignore_tags_list = self.ignore_tags.split(',')
        
        self.rdmode_keyword = self.cfg.cfg.get("reading_mode_keyword",u"随笔")
        self.rdmode_keyword_list = self.rdmode_keyword.split(',')


        self.per_page = self.cfg.cfg.get("per_page",6)
        self.auto_publish = self.cfg.cfg.get("auto_publish",True);
        # self.auto_md2html = self.cfg.cfg.get("auto_md2html",True);

        self.sidebar_show = self.cfg.cfg.get("sidebar_show",0)
        self.sidebar_show_page = self.cfg.cfg.get("sidebar_show_page",0)
        self._sidebar_contact = self.cfg.cfg.get("sidebar_contact","")
        self._sidebar_contact_name = self.cfg.cfg.get("sidebar_contact_name","联系/反馈")
        self.sidebar_list = self.cfg.cfg.get("sidebar",list())
        
        self.dirs = [self.source_dir + self.public_file, self.source_dir + self.nopublic_file]
                        
        self.menu_list = self.cfg.cfg.get("menu_list",dict())

        self.replace_str_list = self.cfg.cfg.get("replace_str",list())
        
        self.slinks_name = self.cfg.cfg.get("slinks_name","友情链接")
        self.slinks_file = self.cfg.cfg.get("slinks_file","slinks.org")
        if self.slinks_file:
            self.slinks_file = self.source_dir + self.slinks_file

        self.links_name = self.cfg.cfg.get("links_name","觅链")        
        self.links_file = self.cfg.cfg.get("links_file","links.org")
        if self.links_file:
            self.links_file = self.source_dir + self.links_file
        

        self.shift_hour = self.cfg.cfg.get("shift_hour",0)
        self.calendar_name = self.cfg.cfg.get("calendar_name","")
        self.calendar_jobfile = self.cfg.cfg.get("calendar_jobfile","calendar.org")
        if self.calendar_jobfile:
            self.calendar_jobfile = self.source_dir + self.calendar_jobfile
        

        if self.sidebar_show == 1:
            self.col_md_index = "col-md-9"
            self.col_md_index_r = "col-md-3"
        else:
            self.col_md_index = "col-md-12"
            self.col_md_index_r = ""
            
        if self.sidebar_show_page == 1:
            self.col_md_page = "col-md-9"
            self.col_md_page_r = "col-md-3"
        else:
            self.col_md_page = "col-md-12"
            self.col_md_page_r = ""

        # homepage will update in local/remote server mode
        self.public_url = self.homepage + re.sub("//*","/",self.blogroot + '/')
        self.search_path = "search.json"

        # depends on public_url
        self.menus = [
            [self.public_url + "links.html",self.links_name,"fa fa-sitemap",self.links_name],
            [self.public_url + "archive.html","归档","fa fa-archive","归档"],
            [self.public_url + "tags.html","标签","fa fa-tags","标签"],
            [self.public_url + "calendar.html", self.calendar_name, "fa fa-calendar",self.calendar_name] if self.calendar_name else None,
            [self.public_url + "about.html","说明","fa fa-user","说明"],
            [self.public_url + "rss.xml","订阅","fa fa-rss","订阅"],
            [self.public_url + self.search_path,"搜索","fa fa-search fa-fw","搜索"]
        ]

        
        self.menus_map = {
            self.links_name: "links.html",
            "归档": "archive.html",
            "说明": "about.html",
            "标签": "tags.html",
            "订阅": "rss.xml"
        }

        if self.calendar_name:
            self.menus_map[self.calendar_name] = "calendar.html"


        for _menu in self.menu_list:
            menu = self.menu_list[_menu]
            if menu["url"].endswith(".html"):
                _url = menu["url"]
            else:
                _url = menu["url"] + ".html"
                
            _item = [self.public_url + _url,menu["title"],menu["icon"],menu["title"]]
            if _item not in self.menus:
                self.menus.append(_item)
                self.menus_map[menu["title"]] = _url.strip(".html")


        if os.path.exists(self.links_file):
            curtitle = self.links_default_title
            for link in open(self.links_file,"r").readlines():
                link = link.strip()
                if not link: continue
                if link.startswith("#"): continue

                if link.startswith("*"):
                    curtitle = ''.join(link.split(" ")[1:])
                    self.links[curtitle] = []
                    self.links[self.links_title_key].append(curtitle)
                    continue
                
                link = [i.strip() for i in link.split(',')]
                
                if len(link) >= 3:
                    url,name,icon = link[:3]
                elif len(link) == 2:
                    url,name = link
                    icon = "fa fa-link"
                else:
                    url = name = link[0]
                    icon = "fa fa-link"
            
                item = [url,icon,name]
                if item not in self.links[curtitle]:
                    self.links[curtitle].append(item)
        #
        # self.links[self.links_title_key].append(self.links_default_title)
        # nopublic_link = [self.public_url + "tags/" + self.nopublic_tag + ".html","fa fa-link",self.nopublic_tag]
        # if nopublic_link not in self.links[self.links_default_title]:
            # self.links[self.links_default_title].append(nopublic_link)

    def header_prefix(self,deep=1,title=""):
        """
        gen the header of each html
        """
        
        if deep == 1:
            path = "."
        elif deep == 2:
            path = ".."

        if not title:
            title = self.title
            
        return """
        <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        %s
        <title>%s</title>
        <meta name="author" content="%s">
        <meta name="email" content="%s">
        <meta name="description" content="%s">
        <meta property="og:site_name" content="%s"/>
        <meta name="Keywords" content="%s">
        
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <meta property="og:image" content="undefined"/>

        <link href="%sfavicon.ico" rel="icon">
        
        <link rel="stylesheet" href="%stheme/%s/css/bootstrap.min.css" media="screen" type="text/css">
        <link rel="stylesheet" href="%stheme/%s/css/font-awesome.css" media="screen" type="text/css">
        <link rel="stylesheet" href="%stheme/%s/css/style.css" media="screen" type="text/css">
        <link rel="stylesheet" href="%stheme/%s/css/highlight.css" media="screen" type="text/css">
        <link rel="stylesheet" href="%stheme/%s/css/%s-highlight.css" media="screen" type="text/css">
        <script type="text/javascript" src="%stheme/%s/js/jquery-2.0.3.min.js"></script>
        <script type="text/javascript" src="%stheme/%s/js/local-search.js?v=7.4.1"></script>

        <script type="text/javascript" src="%stheme/%s/js/mermaid-10.6.1.min.js"></script>
        <script>
            mermaid.initialize({ startOnLoad: true });
        </script>
        
        <ORGNOTESTYLE>
        </head>
        """ % (self.js_config(),title, self.author, self.email, self.description, self.title,self._keywords,
               self.blogroot,
               self.blogroot,self.theme,
               self.blogroot,self.theme,
               self.blogroot,self.theme,
               self.blogroot,self.theme,
               self.blogroot,self.theme,self.css_highlight,
               self.blogroot,self.theme,
               self.blogroot,self.theme,
               self.blogroot,self.theme
        )

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
    
        <a class="navbar-brand" href="%sindex.html">%s</a>
        """ % (self.blogroot,self.title)

    def gen_tag_href(self,name=""):
        if name not in self.menus_map.keys():
            return "<a href=\"%stags/%s.html\"><i class=\"%s\"></i>%s</a>" % (self.public_url,name,name,name)
        else:
            return "<a href=\"%s%s\"><i class=\"%s\"></i>%s</a>" % (self.public_url,self.menus_map[name],name,name)

    def gen_href(self,line=list()):
        if len(line) == 4:          # menu
            if "rss" in line[0]:
                return "<li><a href=\"%s\" title=\"%s\" target=\"_blank\"><i class=\"%s\"></i>%s</a></li>" % (line[0],line[1],line[2],line[3])
            elif "search" in line[0]:
                return """<li>
                <a role="button" class="popup-trigger">
                <i class="%s"></i>%s
                </a>
                </li>
                """ % (line[2],line[3])
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
            if not menu: continue
            output += self.gen_href(menu)

        # search label
        output += """
        <div class="site-search">
          <div class="popup search-popup">
            <div class="search-header">
              <span class="search-icon">
                <i class="fa fa-search"></i>
              </span>
            <div class="search-input-container">
              <input autocomplete="off" autocorrect="off" autocapitalize="none"
                     placeholder="Searching..." spellcheck="false"
                     type="text" id="search-input">
            </div>
            <span class="popup-btn-close">
                <i class="fa fa-times-circle"></i>
            </span>
          </div>
          <div id="search-result"></div>
        </div>
        <div class="search-pop-overlay"></div>
        """

        output +="""
        </ul>
        
        </div> <!-- navbar -->
        </div> <!-- container -->
        </nav>
        """

        return output

    def contain_prefix(self,tags=[],name="",header_title="",ispage=False):
        """
        ispage: False

        - True: it's in each note page, use self.col_md_page
        - False: it's in index page, use self.col_md_index
        """

        col_md = self.col_md_page if ispage else self.col_md_index
            
        if header_title == "":
            _header_title  = self.subtitle
        elif header_title in self.__pagenames__.keys():
            _header_title = self.__pagenames__[header_title]
        else:
            _header_title = header_title

        output =  """
        <div class="clearfix"></div>
        <div class="container">
        <div class="content">
        
        <div class="page-header">                   <!-- page-header begin -->
        <h1>%s</h1>
        </div>                                      <!-- page-header end -->
        
        <div class="row page">                      <!-- row-page begin -->
        <div class="%s">                            <!-- col-md-9/12 begin -->
        <div class="mypage">                        <!-- mypage begin -->
        
        <div class="slogan">                        <!-- slogan begin -->
        <i class="fa fa-heart"></i>
        """ % (_header_title,col_md)

        if not tags:
            output += "主页君: " + self.author
        elif len(tags) == 1 and tags[0] in self.tags:
            output += name
            output += self.gen_tag_href(tags[0])
        else:
            output += name
            for tag in tags:
                output += self.gen_tag_href(tag)
                if tag != tags[-1]: output += " , "

        return output

    def contain_prefix_end(self,link=""):
        output = ""
        if link.endswith(".html"):
            #print(link)
            #output += "<span class='date'>由「"
            #output += "<a href=\"%s%s.html\"><i class=\"%s\"></i>%s</a>" % (self.public_url,self.menus_map["说明"],"作者",self.author)
            #output += "」创作于%s</span>" % self.gen_date(link)
            output += "<span class='date'>文|<a href='%s'><i class='%s'></i>%s</a></span>" % (self.public_url+"about.html",
                                                                                                self.public_url+"about.html",
                                                                                                self.author)
            #self.public_url+"about.html",self.author
            #output += "<a href=\"%s\"><i class=\"%s\"></i>%s</a>" % (self.public_url,self.menus_map["说明"],"作者",self.author)
            #output += "<span class='date'>创作于%s</span>" % self.gen_date(link)
        else:
            pass
            
        output += """
        </div>                                     <!-- slogan end -->
        """

        return output

    def gen_notes(self,dirs=list()):
        """
        gen each note from blog list
        """
        import os
        public_file = dirs[0]
        nopublic_file = dirs[1]

        nopublic_notes = []
        for line in open(nopublic_file):
            line = line.strip()
            if not line or line.startswith("#"): continue
            
            nopublic_notes.append(line)
            
            if line.endswith(".org"):
                link = line.replace(".org",".html")
            elif line.endswith(".md"):
                util.publish_note(line,self.source_dir)
                link = line.replace(".md",".html")
            else:
                link = line

            name = util.gen_title(link)
            self.localnotes += [[link,name]]

        for line in open(public_file):                
            line = line.strip()
            if not line or line.startswith("#"): continue
            
            if line in nopublic_notes: continue

            if line.endswith(".org"):
                link = line.replace(".org",".html")
            elif line.endswith(".md"):
                util.publish_note(line,self.source_dir)
                link = line.replace(".md",".html")
            else:
                link = line

            name = util.gen_title(link)
            self.notes += [[link,name]]


    def contain_notes(self,data=list(),num=0,lastone=0):
        # each note

        output = ""

        for item in data:
            output += """
            <h3 class="title">
            <a href="%s">%s</a>
            <span class="date">%s </span>
            </h3>
            """ % (self.gen_public_link(item[0],self.public_url),item[1],self.gen_date(item[0]))


            if self.emacs_version[0] >= 24: # and self.emacs_version[1] >= 4:
                output += """<div class="%s">""" % "col-md-12" #self.col_md_index
            else:
                output += """            
                <div class="entry">
                <div class="row">
                <div class="%s">
                """ % self.col_md_index
                

        
            output += self.contain_note(item[0])

            sub_title = sub_title = "<h1 class=\"title\">%s</h1>" % util.gen_title(item[0])
            output = output.replace(sub_title,"")

            if self.emacs_version[0] >= 24:# and self.emacs_version[1] >= 4:
                output += """
                </div> <!-- %s -->
                """ % "col-md-12" #self.col_md_index
            else:
                output += """
                </div> <!-- %s -->
                </div> <!-- row -->
                </div> <!-- entry -->
                """ % "col-md-12" #self.col_md_index
        

        if num == 0:
            prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>'
        elif num == 1:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>' % (self.blogroot + "index.html")
        else:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>' % (self.public_url + "page"+str(num-1)+".html")

        if lastone == len(self.notes):
            next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>下一页</a></li>'
        else:
            next_page = '<li class="next"><a href="%s" class="alignright next">下一页<i class="fa fa-arrow-circle-o-right"></i></a></li>' % (self.public_url + "page"+str(num+1)+".html")

        output += """
        <div>
        <center>
        <div class="pagination">
        <ul class="pagination">
        %s
        <li><a href="%sarchive.html" target="_blank"><i class="fa fa-archive"></i>归档</a></li>
        %s
        </ul>
        </div>
        </center>
        </div>
        """ % (prev_page,self.public_url,next_page)
        
        output += self.duosuo()
        
        output += """
        </div> <!-- mypage -->
        </div> <!-- %s -->
        """  % "col-md-12" #self.col_md_index

        return output

    def gen_prev(self,num=0):
        if num == 0:
            return ""
        else:
            return self.gen_public_link(self.notes[num-1][0],self.public_url)

    def gen_next(self,num=0):
        if num == len(self.notes) - 1:
            return ""
        else:
            return self.gen_public_link(self.notes[num+1][0],self.public_url) if self.notes else ""

    def gen_tag_list(self,public=True):
        """
        - self.keywords is a list of all keywords
        - self.tags is a dict, a keyword's value is a list, each item is a [notefile,notetitle]
        """
        
        if not public: return
        for num,link in enumerate(self.notes):
            keywords = self.gen_category(link[0])

            self.page_tags[link[0]] = keywords

            for key in keywords:
                
                if key in self.ignore_tags_list:
                    continue
                
                if key not in self.keywords:
                    self.keywords.append(key)
                if key not in self.tags.keys():
                    self.tags[key] = list()
                else:
                    pass

                self.tags[key].append([link[0], link[1].strip()])

    def gen_timetag_list(self,public=True):
        if not public: return
        for num,link in enumerate(self.notes):
            # save each page in a yymm dict
            yyyymm = ''.join(self.gen_date(link[0]).split('-')[:2])
            if yyyymm not in self.timetags.keys():self.timetags[yyyymm] = list()
            self.timetags[yyyymm].append(link)



    def copyright(self,num=""):
        if not self.notes:
            return ""

        #
        if self.weixin_name:
            if self.weixin_public:
                wx = "<li><strong>微信搜索：</strong> <span>「 <a href='%s%s'>%s</a> 」</span>, 关注公众号!<li>" % (self.public_url,self.weixin_public,self.weixin_name)
            else:
                wx = "<li><strong>微信搜索：</strong> <span style='color:red'>「 %s 」</span>, 关注公众号!<li>" % self.weixin_name
        else:
            wx = ""
            
        output = """
        <hr>
        <div id="post-copyright">
        <ul class="post-copyright">
        <li class="post-copyright-author">
        <strong>本文作者：</strong>「
        <a href="%s" title="%s">%s</a> 」创作于%s，共%s字
        </li>
        %s
        <li class="post-copyright-link">
        <strong>本文链接：</strong>
        <a href="%s" title="%s">%s</a>
        </li>
        <li class="post-copyright-license">
        <strong>版权声明：</strong>
        原创文章，如需转载请注明文章作者和出处。谢谢！
        </li>
        </ul>
        </div>
        """ % (self.public_url+"about.html",
               self.author,self.author,
               self.gen_date(self.notes[num][0]),
               self.cjk_num,
               wx,
               self.gen_public_link(self.notes[num][0],self.public_url),
               self.notes[num][1],
               self.gen_public_link(self.notes[num][0],self.public_url))
        

        # 本博客所有文章除特别声明外，均采用 <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/" rel="external nofollow" target="_blank">CC BY-NC-SA 3.0</a> 许可协议。转载请注明出处！
        
        return output

    def get_style(self,link=""):
        output = "<style>"

        html_data = BeautifulSoup(open(link,"r").read(),"html.parser")
        obj = html_data.find('style')
        if obj:
            output += obj.text

        output += "</style>"
        return output
    
    def contain_page(self,link="",num=0, public=True):
        output = ""

        html_data = BeautifulSoup(open(link,"r").read(),"html.parser")

        #去除注释
        #comments = html_data(text=lambda text: isinstance(text, Comment))
        #[comment.extract() for comment in comments]

        obj = html_data.find('h1',{'class':'title'})
        if obj:
            _title = obj.text
        else:
            obj = html_data.find("title")
            if obj:
                _title = obj.text
            else:
                obj = html_data.find_all('h1')
                _title = obj[0].text if obj else link

        obj = html_data.find('div',{'id':'content'})
        if obj:
            content_data = obj
            content_data_text = str(content_data)
        else:
            content_data = html_data.find('body')
            # content_data_text = str(content_data).replace("<body>","").replace("</body>","")
            content_data_text = str(content_data).replace("<body>","<div id='content'>").replace("</body>","</div>")

        obj = html_data.find(attrs={"name":"keywords"})
        if obj and obj.has_attr('content'):   # 'content' in obj:
            keywordtext = obj.attrs['content']   # obj['content']
        else:
            keywordtext = ""

        reading_mode_obj = html_data.find(attrs={"name":"reading-mode"})
        if reading_mode_obj and reading_mode_obj.has_attr('content'):
            reading_mode_status = True
        else:
            reading_mode_status = False

        reading_mode_processed = False
        if reading_mode_status:
            content_data_text = content_data_text.replace("id=\"content\"","id=\"content-reading\"")
            content_data_text = content_data_text.replace("id=\'content\'","id=\'content-reading\'")
            reading_mode_processed = True
            
        for rdmode_key in self.rdmode_keyword_list:
            if reading_mode_processed:
                break
            
            if rdmode_key in keywordtext:
                content_data_text = content_data_text.replace("id=\"content\"","id=\"content-reading\"")
                content_data_text = content_data_text.replace("id=\'content\'","id=\'content-reading\'")
                reading_mode_processed = True
                break
                        
        # replace images path
        public_file = "file:///%s/" % self.public
        public_path = "%s" %(self.public_url)
        if public_file in content_data_text:
            content_data_text = content_data_text.replace(public_file, public_path)
        
        image_file = "file:///%s/" % self.images_dir
        image_path = "%s%s/" %(self.public_url,self.images_dir)
        if image_file in content_data_text:
            content_data_text = content_data_text.replace(image_file, image_path)

        # replace files path
        data_file = "file:///%s/" % self.files_dir
        data_path =  "%s%s/" %(self.public_url,self.files_dir)
        if data_file in content_data_text:
            content_data_text = content_data_text.replace(data_file, data_path)

        if content_data:
            try:
                src_data = content_data.find_all('div',{'class':'org-src-container'})
            except:
                src_data = ""
        else:
            src_data = ""
            
        for src_tag in src_data:
            # src-python
            src_lang = src_tag.find('pre').attrs['class'][-1].split('-')[-1]
            src_code = src_tag.text
            new_src = get_hightlight_src(src_code,src_lang)
            content_data_text = content_data_text.replace(str(src_tag),new_src)


        # cjk nums
        import re
        hanzi_regex = re.compile(r'[\u4E00-\u9FA5]')
        hanzi_list = hanzi_regex.findall(content_data_text)
        self.cjk_num = len(hanzi_list)

        content_data_text += self.copyright(num)

            
        if public:
            new_archive = [self.gen_public_link(self.notes[num][0],self.public_url),"fa fa-file-o",self.notes[num][1].strip()] if self.notes else []
            if not new_archive in self.archives:
                self.archives.append(new_archive)
            
            if num == 0:
                prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>'
            else:
                prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>' % self.gen_prev(num)
                
            if num == (len(self.notes) - 1):
                next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>下一页</a></li>' 
            else:
                next_page = '<li class="next"><a href="%s" class="alignright next">下一页<i class="fa fa-arrow-circle-o-right"></i></a></li>' % self.gen_next(num)

            page_order = """
            <div>
            <center>
            <div class="pagination">
            <ul class="pagination">
            %s
            <li><a href="%sarchive.html" target="_blank"><i class="fa fa-archive"></i>归档</a></li>
            %s
            </ul>
            </div>
            </center>
            </div>
            """ % (prev_page,self.public_url,next_page)
        else:
            page_order = ""


        without_title_data = content_data_text.replace('<h1 class="title">%s</h1>' % (_title),"")
        new_data = without_title_data + page_order + self.donate() + self.duosuo() + self.utteranc()
        output += new_data
        output += "</div> <!-- my-page -->"
        output += "</div> <!-- col-md -->"

                
        return output
    
    def contain_note(self,link=""):
        import re
        
        output = ""

        return output

        html_data = BeautifulSoup(open(link,"r").read(),"html.parser")

        # _title = html_data.find('h1',{'class':'title'}).text
        obj = html_data.find('h1',{'class':'title'})
        if obj:
            _title = obj.text
        else:
            obj = html_data.find("title")
            if obj:
                _title = obj.text
            else:
                obj = html_data.find_all('h1')
                _title = obj[0].text if obj else link

        content_data = html_data.find('div',{'id':'content'})

        if 'table-of-contents' in str(content_data):
            content_data_text = str(html_data.find('div',{'id':'table-of-contents'}))
        else:
            content_data_text = str(content_data)

        content_data_text = content_data_text.replace('<h1 class="title">%s</h1>' % (_title),"")

        src_data = content_data.find_all('div',{'class':'org-src-container'})
        for src_tag in src_data:
            # src-python
            src_lang = src_tag.find('pre').attrs['class'][-1].split('-')[-1]
            src_code = src_tag.text
            new_src = get_hightlight_src(src_code,src_lang)
            content_data_text = content_data_text.replace(str(src_tag),new_src)

        READ_MORE = ""
        
        if 'table-of-contents' in content_data_text:
            new_data = content_data_text
        else:
            new_data = content_data_text.split('</p>')
            p_num = len(new_data)

            if p_num > 5:
                new_data = '</p>'.join(new_data[:5])
                new_data += '''
                </p>
                </div>
                '''
            
                #if 'table-of-contents' in new_data:
                #    new_data += '''
                #    </div>
                #    </div>
                #    '''
            else:
                new_data = '</p>'.join(new_data)


        #delete id="content"
        new_data = new_data.replace("content","content-index")
        #new_data = new_data.replace(self.col_md_page,"col-md-12")

        READ_MORE += new_data


        READ_MORE +=  """
        <footer>
        <div class="alignleft">
        <a href="%s#more" class="more-link">阅读全文</a>
        </div>
        <div class="clearfix"></div>
        </footer>
        """ % self.gen_public_link(link,self.public_url)
        
        #output += "</div> <!-- contain -->"
        #output += "</div> <!-- col-md-12 -->"

        if self.rss_type != "ReadNone":
            output += READ_MORE
            
        return output


    def contain_archive_links(self,data={}):
        output = ""
        output += """
        <!-- display as entry -->
        <div class="entry">
        <div class="row">
        <div class="%s">
        """ % self.col_md_index

        output += "<ul>"
        for archives in data[self.links_title_key]:
            output += "<h3>%s</h3>" % archives            
            for archive in data[archives]:
                if len(archive) == 2:
                    link_list = archive[0].split('/')[2:]
                    if len(link_list) >= 4:
                        link_list = link_list[-4:]
                    newarchive = [self.public_url + '/'.join(link_list),'fa fa-file-o',archive[1]]
                    output += self.gen_href(newarchive)
                else:
                    output += self.gen_href(archive)

        output += "</ul>"

        output += """
        </div>
        </div>
        </div>
        """

        output += """
        </div> <!-- mypage -->
        </div> <!-- %s -->
        """ % self.col_md_index

        return output

    def contain_archive(self,data=list()):
        
        output = ""
        output += """
        <!-- display as entry -->
        <div class="entry">
        <div class="row">
        <div class="%s">
        """ % self.col_md_index
        
        for archive in data:
            if len(archive) == 2:
                link_list = archive[0].split('/')[2:]
                if len(link_list) >= 4:
                    link_list = link_list[-4:]
                newarchive = [self.public_url + '/'.join(link_list),'fa fa-file-o',archive[1]]
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
        </div> <!-- %s -->
        """ % self.col_md_index
        
        return output

    def contain_archive_tag(self):
        output = ""
        
        """
        <!-- display as entry -->
        <div class="entry"> 
        <div class="row">
        <div class="%s">
        """ % self.col_md_index

        output += "<ul>"

        from functools import cmp_to_key
        key = cmp_to_key(lambda x,y: len(self.tags[x]) - len(self.tags[y]))
        for key in sorted(self.keywords,key=key,reverse=True):
            
            if key in self.ignore_tags_list:
                continue
            
            output += "<a href=\"javascript:showul('%s');\"><h3>%s(%d)</h3></a>" % (key,key,len(self.tags[key]))
            output += "<ul id='%s' style='display:none'>" %  key
            for link in self.tags[key]:
                newarchive = [self.gen_public_link(link[0],self.public_url),'fa fa-file-o',link[1]]
                output += self.gen_href(newarchive)
            output += "</ul>"

        output += "</ul>"

        """
        </div>
        </div>
        </div>
        """        

        output += """
        </div> <!-- mypage -->
        </div> <!-- %s -->
        """ % self.col_md_index

        return output
    
    def contain_about(self):
        """about me page"""

        output = ""

        output += """
        <!-- display as entry -->
        <div class="entry">
        <div class="row">
        <div class="%s">
        """ % self.col_md_index
        
        if self.description:
            output += "<p>%s</p>" % self.description
        else:
            output += """
            <p>这是一个建立在<code><a class="i i1 fc01 h" hidefocus="true" href="https://www.github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a></code>上的博客.</p>
            """

        output += """
        </div>
        </div>
        </div>             
        """ 

        output += self.duosuo()

        output += """
        </div> <!-- mypage -->
        </div> <!-- %s -->
        """ % self.col_md_index
        
        return output

    def contain_calendar(self):
        output = ""

        if not self.calendar_name or not self.calendar_jobfile: return output
        if not os.path.exists(self.calendar_jobfile):
            print("Can not found jobfile: ",self.calendar_jobfile)
            return output

        by_types = {'by_once':'一次性事情',
                    'by_day':'每天一次',
                    'by_week':'每周一次',
                    'by_month':'每月一次',
                    'by_quarter':'每季一次',
                    'by_year':'每年一次'}

        for job in open(self.calendar_jobfile, "r").readlines():
            job = job.strip()
            if not job: continue
            if job.startswith("#"): continue
            
            job = [i.strip() for i in job.strip().split(',')]
            #print(job)

            if len(job) < 3:
                print("Bad format calendar job(time,name,job type,url):", job)
                continue

            jtype,jtime = job[:2]
            hasurl = False
            for p in ["http://","https://","www."]:
                if job[-1].startswith(p):
                    hasurl = True
                    continue

            if hasurl:
                jurl = job[-1]
                jname = ','.join(job[2:-1]) if len(job) > 3 else jurl
            else:
                jurl = ""
                jname = ','.join(job[2:])

            if jtype not in by_types:
                print("Bad job type in", job)
                print("job type must be on of ", by_types.keys())
                continue

            try:
                jtime = datetime.datetime.strptime(jtime, "%Y/%m/%d %H:%M")
            except ValueError as e:
                print("Bad job format:", job)
                print(str(e))
                continue

            quarter_list = [j for j in [i + jtime.month for i in range(-9, 10, 3)] if j >= 1 and j <= 12]

            today = datetime.datetime.now() + datetime.timedelta(hours=self.shift_hour)


            monthrange = calendar.monthrange(today.year,today.month)

            if monthrange[1] < jtime.day:
                jtime.replace(day=monthrange[1])

            # get current time to generate calendar jobs
            today = today.replace(hour=jtime.hour, minute=jtime.minute)
            
            is_today_job = False
            is_week_job = False
            is_prev_job = False
            is_done_job = False

            if jtype == "by_day" or (today.year, today.month, today.day) == (jtime.year, jtime.month, jtime.day):
                is_today_job = True
            elif jtype == "by_once":
                delta = jtime - today
                if delta.days in range(0, 8):
                    is_week_job = True
                elif delta.days in range(-8, 0):
                    is_prev_job = True
                elif delta.days < -8:
                    is_done_job = True
                else:
                    pass
            elif jtype == "by_week":
                if jtime.weekday() == today.weekday():
                    is_today_job = True
                else:
                    is_week_job = True
                    is_prev_job = True
            elif jtype == "by_month":
                jtime = jtime.replace(year=today.year,month=today.month)
                if today.day == jtime.day:
                    is_today_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day > jtime.day:
                    is_prev_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day < jtime.day:
                    is_week_job = True
                else:
                    pass
            elif jtype == "by_quarter":
                if today.month not in quarter_list: continue
                jtime = jtime.replace(year=today.year,month=today.month)
                if today.day == jtime.day:
                    is_today_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day > jtime.day:
                    is_prev_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day < jtime.day:
                    is_week_job = True
                else:
                    pass
            elif jtype == "by_year":
                if today.year < jtime.year: continue
                if today.month != jtime.month: continue
                jtime = jtime.replace(year=today.year,month=today.month)
                if today.day == jtime.day:
                    is_today_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day > jtime.day:
                    is_prev_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day < jtime.day:
                    is_week_job = True
                else:
                    pass
            else:
                continue



            weekday = jtime.weekday() + 1 # 0 + 1: Mon
            t_weekday = today.weekday() + 1

            if is_today_job:
                today_str = today.strftime("%Y/%m/%d %H:%M")
                self.job_today.append([today_str, jname, jtype, jurl])
            elif is_week_job:
                if t_weekday >= weekday:
                    days = (7 - t_weekday) + weekday
                else:
                    days = weekday - t_weekday
                today = today + datetime.timedelta(days=days)
                today_str = today.strftime("%Y/%m/%d %H:%M")
                self.job_week.append([today_str, jname, jtype, jurl])
            elif is_prev_job:
                if t_weekday <= weekday:
                    days = (7 - weekday) + t_weekday
                else:
                    days = t_weekday -  weekday
                days *= -1
                today = today + datetime.timedelta(days=days)
                today_str = today.strftime("%Y/%m/%d %H:%M")
                self.job_prev.append([today_str, jname, jtype, jurl])
            elif is_done_job:
                day_str = jtime.strftime("%Y/%m/%d %H:%M")
                self.job_done.append([day_str,jname,jtype,jurl])
            else:
                pass

        #print(self.job_today)
        #print(self.job_week)

        for jobs in [self.job_today,self.job_week,self.job_prev,self.job_done]:
            if not jobs: continue
            if jobs == self.job_today:
                output += "<h3>今日行程</h3>"
                job_data = sorted(jobs)
            elif jobs == self.job_week:
                output += "<h3>下周行程</h3>"
                job_data = sorted(jobs)
            elif jobs == self.job_prev:
                output += "<h3>上周行程</h3>"
                job_data = sorted(jobs,reverse=True)
            else:
                output += "<h3>完成行程</h3>"
                job_data = sorted(jobs,reverse=True)

            output += "<ul>"
            for job in job_data:
                if not job[3]:
                    output += "<li><strong>时间</strong>: %s , <strong>(%s)</strong>: %s </li>" % (job[0], by_types[job[2]],job[1])
                else:
                    output += "<li><strong>时间</strong>: %s , <strong>(%s)</strong>: <a href='%s'>%s</a> </li>" % (job[0], by_types[job[2]],job[3],job[1])
            output += "</ul>"

        output += """
        </div> <!-- mypage -->
        </div> <!-- %s -->
        """ % self.col_md_index

        return output

    def donate(self):
        if not self.donate_name or (not self.donate_wechatpay and not self.donate_alipay and not self.weixin_public):
            return ""

        output = ""
        
        if self.donate_name:
            
            output += """
            <div class="post-reward">
            <input type="checkbox" name="reward" id="reward" hidden />
            <label id="reward-button" class="reward-button" for="reward">%s</label>
            <div class="qr-code">
            """ % self.donate_name

            if self.donate_wechatpay:
                output += """
                <label id="qr-code-image-w" class="qr-code-image" for="reward" hidden>
                <img class="image" src="%s/%s">
                <span>微信打赏</span>
                </label>
                """ % (self.public_url,self.donate_wechatpay)

            if self.donate_alipay:
                output += """
                <label id="qr-code-image-a" class="qr-code-image" for="reward" hidden>
                <img class="image" src="%s/%s">
                <span>支付宝打赏</span>
                </label>
                """ % (self.public_url,self.donate_alipay)

            if self.weixin_public:
                output += """
                <label id="qr-code-image-p" class="qr-code-image" for="reward" hidden>
                <img class="image" src="%s/%s">
                <span>微信公众号</span>
                </label>
                """ % (self.public_url,self.weixin_public)

                
            output += """
            </div>
            </div>
            """
            
        return output
            
    def utteranc(self):
        if not self.utteranc_repo:
            return ""
        else:
            return """
            <script src="https://utteranc.es/client.js"
            repo="%s"
            issue-term="title"
            theme="github-light"
            crossorigin="anonymous"
            async>
            </script>
            """ % self.utteranc_repo

    def duosuo(self):
        if not self.duoshuo_shortname:
            return """
            """
        else:
            return """
            <!-- Duoshuo Comment BEGIN -->
            <div class="ds-thread"></div>
            <script type="text/javascript">
            var duoshuoQuery = {short_name:"%s"};
            (function() {
            var ds = document.createElement('script');
            ds.type = 'text/javascript';ds.async = true;
            ds.src = 'http://static.duoshuo.com/embed.js';
            ds.charset = 'UTF-8';
            (document.getElementsByTagName('head')[0]
            || document.getElementsByTagName('body')[0]).appendChild(ds);
            })();
            </script>
            <!-- Duoshuo Comment END -->
            """ % self.duoshuo_shortname
        
    def contain_sidebar(self):
        return """
        <div class="%s">
        <div id="sidebar">
        """ % (self.col_md_index_r if self.col_md_index_r else self.col_md_page_r)
    
    def sidebar_contact(self):
        return """
        <div class="widget">
        <h4>%s</h4>
        <ul class="entry list-unstyled">
        <li>%s</li>
        </ul>
        </div>
        """ % (self._sidebar_contact_name,self._sidebar_contact)

    def sidebar_weixin(self):
        if not self.weixin_name and not self.weixin_public:
            return ""
        
        if not self.weixin_public:
            return """
            <div class="widget">
            <h4>%s</h4>
            <ul class="entry list-unstyled">
            <li>%s</li>
            </ul>
            </div>
            """ % ("微信公众号",self.weixin_name)
        else:        
            return """
            <div class="widget">
            <h4>%s</h4>
            <ul class="entry list-unstyled">
            <li><img class="image" src="%s/%s"></li>
            </ul>
            </div>
            """ % ("微信公众号",self.public_url,self.weixin_public)

    def sidebar_duoshuo(self):
        return """
        <div class="widget">
        <h4>最新评论</h4>
        <ul class="entry list-unstyled">

        <!-- 多说最新评论 start -->
        <div class="ds-recent-comments" data-num-items="5" data-show-avatars="1" data-show-time="1" data-show-title="1" data-show-admin="1" data-excerpt-length="170"></div>
        <!-- 多说最新评论 end -->
        <!-- 多说公共JS代码 start (一个网页只需插入一次) -->
        <script type="text/javascript">
        var duoshuoQuery = {short_name:"%s"};
        (function() {
        var ds = document.createElement('script');
        ds.type = 'text/javascript';ds.async = true;
        ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
        ds.charset = 'UTF-8';
        (document.getElementsByTagName('head')[0]
        || document.getElementsByTagName('body')[0]).appendChild(ds);
        })();
        </script>
        <!-- 多说公共JS代码 end -->
        </ul>
        </div>
        """ % self.duoshuo_shortname

    
    def sidebar_tags(self):
    
        output = ""
        
        output += """
        <div class="widget">
        <h4>标签云</h4>
        <ul class="tag_box inline list-unstyled">
        """

        from functools import cmp_to_key
        key = cmp_to_key(lambda x,y: len(self.tags[x]) - len(self.tags[y]))
        for key in sorted(self.keywords,key=key,reverse=True):
            
            if key in self.ignore_tags_list:
                continue
            
            output += "<li><a href=\"%stags/%s.html\">%s<span>%s</span></a></li>" % (self.public_url,key,key,len(self.tags[key]))

        output += """
        </ul>
        </div>
        """

        return output

    def contain_tags(self):
        output = ""
        output += """
        <div class="tag-cloud-tags" style="padding: 5px 15px">
        """
        from functools import cmp_to_key
        key = cmp_to_key(lambda x,y: len(self.tags[x]) - len(self.tags[y]))
        for key in sorted(self.keywords,key=key,reverse=True):
            
            if key in self.ignore_tags_list:
                continue
            
            nums = len(self.tags[key])
            size = nums/5.0
            if size < 1:
                size = 1
            elif size > 4:
                size = 4
            else:
                pass
            output += "<a href=\"%stags/%s.html\" style=\"font-size:%srem\">%s</a>" % (self.public_url,key,size,key)            

        output += """
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
            output += "<li><a href=\"%stags/%s.html\">%s<span>%s</span></a></li>" % (self.public_url,key,key,len(self.timetags[key]))
            tot += len(self.timetags[key])
        output += "<li><a href=\"%sarchive.html\">All<span>%s</span></a></li>" % (self.public_url,tot)
        
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
            output += "<li><a href=\"%s\"><i class=\"fa fa-file-o\"></i>%s</a></li>" % (self.gen_public_link(note[0].replace('"',""),self.public_url),note[1])
            
        output += """
        </ul>   
        </div> 
        """
        
        return output

    def sidebar_weibo(self):
        return """
        """

    def sidebar_link(self):
        output = """
        <div class="widget">
        <h4>%s</h4>
        <ul class="entry list-unstyled">
        """ % self.slinks_name

        if os.path.exists(self.slinks_file):
            for link in open(self.slinks_file,"r").readlines():
                link = link.strip()
                if not link: continue
                if link.startswith("#"): continue
                link = [i.strip() for i in link.split(',')]

                if len(link) >= 3:
                    url,name,icon = link[:3]
                elif len(link) == 2:
                    icon = "fa fa-link"
                else:
                    url = name = link[0]
                    icon = "fa fa-link"

                item = (url,name,icon)
                if item not in self.slinks:
                    self.slinks.append(item)
                    
        for link in self.slinks:
            url,name,icon = link
            output += """
            <li><a href="%s" title="%s" target="_blank"><i class="%s"></i>%s</a></li>
            """ % (url, name, icon,name)
        
        output += """
        </ul>
        </div>
        """

        return output

    def end_sidebar(self):
        return """
        </div> <!-- sidebar -->
        </div> <!-- %s -->
        """ % self.col_md_index_r
        
    def contain_suffix(self):
        return """
        </div> <!-- row-fluid -->
        </div>
        </div>
        """

    def header_suffix(self):
        return """
        <div class="container-narrow">
        <footer>
        <p>&copy; 2014-%d %s
        with help from <a href="https://github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a>. Theme by <a href="https://github.com/LeslieZhu/orgnote-theme-freemind">orgnote-theme-freemind</a>.  Published with GitHub Pages. 
        </p> </footer>
        </div> <!-- container-narrow -->
        
        <a id="gotop" href="#">   
        <span>▲</span> 
        </a>
        
        %s

        </body>
        </html>
        """ % (time.localtime().tm_year,self.author,self.gen_jscripts())

    def js_config(self):
        return """
        <script>
        var CONFIG = {
        root: '/',
        localsearch: {"enable":true,"trigger":"auto","top_n_per_article":1,"preload":true},
        path: '%s',
        };
        </script>
        """ % self.search_path

    def gen_jscripts(self):
        return """

        <script type="text/javascript">
        
        <!-- donate script -->
        var reward = document.getElementById('reward');
        if(reward){
            reward.onclick = function() {
              $('#reward-button').addClass('hidden');
              $('#qr-code-image-w').show();
              $('#qr-code-image-a').show();
              $('#qr-code-image-p').show();
            }
        }
        <!-- /donate script -->

        
        function showul(name){
            var uls = document.getElementById(name);
            if(uls.style.display == "none"){
               uls.style.display = "block";
            } else {
               uls.style.display = "none";
            } 
        }
        </script>
        """

    def gen_public_link(self,link="",prefix=None):
        if prefix == None:
            prefix = "" #self.public_url

        link_list = link.split('/')[2:]
        if len(link_list) >= 4:
            link_list = link_list[-4:]
            
        return prefix+'/'.join(link_list)
        # return prefix+'/'.join(link.split('/')[2:])
        #return re.sub("//*","/",'/'.join(link.split('/')[2:]))

    def gen_sidebar(self):
        """
        if the sidebar enable, then display each sidebar by order
        """

        if self.sidebar_show == 1:
            output = self.contain_sidebar()
            if self._sidebar_contact:
                output += self.sidebar_contact()
            for _sidebar in self.sidebar_list:
                if _sidebar == "sidebar_latest":
                    output += self.sidebar_latest(self.notes)
                elif _sidebar == 'sidebar_tags':
                    output += self.sidebar_tags()
                elif _sidebar == 'sidebar_time':
                    output += self.sidebar_date()
                elif _sidebar == 'sidebar_link':
                    output += self.sidebar_link()
                elif _sidebar == 'sidebar_weibo' and self.weibo_shortname:
                    output += self.sidebar_weibo()
                elif self.duoshuo_shortname and _sidebar == 'sidebar_duoshuo' and self._sidebar_contact:
                    output += self.sidebar_duoshuo()
                elif self.weixin_name or self.weixin_public:
                    output += self.sidebar_weixin()
                else:
                    pass
            output += self.end_sidebar()
        else:
            output = ""
            
        return output

    def gen_sidebar_page(self):
        output = ""
        
        #if self.utteranc_repo:
        #    output += self.utteranc()
            
        if self.sidebar_show_page == 0:
            #if self._sidebar_contact:
            #    output = self.sidebar_contact()
            #else:
            #    output = ""
            output += "" # do not want this now
        else:
            output += self.contain_sidebar()
            if self._sidebar_contact:
                output += self.sidebar_contact()
            for _sidebar in self.sidebar_list:
                if _sidebar == "sidebar_latest":
                    output += self.sidebar_latest(self.notes)
                elif _sidebar == 'sidebar_tags':
                    output += self.sidebar_tags()
                elif _sidebar == 'sidebar_time':
                    output += self.sidebar_date()
                elif _sidebar == 'sidebar_link':
                    output += self.sidebar_link()
                elif _sidebar == 'sidebar_weibo' and self.weibo_shortname:
                    output += self.sidebar_weibo()
                elif self.duoshuo_shortname and _sidebar == 'sidebar_duoshuo' and self._sidebar_contact:
                    output += self.sidebar_duoshuo()
                elif self.weixin_name or self.weixin_public:
                    output += self.sidebar_weixin()
                else:
                    pass
            output += self.end_sidebar()

        return output

    def gen_archive(self):
        output = open('./' + self.public_dir + "archive.html","w")
        print(self.header_prefix(title="归档"),file=output)
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix(["归档"],"","归档(%d)" % sum([len(self.tags[k]) for k in self.keywords])),file=output)
        print(self.contain_prefix_end(),file=output)
        print(self.contain_archive_tag(),file=output)
        print(self.gen_sidebar(),file=output)
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)
            
        output.close()

    def gen_rss(self):
        output = open('./' + self.public_dir + "rss.xml","w")
        print(self.gen_rss_xml(),file=output)
        output.close()

    def gen_search(self):
        output = open('./' + self.public_dir + self.search_path,"w")
        print(self.gen_search_json(),file=output)
        output.close()

    def gen_search_json(self):
        searchdb = []
        
        for note in self.notes:
            link,name = note
            item = {}
            item['title'] = name
            item['url'] = self.gen_public_link(link,'/') #,self.public_url)
            item['content'] = self.gen_content(link)
            searchdb.append(item)

        return json.dumps(searchdb)

    def gen_search_xml(self):
        output = ""

        #entry
        output += """<?xml version="1.0" encoding="UTF-8" ?>
        <item>
        """

        # item
        for note in self.notes:
            link,name = note
            output += '''
            <entry>
            <title> %s </title>
            <url> %s </link>
            <description>%s </description>
            </entry>
            ''' % (name,
                   self.gen_public_link(link,self.public_url),
                   self.gen_content(link))

        output += """
        </item>
        </xml>
        """

        return output

    def gen_rss_xml(self):
        output = ""

        # prefix
        output += """<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0">
        <channel>

        <title>%s</title>

        <link>%s</link>

        <description>
           <![CDATA[%s]]>
        </description>

        <language>zh-CN</language>
        <generator>OrgNote: A simple org-mode blog, write blog by org-mode in Emacs</generator>
        <webMaster><![CDATA[%s]]></webMaster>
        <ttl>120</ttl>
        
        <image>
        <title><![CDATA[%s]]></title>
        <url>%s/favicon.ico</url>
        <link>%s</link>
        </image>        
        """ % (self.title,self.homepage,self.subtitle,
               self.author,self.title,self.homepage,self.homepage)

        # item
        for note in self.notes:
            link,name = note

            output += '''
            <item>
            <title> %s </title>
            <link> %s </link>
            <author><![CDATA[%s]]></author>
            <guid isPermaLink="true">%s</guid>
            ''' % (name.replace("&","&amp;"),self.gen_public_link(link,self.public_url),
                   self.author,self.gen_public_link(link,self.public_url))

            for tag in self.gen_category(link):
                
                if tag in self.ignore_tags_list:
                    continue
                
                output += '''<category><![CDATA[%s]]></category>''' % tag
                

            output += '''
            <pubDate>%s</pubDate>
            <description><![CDATA[%s]]></description>
            <comments>%s</comments>
            </item>
            ''' % (self.gen_date(link),
                   (self.gen_content(link) if self.rss_type == "ReadAll" else self.contain_note(link)),
                   self.gen_public_link(link,self.public_url))

        # suffix
        output += '''
        </channel>
        </rss>
        '''

        return output

    def gen_content(self,link):
        html_data = BeautifulSoup(open(link,"r").read(),"html.parser")
        content_data = html_data.find('div',{'id':'content'})
        return str(content_data)

    def gen_tags_menu_page(self):
        output = open('./' + self.public_dir + "tags.html","w")
        print(self.header_prefix(title="标签"),file=output)
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix(["标签"],"","标签",True),file=output)
        print(self.contain_prefix_end(),file=output)
        print(self.contain_tags(),file=output)
        #print(self.gen_sidebar(),file=output)
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)

        output.close()
        
    def gen_page(self,note=list(),num=0,public=True):
        import os
        import os.path

        page_file = './' + self.gen_public_link(note[0],self.public_dir)
        page_dir = os.path.dirname(page_file)
        
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)

        output = open(page_file,"w")
        output_html = ""

        header = self.header_prefix(2,note[1].strip())
        style = self.get_style(note[0])
        header = header.replace("<ORGNOTESTYLE>", style)
        header = header.replace("<ORGNOTESTYLE>", "")

        output_html += header
        output_html += self.body_prefix()
        output_html += self.body_menu(self.menus)

        if public:
            tags = self.page_tags[note[0]]
            if self.ignore_tags_list:
                tags = [i for i in tags if i not in self.ignore_tags_list]
                
            output_html += self.contain_prefix(tags,"标签: ",util.gen_title(note[0]))
        else:
            output_html += self.contain_prefix([self.nopublic_tag],"标签: ",util.gen_title(note[0]))

        output_html += self.contain_prefix_end(note[0])
        output_html += self.contain_page(note[0],num,public)
        output_html += self.gen_sidebar_page()
        output_html += self.contain_suffix()
        output_html += self.header_suffix()

        for item in self.replace_str_list:
            if not isinstance(item, list):
                item = [i.strip() for i in item.split("=>")]
            if not item or not len(item) != 2: continue
            output_html = output_html.replace(item[0],item[1])

        print(output_html, file=output)
        output.close()


        
    def gen_public(self):
        for i,note in enumerate(self.notes):
            self.gen_page(note,i,True)
        for i,note in enumerate(self.localnotes):
            self.gen_page(note,i,False)

    def split_index(self,num,b_index,e_index):
        """
        split index.html as page1,page2,page3...,so do not need display all notes in homepage
        """
        if num == 0:
            output = open('./' + self.public_dir + "index.html","w")
        else:
            output = open('./' + self.public_dir + "page"+str(num)+".html","w")

        print(self.header_prefix(title=self.title),file=output)
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix(),file=output)
        print(self.contain_prefix_end(),file=output)
        print(self.contain_notes(self.notes[b_index:e_index],num,e_index),file=output)              # auto gen
        print(self.gen_sidebar(),file=output)
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)
            
        output.close()

    def gen_index(self,note_num=None):
        """
        each split page hold `num` notes
        """

        if note_num == None: 
            note_num = self.per_page

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
        about_file = "%sabout.html" % self.source_dir
        
        output = open(self.public_dir + "about.html","w")
        print(self.header_prefix(title="说明"),file=output)        
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix(["说明"],"","说明"),file=output)
        print(self.contain_prefix_end(),file=output)
        
        if os.path.exists(about_file):
            print(self.contain_page(about_file,0,True),file=output)
        else:
            print(self.contain_about(),file=output)
            
        print(self.gen_sidebar(),file=output)
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)
        
        output.close()

    def gen_links(self):
        output = open("./" + self.public_dir + "links.html","w")
        print(self.header_prefix(title=self.links_name),file=output)
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix([self.links_name],"",self.links_name),file=output)
        print(self.contain_prefix_end(),file=output)
        print(self.contain_archive_links(self.links),file=output)
        print(self.gen_sidebar(),file=output)
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)
            
        output.close()

    def gen_tags(self):
        for key in self.keywords:
            if key in self.ignore_tags_list:
                continue
            
            output = open("./" + self.public_dir + "tags/" + key + ".html","w")
            print(self.header_prefix(title=key),file=output)
            print(self.body_prefix(),file=output)
            print(self.body_menu(self.menus),file=output)
            print(self.contain_prefix([key],"分类: ",key),file=output)
            print(self.contain_prefix_end(),file=output)
            #print(self.contain_notes(__tags__[key]),file=output)
            print(self.contain_archive(self.tags[key]),file=output)              # auto gen
            print(self.gen_sidebar(),file=output)
            print(self.contain_suffix(),file=output)
            print(self.header_suffix(),file=output)
            output.close()
            
    def gen_timetags(self):
        for key in sorted(self.timetags.keys(),reverse=True):
            output = open("./" + self.public_dir + "tags/" + key + ".html","w")
            print(self.header_prefix(title=key),file=output)
            print(self.body_prefix(),file=output)
            print(self.body_menu(self.menus),file=output)
            print(self.contain_prefix([key],"月份: ",key),file=output)
            print(self.contain_prefix_end(),file=output)
            print(self.contain_archive(self.timetags[key]),file=output)
            print(self.gen_sidebar(),file=output)
            print(self.contain_suffix(),file=output)
            print(self.header_suffix(),file=output)
            output.close()

    def gen_nopublic(self):
        output = open("./" + self.public_dir + "tags/" + self.nopublic_tag + ".html","w")
        print(self.header_prefix(title=self.nopublic_tag),file=output)
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix([self.nopublic_tag],"分类: ",self.nopublic_tag),file=output)
        print(self.contain_prefix_end(),file=output)
        print(self.contain_archive(self.localnotes),file=output)              # auto gen
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)
        output.close()
        
    def gen_calendar(self):
        output = open(self.public_dir + "calendar.html","w")
        print(self.header_prefix(title=self.calendar_name),file=output)
        print(self.body_prefix(),file=output)
        print(self.body_menu(self.menus),file=output)
        print(self.contain_prefix([self.calendar_name],"",self.calendar_name),file=output)
        print(self.contain_prefix_end(),file=output)
        print(self.contain_calendar(),file=output)
        print(self.gen_sidebar(),file=output)
        print(self.contain_suffix(),file=output)
        print(self.header_suffix(),file=output)
        output.close()
        
    
    def gen_date(self,link=""):
        """ Filter Publish data from HTML metadata>"""
        
        html_data = BeautifulSoup(open(link,"r").read(),"html.parser")

        date_tag = html_data.find('p',{'class':'date'})
        pubdate = time.strftime("%m/%d/%Y")
        
        if date_tag:
            try:
                pubdate = date_tag.contents[0].split(':')[-1].strip()
            except:
                pubdate = time.strftime("%m/%d/%Y")    
        else:
            try:
                pubdate = html_data.find('meta',{'name':'generated'}).attrs['content']
            except:
                pubdate = time.strftime("%m/%d/%Y")
                
        if "/" in pubdate:
            try:
                pubdate=time.strptime(pubdate, "%m/%d/%Y")
            except ValueError:
                pubdate=time.strptime(pubdate, "%Y/%m/%d")
            except Exception as e:
                print(e)
                sys.exit(-1)
                
        elif "-" in pubdate:
            try:
                pubdate=time.strptime(pubdate, "%Y-%m-%d")
            except ValueError:
                pubdate=time.strptime(pubdate, "%m-%d-%Y")
            except Exception as e:
                print(e)
                sys.exit(-1)
        else:
            print(link,pubdate)
            pubdate=time.strptime(pubdate, "%Y%m%d")

        pubdate=time.strftime("%Y-%m-%d %a",pubdate)
        return pubdate

    def gen_category(self,link=""):
        """ Filter Keywords from HTML metadata """

        html_data = BeautifulSoup(open(link,"r").read(),"html.parser")
        keywords_list = html_data.findAll('meta',{'name':'keywords'})

        if keywords_list and 'content' in keywords_list[0].attrs.keys():
            keywords = keywords_list[0].attrs['content']
            return [i.strip() for i in keywords.split(",") if i not in self.ignore_tags_list]
        else:
            return [i.strip() for i in self.default_tag_list]

    def monitor_log(self,s=""):
        print("[Monitor] %s" % s)

    def monitor_kill(self):
        if self.process and self.process.is_alive():
            self.monitor_log('Kill process [%s]...' % self.process.pid)
            self.process.terminate()
            self.monitor_log('Process ended with code %s.' % self.process.exitcode)
            self.process = None

    def monitor_restart(self,port="8080",filename=""):
        #self.monitor_kill()
        #self.process = Process(target=self.monitor_start, args=(self.port,))
        #self.process.daemon = True
        #self.process.start()
        #self.process.join()

        print("Watch: re-generate pages")
        self.homepage ="http://localhost:" + port
        self.do_generate(self.homepage)


    def do_server(self,port="8080"):
        self.port = port

        self.monitor_path = self.source_dir
        
        observer = Observer()
        observer.schedule(OrgNoteFileSystemEventHander(OrgNote(),self.monitor_restart,self.port), self.monitor_path, recursive=True)
        observer.start()
        
        self.monitor_log('Watching directory %s' % self.monitor_path)

        self.process = Process(target=self.monitor_start, args=(self.port,))
        self.process.daemon = True
        self.process.start()
        self.process.join()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    def monitor_start(self,port):
        import sys

        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)
            
        self.port = port
        self.homepage ="http://localhost:" + self.port
        self.do_generate(self.homepage)                

        try:
            server_address = ('', int(self.port))
            if sys.version_info.major == 2:
                import SimpleHTTPServer,BaseHTTPServer
                server_class = BaseHTTPServer.HTTPServer
                handler_class = SimpleHTTPServer.SimpleHTTPRequestHandler

                curdir = os.getcwd()
                os.chdir(self.public_dir)
                
                BaseHTTPServer.test(handler_class,server_class)
                
                os.chdir(curdir)
            elif sys.version_info.major == 3:
                import http.server
                if sys.version_info >= (3,7):
                    curdir = os.getcwd()
                    os.chdir(self.public_dir)
                    
                    server_class=http.server.ThreadingHTTPServer
                    handler_class=partial(http.server.SimpleHTTPRequestHandler,directory=os.getcwd())
                    handler_class.protocol_version = "HTTP/1.0"
                    
                    with server_class(server_address, handler_class) as httpd:
                        sa = httpd.socket.getsockname()
                        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
                        print(serve_message.format(host=sa[0], port=sa[1]))
                        try:
                            httpd.serve_forever()
                        except KeyboardInterrupt:
                            print("\nKeyboard interrupt received, exiting.")
                            os.chdir(curdir)
                            sys.exit(0)                            
                else:
                    server_class=http.server.HTTPServer
                    handler_class=http.server.SimpleHTTPRequestHandler                    
                    handler_class.protocol_version = "HTTP/1.0"

                    curdir = os.getcwd()
                    os.chdir(self.public_dir)
                    
                    httpd = server_class(server_address, handler_class)
                    
                    sa = httpd.socket.getsockname()
                    print("Serving HTTP on", sa[0], "port", sa[1], "...")
                    try:
                        httpd.serve_forever()
                    except KeyboardInterrupt:
                        print("\nKeyboard interrupt received, exiting.")
                        httpd.server_close()
                        os.chdir(curdir)
                        sys.exit(0)                        
        except Exception as ex:
            print(str(ex))
            usage()

    def public_syncdirs(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)

        for dir in self.sync_dirs:
            if os.path.exists("./"+dir):
                os.system("rsync --quiet -av ./%s ./%s/" % (dir,self.public_dir))
    
    def public_theme(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)
            
        if os.path.exists("./theme"):
            os.system("rsync --quiet -av ./theme ./%s/" % self.public_dir)

    def public_images(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)
            
        if os.path.exists("%s%s" % (self.source_dir,self.images_dir)):
            os.system("rsync --quiet -av %s%s ./%s/" % (self.source_dir,self.images_dir,self.public_dir))

        if os.path.exists("%s%s" % (self.source_dir,self.files_dir)):
            os.system("rsync --quiet -av %s%s ./%s/" % (self.source_dir,self.files_dir,self.public_dir))

    def public_cname(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)

        if os.path.exists("%sCNAME" % self.source_dir):
            os.system("rsync --quiet -av %sCNAME ./%s/" % (self.source_dir,self.public_dir))
        
    def public_favicon(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)

        if os.path.exists("%sfavicon.ico" % self.source_dir):
            os.system("rsync --quiet -av %sfavicon.ico ./%s/" % (self.source_dir,self.public_dir))
        
    def do_deploy(self,branch="master"):
        if not self.deploy_url or self.deploy_type != "git":
            print("Please add deploy repo git config info")
            return False
        
        import os
        import shutil
        
        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)        

        # cleanup cached html file
        os.system("rm -r %s/2*/" % self.public_dir)
        
        self.do_generate()
        
        curdir = os.getcwd()
        repodir = "./%s/.repo" % self.public_dir
        
        if not os.path.exists(repodir):
            os.makedirs(repodir)            
            os.chdir(repodir)
            os.system("git init && git remote add origin %s && git fetch && git pull origin %s" % (self.deploy_url,self.deploy_branch))
        else:
            os.chdir(repodir)
            os.system("git fetch && git pull origin %s" % (self.deploy_branch))
            #os.system("git rm -r . && git commit -m 'cleanup'")
            
        os.system("rsync -a --exclude='.repo/' ../ ./")
        os.system("git add . && git commit -m 'update' && git push origin %s" % self.deploy_branch)
        os.chdir(curdir)

    def do_generate(self,homepage="",batch=""):
        self.cfg.update()
        self.refresh_config(homepage)
        
        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)        
        self.public_images()
        self.public_theme()
        self.public_syncdirs()
        self.public_cname()
        self.public_favicon()
        self.gen_notes(self.dirs)

        # In emacs batch mode, use scripts/init-orgnote.el
        # can generate highlight code in html
        # this will force generate all raw-html again in
        # emacs batch mode, work as a backed feature.
        # 
        # all:  re-generate all notes's raw-html file
        # xxx.org:  re-generate the note's raw-html file
        # num:  re-generate last num notes's raw-html file
        # blank: ignore raw-html re-generate step
        # 
        if batch == "all":
            notes = [note[0].replace('.html','.org') for note in self.notes]
            for note in notes:
                self.do_page(note)
        elif batch.endswith('.org') or batch.endswith('.md'):
            self.do_page(batch)
        elif batch.isdigit():
            notes = [note[0].replace('.html','.org') for note in self.notes]
            for note in notes[:int(batch)]:
                self.do_page(note)
        else:
            pass

        self.gen_tag_list()
        self.gen_timetag_list()
        self.gen_public()
        self.gen_index()
        self.gen_about()
        self.gen_links()
        self.gen_archive()
        self.gen_tags()
        self.gen_tags_menu_page()
        self.gen_rss()
        self.gen_search()
        self.gen_timetags()
        # self.gen_nopublic()
        self.gen_calendar()
        print("notes generate done")

    def do_new(self,notename=""):
        if self.auto_publish:
            notefullname = util.add_note(notename,self.source_dir)
            if notefullname: self.do_publish(notefullname)                
        else:
            return util.add_note(notename,self.source_dir)

    def do_page(self,notename=""):
        print(">>>>>>do_page:",notename)
        if notename.endswith(".org") and not os.path.exist(notename):
            notename = notename.replace(".org",".md")
        elif notename.endswith(".md") and not os.path.exist(notename):
            notename = notename.replace(".md",".org")
        else:
            pass
        print("working on :",notename)
        if notename.endswith(".org"):
            return util.to_page(notename)
        elif notename.endswith(".md"):
            return util.to_page_mk2(notename)
        else:
            pass

    def do_recall(self,notename=""):
        import os.path
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]

        publish_line = util.publish_note(notename,self.source_dir)
        
        if not publish_line: return
        
        link = publish_line.replace(".org",".html").replace(".md",".html")

        if publish_line == None:
            print("\033[31m[ERROR]\033[0m: Can not cancel note: %s, are you sure it exists?" % notename)
            return

        print(publish_line)

        if not os.path.exists(publish_list):
            data = []
        else:
            data = open(publish_list,"r").readlines()
            data = [i.strip() for i in data if not i.startswith("#")]

        nopublish_data = open(nopublish_list,"r").readlines()
        nopublish_data = [i.strip() for i in nopublish_data if not i.startswith("#")]

        if publish_line in data:
            data.remove(publish_line)
            output = open(publish_list,"w")
            for line in data:
                if line in nopublish_data:
                    continue
                print(line,file=output)
            output.close()
            
        if publish_line in nopublish_data:
            nopublish_data.remove(publish_line)
            output = open(nopublish_list,"w")
            for line in nopublish_data:
                print(line,file=output)
            output.close()

        page_file = self.gen_public_link(link,self.public_dir)
        
        curdir = os.getcwd()
        repodir = "./%s/.repo/" % self.public_dir
        
        repo_file = self.gen_public_link(link,repodir)
        filename = os.path.basename(repo_file)

        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)        

        if os.path.exists(page_file):
            os.remove(page_file)
            print("\033[34m[Warning]\033[0m: delete %s done!" % page_file)

        if os.path.exists(repo_file):
            os.remove(repo_file)
            print("\033[34m[Warning]\033[0m: delete %s done!" % repo_file)
            os.chdir(repodir)
            os.system("git  commit -am 'recall %s' >/dev/null;git push origin %s >/dev/null" % (filename,self.deploy_branch))
            os.chdir(curdir)


        print("\033[34m[Info]\033[0m: Recall %s done!" % notename)

        

    def do_publish(self,notename=""):
        import os.path
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]

        publish_line = util.publish_note(notename,self.source_dir)
        if publish_line == None:
            print("\033[31m[ERROR]\033[0m: Can not publish note: %s, are you sure the html file exists?" % notename)
            return

        print(publish_line)
            
        nopublish_data = open(nopublish_list,"r").readlines()
        nopublish_data = [i.strip() for i in nopublish_data if not i.startswith("#")]

        if not os.path.exists(publish_list):
            output = open(publish_list,"w")
            print(publish_line,file=output)
            output.close()
        else:
            data = open(publish_list,"r").readlines()
            data = [i.strip() for i in data if not i.startswith("#")]

            if publish_line in nopublish_data:
                print(" it is in no-public file '%s', will not publish!" % self.nopublic_file)
                return

            if publish_line in data:
                print(" publish done")
                return
            
            output = open(publish_list,"w")
            print(publish_line,file=output)
            for line in data:
                if line in nopublish_data: 
                    continue
                print(line,file=output)
            output.close()
        print("publish done")

    def scan(self,note_dir = None):
        """
        scan the note_dir, build a dict with notes
        """

        if note_dir == None:
            note_dir = self.source_dir

        for path,dirs,files in os.walk(note_dir):
            if dirs: continue
            for _file in files:
                if not _file.endswith(".org") and not _file.endswith(".md"):continue
                _path = path + "/"+ _file
                if _path in [self.source_dir + self.public_file,self.source_dir + self.nopublic_file,self.source_dir + "about.org"]: continue
                if _path.endswith(".html"):continue
                self.notes_db[_path] = _path #_file

    def do_list(self):
        """
        list all notes
        """
        self.scan()
        for _note in reversed(sorted(self.notes_db.keys())):
            print(_note)

    def do_org2html(self,note=""):
        if note:
            if note.endswith(".org"):
                #print("Run: emacs -l scripts/init-orgnote.el --batch %s --funcall org-html-export-to-html" % note)
                util.to_page(note)
            else:
                print("%s not .org file" % note)
        else:
            self.scan()
            for _note in reversed(sorted(self.notes_db.keys())):                        
                if _note.endswith(".org"):
                    #print("Run: emacs -l scripts/init-orgnote.el --batch %s --funcall org-html-export-to-html" % _note)
                    util.to_page(_note)

    def do_md2html(self,note=""):
        if note:
            if note.endswith(".md"):
                util.to_page_mk2(note)
            else:
                print("%s not .md file" % note)
        else:
            self.scan()
            for _note in reversed(sorted(self.notes_db.keys())):
                if _note.endswith(".md"):
                    util.to_page_mk2(_note)



    def do_status(self):
        
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]
        
        publish_data = open(publish_list,"r").readlines()
        publish_data = [i.strip() for i in publish_data if not i.startswith("#")]

        nopublish_data = open(nopublish_list,"r").readlines()
        nopublish_data = [i.strip() for i in nopublish_data if not i.startswith("#")]
        
        all_publish = True
        self.scan()
        for _note in reversed(sorted(self.notes_db.keys())):                        
            if _note.endswith(".org"):
                _html = _note.replace(".org",".html")
            elif _note.endswith(".md"):
                _html = _note.replace(".md",".html")
            else:
                _html = _note

            publish_line = util.publish_note(self.notes_db[_note],self.source_dir)

            if publish_line not in publish_data and publish_line not in nopublish_data:
                #if _html in publish_data or _html in nopublish_data:
                #    print("Warning: %s (title) updated!" % _note)
                #    print("\tPlease update it in %s/public.org or %s/nopublic.org" % (_note,self.source_dir,self.source_dir))
                #    print("\tWith: %s" % publish_line)
                #else:
                print("\033[34m[Warning]\033[0m: %s not publish yet!" % _note)
                # \033[34m蓝色字\033[0m
                # \033[41;37m红色\033[0m
                all_publish = False

        # check .html exists
        for _note in publish_data:
            if _note.endswith(".org"):
                _html = _note.replace(".org",".html")
            elif _note.endswith(".md"):
                _html = _note.replace(".md",".html")
            else:
                continue

            if os.path.exists(_note) and not os.path.exists(_html):
                all_publish = False
                print("\033[34m[Warning]\033[0m: %s not generate html file yet!" % _note)
                publish_line = util.publish_note(_note,_note)

        if all_publish:
            print("all notes published!")
            
        

def usage():
    import sys
    
    print("""
Usage: orgnote <command>

Commands:
  init       Create a new OrgNote folder
  new        Create a new .org or .md post
  list       List this blog notes
  status     Status of those notes
  org2html   Run Emacs to convert .org to .html
  md2html    convert .md to .html
  publish    Publish a note
  recall     Cancel publish a note
  generate   Generate static files
  server     Start the server
  deploy     Deploy your website
  help       Get help on a command
  version    Display version information
    
For more help, you can check the docs:  http://orgnote.readthedocs.org/zh_CN/latest/
    """)

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
            print("init....")
            orgnote.init.main()
        elif sys.argv[1] == "deploy":
            blog.do_deploy()
        elif sys.argv[1] == "version":
            print(orgnote.__version__)
        elif sys.argv[1] == "generate":
            blog.do_generate()
        elif sys.argv[1] == "list":
            blog.do_list()
        elif sys.argv[1] == "status":
            blog.do_status()
        elif sys.argv[1] == "org2html":
            blog.do_org2html()
        elif sys.argv[1] == "md2html":
            blog.do_md2html()
        else:
            usage()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "server":
            blog.do_server(sys.argv[2])
        elif sys.argv[1] == "new":
            blog.do_new(sys.argv[2])
        elif sys.argv[1] == "publish":
            blog.do_publish(sys.argv[2])
        elif sys.argv[1] == "generate":
            blog.do_generate("http://localhost:" + sys.argv[2]) # port: 8080
        elif sys.argv[1] == "deploy":
            blog.do_deploy(sys.argv[2])
        elif sys.argv[1] == "recall":
            blog.do_recall(sys.argv[2])
        elif sys.argv[1] == "org2html":
            blog.do_org2html(sys.argv[2])
        elif sys.argv[1] == "md2html":
            blog.do_md2html(sys.argv[2])
        else:
            usage()
    else:
        usage()

if __name__ == "__main__":
    import sys
    sys.exit(main())
