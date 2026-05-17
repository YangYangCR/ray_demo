import ray
from ray.actor import ActorClass, ActorProxy

"""
不使用注解而是使用api来生成Actor

优先使用 ray.remote(MyClass) 而不是 @ray.remote 来定义 Actor：
与其使用 @ray.remote 装饰你的类，不如使用 ActorClass = ray.remote(MyClass)。
这保留了原始类类型，并允许类型检查器和 IDE 推断正确的类型。

使用 @ray.method 来定义 Actor 方法：使用 @ray.method 装饰 Actor 方法，
以启用对 Actor 句柄的远程方法调用的类型提示。

使用 ActorClass 和 ActorProxy 类型：当你实例化一个 Actor 时，
将句柄注解为 ActorProxy[MyClass]，以获取远程方法的类型提示
"""


class Counter:

    def __init__(self):
        self.value = 0

    @ray.method
    def increment(self) -> int:
        self.value += 1
        return self.value


# 生成Actor
counter_actor: ActorClass[Counter] = ray.remote(Counter)
# 获取actor的引用
counter: ActorProxy[Counter] = counter_actor.remote()

# 执行远程方法
obj_ref: ray.ObjectRef[int] = counter.increment.remote()
print(ray.get(obj_ref))
