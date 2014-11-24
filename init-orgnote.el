;; 设置org-mode输出中文目录
(custom-set-variables
 '(column-number-mode t)
 '(display-battery-mode t)
 '(display-time-mode t)
 '(org-blank-before-new-entry (quote ((heading) (plain-list-item))))
 '(org-export-language-setup (quote (("en" "Author" "Date" "Table of Contents" "Footnotes") ("zh-CN" "作者" "日期" "目录" "脚注"))))
 '(show-paren-mode t)
 '(size-indication-mode t)
 '(text-mode-hook (quote (turn-off-auto-fill text-mode-hook-identify))))
