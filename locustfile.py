import random

from locust import HttpUser, task, constant_throughput
from data_factory import get_register_data
import queue
import loader


class FecMallUser(HttpUser):
    host = 'http://appserver.fecmall.com'

    @task(5)
    def open_index(self):

        url = '/cms/home/index'
        with self.client.get(url=url, catch_response=True, name='登录首页') as response:
            if response.status_code != 200:
                response.failure('失败了')
            print(response.json())

    @task(1)
    def register_user(self):

        url = '/customer/register/account'
        data = get_register_data(iterations=1)[0]

        with self.client.post(url=url, catch_response=True, data=data, name='注册账号') as response:
            if response.status_code != 200:
                response.failure('失败了')
            print(response.json())

    # 参数化 一次次取出放回
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = queue.Queue()

    def on_start(self):
        csv_list = loader.load_csv_file('./data/user.csv')
        for item in csv_list:
            self.q.put(item)

    # 参数化 登录
    @task(2)
    def multi_login(self):
        item = self.q.get()

        url = '/customer/login/account'
        data = {'email': item['email'], 'password': item['password']}
        # print('参数化登陆账号', data)

        with self.client.post(url=url, catch_response=True, data=data, name='登录账号') as response:
            if response.status_code != 200:
                response.failure('失败了')
            print(response.json())

        self.q.put(item)

    @task(2)
    def get_info(self):
        data = {'email': '1033817498@qq.com', 'password': '123456'}
        with self.client.post(url='/customer/login/account', catch_response=True, data=data, name='获取信息token') as response:
            if response.status_code != 200:
                response.failure('失败了')
            print(response.json())
            # print(response.headers)
            # print('token', response.headers['Access-Token'])
            token = response.headers.get('Access-Token')

        headers = {'Access-Token': token}

        with self.client.get(url='/customer/account/index', catch_response=True, headers=headers, name='账号查询') as response1:
            if response1.status_code != 200:
                response1.failure('失败了')
            print(response1.json())

        with self.client.get(url='/customer/address/index', catch_response=True, headers=headers, name='地址查询') as response2:
            if response2.status_code != 200:
                response2.failure('失败了')
            print(response2.json())

        with self.client.get(url='/checkout/cart/index', catch_response=True, headers=headers, name='购物车查询') as response3:
            if response3.status_code != 200:
                response3.failure('失败了')
            print(response3.json())

        with self.client.get(url='/customer/order/index', catch_response=True, headers=headers, name='订单查询') as response4:
            if response4.status_code != 200:
                response4.failure('失败了')
            print(response4.json())

    @task(2)
    def add_cart(self):

        data = {'email': '1033817498@qq.com', 'password': '123456'}
        with self.client.post(url='/customer/login/account', catch_response=True, data=data, name='获取购物车token') as response:
            if response.status_code != 200:
                response.failure('失败了')
            token = response.headers.get('Access-Token')

        product_id = random.randint(1, 10)
        num = random.randint(1, 5)

        headers = {'Access-Token': token}
        data = {'custom_option': {"my_color": "red", "my_size": "S", "my_size2": "S2", "my_size3": "S3"},
                'product_id': str(product_id),
                'qty': int(num)}
        with self.client.post(url='/checkout/cart/index', data=data, headers=headers, name='添加购物车') as response:
            if response.status_code != 200:
                response.failure('失败了')
            print(response.json())

    @task(2)
    def submit_order(self):

        data = {'email': '1033817498@qq.com', 'password': '123456'}
        with self.client.post(url='/customer/login/account', catch_response=True, data=data, name='获取订单token') as response:
            if response.status_code != 200:
                response.failure('失败了')
            token = response.headers.get('Access-Token')

        headers = {'Access-Token': token}
        data = {'address_id': '1',
                'billing': {'first_name': "yanjiang", 'last_name': "li", 'email': "1033817498@qq.com", 'telephone': "15757825661",
                            'street1': "杭州湾",
                            'street2': "",
                            'country': "CN",
                            'state': "ZJ",
                            'city': "宁波市",
                            'zip': "315336"},
                'customer_password': "",
                'confirm_password': "",
                'create_account': 0,
                'shipping_method': "fast_shipping",
                'payment_method': "paypal_standard"}
        with self.client.post(url='/checkout/onepage/submitorder', data=data, headers=headers, name='提交订单') as response:
            if response.status_code != 200:
                response.failure('失败了')
            print(response.json())
