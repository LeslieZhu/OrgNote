快速使用
============

首先，你应该在 `GitHub <https://github.com/>`_ 上建立一个项目 **yourname.github.com**,这里的 `yourname` 是你在GitHub上的用户名.

然后按照步骤执行:

::

  $ git clone git@github.com:yourname/yourname.github.com.git

  $ cd yourname.github.com

  $ orgnote init                       # 初始化目录

  $ orgnote new note-name              # 添加一篇博文

  $ orgnote list                       # 列出所有博文

  $ orgnote status                     # 查看博文是否在发布列表中

  $ orgnote publish note-name          # 将博文添加到发布列表中

  $ orgnote generate                   # 生成博客

  $ orgnote server [port]              # 在本地预览效果，默认通过 localhost:8080 查看效果

  $ orgnote deploy                     # 部署到服务器
