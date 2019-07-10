from utility.utility import generate_uuid
from random import randint
from random import choice


config_ids = ['04700c39-608d-4f7e-8d60-e3a01abc3d75', '1ca45209-b40e-45c4-8db0-2f3ad500094c',
              '2d54fc54-b8d0-4e00-ae34-e0441bf09ce7', '8f5a5414-b42e-4a0f-9b8d-2965e6b755e7']  # ,
              # 'd5ddfff3-56eb-4991-868b-c971860d6c8f']


def generate_value():
    return randint(100, 500) / 10


if __name__ == '__main__':
    quantity = 30

    for _ in range(0, quantity):
        print("INSERT INTO sensor_value VALUES ('{0}', CURRENT_TIMESTAMP, {1}, '{2}');"
              .format(generate_uuid(), generate_value(), choice(config_ids)))
