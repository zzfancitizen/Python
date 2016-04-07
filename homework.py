import functools

def decorator(func):
	@functools.wraps(func)
    def warps(*args, **kw):
        print("begin call")
        print(func(*args,**kw))
        print("end call")
        return
    return warps

@decorator
def square(x):
	return x * x

