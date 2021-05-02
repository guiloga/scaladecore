#!/usr/bin/env python

import time

from faker import Faker


# @entrypoint
def execute(fi):
    # var1 = fi.inputs.get_variable('my-var1')
    fake = Faker()
    name = fake.name()
    print(f'Fake name: {name}')

    print('Sleeping 15 seconds ..')
    time.sleep(15)
    print('Finished Job')


if __name__ == '__main__':
    execute()
