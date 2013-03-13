如何在SAE上安装和运行Trac
---------------------------

1.  下载本示例代码，进入本代码所在目录，使用以下命令打包安装所有的依赖包

        saecloud install -r requirements.txt

    该命令会下载 `Trac-1.0.1` 并安装到应用的 `site-packages` 目录下。

2.  修改 `project/conf/trac.ini` 中的mysql配置为你的应用的配置。

        [trac]
        ...
        database=mysql://$accesskey:$secretkey@w.rdc.sae.sina.com.cn:3307/app_$appname

3.  修改 `config.yaml` 中的应用名为你的应用名，部署应用。

        saecloud deploy

4.  打开 http://$appname.sinaapp.com 即可看到示例trac的页面了。

5.  删除 `project` 目录，使用 `trac-admin` 创建你自己的项目，根据需要修改 `index.wsgi`
    中的 `TRAC_ENV` 环境变量即可。

示例页面： http://tractest.sinaapp.com
