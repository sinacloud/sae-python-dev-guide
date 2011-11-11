其他问题
===============

app版本
-----------

SAE app 代码以数字标识版本，如pythondemo应用有4个版本::

    jaime@westeros:~/source/chenfeng/pythondemo$ ls
    1  2  3  4

代码必须被放到某个版本数字目录里，默认为版本 1，可以在网页界面更改。

改变默认版本之后，请确保当前版本路径在sys.path最前面，防止误导入到旧版本的模块

