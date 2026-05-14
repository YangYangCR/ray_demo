# https://docs.ray.io/en/latest/ray-overview/getting-started.html

import ray

ray.init()

@ray.remote
def add(x, y):
    return x + y

obj_ref = add.remote(1, 2)

result = ray.get(obj_ref)

print(result)