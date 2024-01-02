def stuff(**kwargs):
    print(kwargs)
    print(type(kwargs))

x = {'a': 1, 'b':2}
stuff(**x)