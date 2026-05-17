import asyncio
import time

import ray

"""
取消任务(也就是取消类中的方法执行)

未调度的任务：如果 Ray 尚未调度 Actor 任务，Ray 会尝试取消调度。当 Ray 在此阶段成功取消时，它会调用 ray.get(actor_task_ref)，该调用会产生一个 TaskCancelledError。

运行中的 Actor 任务（常规 Actor、线程 Actor）：对于被归类为单线程 Actor 或多线程 Actor 的任务，Ray 没有提供中断机制。

运行中的异步 Actor 任务：对于被归类为 异步 Actor 的任务，Ray 会尝试取消关联的 asyncio.Task。这种取消方法符合 asyncio 任务取消 中提出的标准。请注意，如果你不在异步函数中 await，asyncio.Task 在执行过程中不会被中断。
"""
@ray.remote(num_cpus=1)
class Counter(object):
    async def f(self):
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            print("Actor task cancelled")


counter = Counter.remote()
f_ref = counter.f.remote()

time.sleep(1)
ray.cancel(f_ref)

try:
    ray.get(f_ref)
except counter.exceptions.RayTaskError:
    print("Object reference was cancelled")
