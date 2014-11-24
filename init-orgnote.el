;; 设置org-mode输出中文目录
(custom-set-variables
 '(org-blank-before-new-entry 
   (quote ((heading) (plain-list-item))))

 '(org-export-language-setup 
   (quote 
    (("en" "Author" "Date" "Table of Contents" "Footnotes") ("zh-CN" "作者" "日期" "目录" "脚注")))))
 
