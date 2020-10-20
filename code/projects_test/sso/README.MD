- sso 单点登录
    apps 表示任意的服务
    login 登录验证的服务
- 流程
    1.访问apps需要登录的服务，跳转到login进行登录
    2.login登录后，跳转到apps，apps再访问login(带token)
    3.
