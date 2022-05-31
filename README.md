# Fecmall_locust
一个在linux部署fecmall平台+netdata资源监控工具，并通过locust开展的负载压力测试

代码部分 data文件夹存放得是随机生成的账号密码，用来登录测试，data_factory为注册数据生成模块，loader可以读取csv里账号密码，locustfile为测试主文件，需要在终端输入locust -f locustfile.py启动，如果文件名指定为locustfile,直接输locust也可以启动

![image](https://user-images.githubusercontent.com/64000814/171212167-024c6b21-035f-4b62-a30e-cc4c9eac7a03.png)

启动后，locust会生成一个ip地址，在浏览器中打开http://localhost:8089/即可
启动页面如下：

![image](https://user-images.githubusercontent.com/64000814/171211762-e19e7399-6030-482b-a129-8fff4212f498.png)

在单登陆场景下，依循缓慢增加原理，可以观察到当用户数为每秒16个时，吞吐量已达顶峰，不再随着用户的增加而增加，响应时间从初始的200毫秒以下，在30个用户稳定时最高将近1秒，CPU此时也已接近98%（虚拟机只给了两个核心）

![image](https://user-images.githubusercontent.com/64000814/171218258-33fcda87-5e9d-4cd7-8bcd-60377b48edc6.png)
![image](https://user-images.githubusercontent.com/64000814/171218368-c62819e0-4a71-4c0a-a280-b5ac2957f1d1.png)
![image](https://user-images.githubusercontent.com/64000814/171218299-f43984f3-c99a-46bb-ade8-5631db50cb47.png)
![image](https://user-images.githubusercontent.com/64000814/171217319-51243269-dc61-4095-9bb7-c0c2973f58bb.png)

在混合场景下，假设单位时间内用户注册的数量为1，以此为基准，设登录首页查看商品的用户数量为5，登录的用户为2，查询账号/地址/购物车信息/订单信息的用户数为2，添加商品到购物车的用户为2，提交订单的数量也为2，再考虑到等待时间，设每个用户在首页等待5秒，查询信息等待3秒，注册时间为5秒，登录时间1秒，添加商品到购物车10秒，提交订单选择地址及支付方式等时间为3秒
