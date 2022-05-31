# Fecmall_locust
一个在linux部署fecmall平台+netdata资源监控工具，并通过locust开展的负载压力测试

代码部分 data文件夹存放得是随机生成的账号密码，用来登录测试，data_factory为注册数据生成模块，loader可以读取csv里账号密码，locustfile为测试主文件，需要在终端输入locust -f locustfile.py启动，如果文件名指定为locustfile,直接输locust也可以启动

![image](https://user-images.githubusercontent.com/64000814/171212167-024c6b21-035f-4b62-a30e-cc4c9eac7a03.png)

启动后，locust会生成一个ip地址，在浏览器中打开http://localhost:8089/即可
启动页面如下：

![image](https://user-images.githubusercontent.com/64000814/171211762-e19e7399-6030-482b-a129-8fff4212f498.png)
