def pdb(func, *args, **kw):
    import pdb; pdb.set_trace()
    result = func(*args, **kw)
    return result