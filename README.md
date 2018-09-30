Flask-blog
======
感谢 Miguel Grinberg 提供的 flask 学习。[https://github.com/miguelgrinberg/flasky-first-edition]

有何修改：
----
* 修改了一些前端样式，并布置成中文。
* 新增了一些功能。
* 改进了头像功能，用户可以自由上传头像。
* 实现了类似 django-admin 的后台。
* 集成了 flask-DebugToolbar 进行调试。
* 数据库可以支持 mysql。

部署：
---
在linux环境中使用 Nginx+Gunicorn+supervisor来部署。

    * supervisor 管理 Gunicorn 配置参考 supervisor.txt。
    * nginx 配置参考 nginx.txt。
