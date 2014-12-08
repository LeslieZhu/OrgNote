命令自动补全
===================

在Bash中自动补全 `OrgNote <https://github.com/LeslieZhu/OrgNote>`_  命令.


安装
-------------

全局设置:

::

    $ git clone git@github.com:LeslieZhu/orgnote-bash-completion.git
    $ sudo cp ./orgnote-bash-completion/orgnote /etc/bash_completion.d/
    $ . /etc/bash_completion.d/orgnote


本地设置:

::

    $ mkdir -p ~/bash_completion.d
    $ cp ./orgnote-bash-completion/orgnote ~/bash_completion.d/
    $ echo "" >> ~/.bashrc
    $ echo 'if [ -f "$HOME/bash_completion.d/orgnote" ] ; then' >> ~/.bashrc
    $ echo '    . $HOME/bash_completion.d/orgnote' >> ~/.bashrc
    $ echo "fi" >> ~/.bashrc
    $ . ~/bash_completion.d/orgnote


用法
---------


列出orgnote命令的选项:

::

    $ orgnote [TAB]
    init new list status publish generate server deploy help version


自动补全命令:

::

    $ orgnote i[TAB]
    $ orgnote init
