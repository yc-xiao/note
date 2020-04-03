from __init__ import *
from threading_pool.otask import Task

task = Task(func=sorted, desc='helloc', args=([1,2,3],))
task.run()
print(task)
