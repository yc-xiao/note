'''
    异步的原则是遇到IO阻塞时，程序不做等待(用户态控制=>协程，系统态控制=>线程)，遇到CPU密集型时协程也是木有用的。
    如果是多核那可以考虑多进程，python存在GIL，同一时间CPU只运行一个线程。
    在web应用中一个web服务还是单个请求还是需要占用CPU，在py无法同时使用多核导致存在劣势。

    asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，
    然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。
    用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，
    然后在coroutine内部用yield from调用另一个coroutine实现异步操作。
    为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，
    可以让coroutine的代码更简洁易读。

    event_loop 事件循环：程序开启一个无限循环，把一些函数注册到事件循环上，当满足事件发生的时候，调用相应的协程函数
    coroutine 协程：协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用。
    task 任务：一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含了任务的各种状态
    future: 代表将来执行或没有执行的任务的结果。它和task上没有本质上的区别
    async/await 关键字：python3.5用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口。

'''
