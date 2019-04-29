from utility.utility import generate_uuid
from random import randint
from random import choice


config_ids = ['0962a74d-2322-44dc-9184-7ed214c6c4b0', '65174d16-d00d-4da2-8a9c-789030fbbad0',
              '71992353-3804-4cdc-bf67-df2adb13b331', 'b1e6cf3c-32b8-4611-b9eb-2e137dc27a7f',
              'b5a69be5-b91b-444a-83da-48216a2ce053']


def generate_value():
    return randint(100, 500) / 10


if __name__ == '__main__':
    quantity = 30

    for _ in range(0, quantity):
        print("INSERT INTO sensor_value VALUES ('{0}', CURRENT_TIMESTAMP, {1}, '{2}');"
              .format(generate_uuid(), generate_value(), choice(config_ids)))
