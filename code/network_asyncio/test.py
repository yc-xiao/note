__str__ 打印实例输出语句
__rep__ 打印实例输出语句
__dir__ 返回实例的属性和方法
__new__ 类初始化时，生成实例
__init__　类初始化时，定义属性
__del__ 类回收时，执行
__len__ 返回类长度
__iter__　返回一个可迭代对象(实现__next__)
__slots__ 指定实例属性(限制)
__call__ a = A(), a() => __call__
getattr(instance, attr, default_value) 返回实例属性
setattr(instance, attr, value) 设置实例属性
delattr(instance, attr) 删除实例属性
isinstance(instance, class) 判断实例是否由类实例化
