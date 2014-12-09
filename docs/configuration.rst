配置
=========

更新 `_config.yml` 文件:

.. note::
   由于YAML对中文支持不好，配置文件里面最好一律使用英文。


博客与作者信息
---------------

::
 
   # OrgNote Configuration
   ## Docs: http://lesliezhu.github.io/OrgNote/
   ## Source: https://github.com/LeslieZhu/OrgNote
   
   # Site
   title: OrgNote
   subtitle: "A simple org-mode blog, write blog by org-mode in Emacs"
   
   author: OrgNote
   email: pythonisland@gmail.com
   
   language: zh-CN


.. note::

   `language` 最好设置为 `zh-CN` ,虽然设置为 `en` 也可以，但OrgNote使用中文比较稳妥。


博客描述与关键字
----------------

::
   
   # About this blog
   description: "Use OrgNote."
   keywords: "OrgNote,Emacs,org-mode,blog,python,geek"
   

.. note::
   这个 `description` 会作为 `About` 页面的内容，支持HTML标签方式。


博客文件目录设置
-----------------

::

   # URL
   ## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
   url: http://yoursite.com
   root: /
   
   
   # Directory
   # if the source_dir is ./notes, then set 'source_dir' as 'notes', not include the '/'
   public_dir: public
   source_dir: notes

.. note::
   
   如果为自己的某个GitHub项目创建网页，并且使用了OrgNote，则由于GitHub会对该项目使用类似 `http://yoursite.github.io/child` 的URL，则root应该设置为 `/child/`.

   对于 `public_dir`, `source_dir` 目录前后都不需要增加 `/` 字符。
   

主题与外观
-----------

::

   # Category & Tag
   default_tag: "札记"
   
   # Theme
   # the default is 'freemind' and it's only theme for OrgNote now
   theme: freemind
   
   
   # Pagination
   ## the note num of each page
   per_page: 6

.. note::
   目前OrgNote只能使用默认的freemind主题。
   

多说评论框
----------

::

   # duoshuo
   duoshuo_shortname:
  

.. note::
   这里添多说评论框的用户ID即可，会自动生成调用代码；如果将多说自动生辰的代码都添加在这里，反而无法工作，切记!

边框布局
---------

::

   # layout
   ## 1: enable
   ## 0: disable
   ### if 'sidebar_show` is disable, igore all `sidebar` option
   ### the sidebar item display as the config order, sidebar items list:
   ### sidebar_latest,sidebar_tags,sidebar_time,sidebar_weibo,sidebar_link
   
   sidebar_show: 1
   sidebar:
     - sidebar_latest
     - sidebar_tags
     - sidebar_time
     - sidebar_link

.. note::
   右边的边框内容，显示顺序是根据这里的排列顺序，如果不需要某个内容，则不要写到这里即可。

链接
-----


::

   # links, each link should setting url,name,icon
   links:
     link1:
       url: http://lesliezhu.github.com
       name: Leslie Zhu
       icon: fa fa-github
     link2:
       url: https://github.com/LeslieZhu/OrgNote
       name: OrgNote
       icon: fa fa-github


.. note::
   对于每个连接的 `link1`, `link2` 等名字都无所谓，但建议使用 `link-num` 的形式。
