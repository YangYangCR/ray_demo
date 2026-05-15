import time

import ray

ray.init()

"""
    @ray.remote这个注解加到一个方法上，会生成一个Task
    无状态 执行完就结束
"""
@ray.remote(num_cpus=1)
def add(x, y):
    return x + y


"""
    @ray.remote这个注解加到一个class上，会生成一个Actor 长期运行的服务
    Actor = 运行在远程进程中的长期存活、有状态、可RPC调用的对象
    Actor约等于一个自动部署的微服务
    为什么Actor是有状态的? 
    因为worker进程不会退出，所以value值一直存在，所以是有状态的
"""
@ray.remote(num_cpus=1)
class Counter:
    def __init__(self):
        self.i = 0

    def get(self):
        return self.i

    def incr(self, value):
        self.i += value


"""
    请求Ray集群启动一个新的worker进程，
    在该远程worker进程中创建counter对象
    counter是远程对象的引用
    执行过程： 1、提交Actor创建请求 2、寻找资源 @ray.remote(num_cpus=1) 
    3、启动worker进程 4、在worker进程中实例化对象 
"""
c = Counter.remote()
print(f"type of c is {type(c)}")
"""
    RPC调用到远程Actor(实际是发送Actor Message)
    多次调用remote方法，相当于发送消息到Actor对应的mailbox队列中
    Actor会按照顺序一个一个处理
"""
c.incr.remote(1)
c.incr.remote(1)
c.incr.remote(1)

# Retrieve final actor state.
print(ray.get(c.get.remote()))
"""
    在 Ray 里，Driver 就是：
    启动 Ray 作业的那个 Python 主程序
"""
time.sleep(10000000)