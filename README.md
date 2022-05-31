# Fecmall_locust
一个在linux部署fecmall平台+netdata资源监控工具，并通过locust开展的负载压力测试

代码部分 data文件夹存放得是随机生成的账号密码，用来登录测试，data_factory为注册数据生成模块，loader可以读取csv里账号密码，locustfile为测试主文件，需要在终端输入locust -f locustfile.py启动，如果文件名指定为locustfile,直接输locust也可以启动

![image](https://user-images.githubusercontent.com/64000814/171212167-024c6b21-035f-4b62-a30e-cc4c9eac7a03.png)

启动后，locust会生成一个ip地址，在浏览器中打开http://localhost:8089/即可
启动页面如下：

![image](https://user-images.githubusercontent.com/64000814/171211762-e19e7399-6030-482b-a129-8fff4212f498.png)

在单登陆场景下，依循缓慢增加原理，可以观察到当用户数为每秒16个时，吞吐量已达顶峰66，不再随着用户的增加而增加，响应时间从初始的200毫秒以下，在30个用户稳定时最高将近1秒，CPU此时也已接近98%（虚拟机只给了两个核心）

![image](https://user-images.githubusercontent.com/64000814/171218258-33fcda87-5e9d-4cd7-8bcd-60377b48edc6.png)
![image](https://user-images.githubusercontent.com/64000814/171218368-c62819e0-4a71-4c0a-a280-b5ac2957f1d1.png)
![image](https://user-images.githubusercontent.com/64000814/171218299-f43984f3-c99a-46bb-ade8-5631db50cb47.png)
![image](https://user-images.githubusercontent.com/64000814/171217319-51243269-dc61-4095-9bb7-c0c2973f58bb.png)

在混合场景下，假设单位时间内用户注册的数量为1，以此为基准，设登录首页查看商品的用户数量为5，登录的用户为2，查询账号/地址/购物车信息/订单信息的用户数为2，添加商品到购物车的用户为2，提交订单的数量为1，再考虑到等待时间，设每个用户考虑时间随机为 1-10秒之间


可以看到，在考虑混合场景后，在单接口场景下的30用户稳定下，CPU基本稳定在15%以下，吞吐量在8左右，响应时间都在200毫秒以下

![image](https://user-images.githubusercontent.com/64000814/171230360-6fe7a5e5-27e5-4b05-9232-01e537597d74.png)

说明可以继续缓慢增压，直到看到瓶颈出现

经过不断尝试，可以发现当用户数在220左右时，系统发生一次中断，具体如图，吞吐量归零后重新攀升，但并不随着用户数的增加继续上升，响应时间急速增加后回落，但实际并无连接错误出现

![image](https://user-images.githubusercontent.com/64000814/171234962-654da073-3482-461b-a23c-e657cd90728e.png)
![image](https://user-images.githubusercontent.com/64000814/171235028-2308285c-38da-4bff-9294-05c02ccfaf0b.png)

具体请求数据统计如下

![image](https://user-images.githubusercontent.com/64000814/171235116-a1b7fbc7-d340-4789-821a-116c05fe39ad.png)

于此，可以简单定位在假设的复合场景下，个人两核心，4G内存的虚拟linux系统上部署的fecmall电商平台瓶颈最大可支持每秒220用户数请求，瓶颈原因可以看出是硬件资源的不足，性能测试考虑因素太多，此处只是简单分析，并无多少实际意义，希望继续深入学习
