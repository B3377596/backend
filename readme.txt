##########前端启动方式###########
1.打开cmd进入frontend文件夹，运行npm install
2.npm run serve


##########后端启动方式#############
1.打开另一个cmd进入backend文件夹，进入虚拟环境，运行pip install -r requirements.txt
2.运行python manage.py makemigrations和运行python manage.py makemigrations back
2.运行python manage.py migrate
3.运行python manage.py runserver

##########访问网页################
浏览器访问http://localhost:8080/
两个cmd分别输出前后端信息
（ps:可能会出现前端端口转接不到后端的情况，这是因为被window拦截，打开安全中心防火墙，点击高级设置，进入入站规则，新建规则，点击端口选择TCP，本地特定端口选择8000，之后一直点下一个即可）
