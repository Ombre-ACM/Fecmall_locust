import random
from mimesis import Person
from mimesis.enums import Gender
from mimesis.schema import Schema


def get_register_data(iterations=1):
    p = Person()

    schema = Schema(schema=lambda: {'email': p.email(domains=['qq.com', '163.com'], unique=True),
                                    'password': '123456',
                                    'firstname': p.first_name(gender=Gender.FEMALE if random.randint(1, 10) > 6 else Gender.MALE),
                                    'lastname': p.last_name(),
                                    'is_subscribed': True if random.randint(1, 10) > 6 else False
                                    })

    return schema.create(iterations=iterations)
