class auto_init:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)

        pre_init = getattr(obj, "__pre_init__", None)
        if callable(pre_init):
            pre_init()

        init = getattr(obj, "__init__", None)
        if callable(init):
            init(*args, **kwargs)

        post_init = getattr(obj, "__post_init__", None)
        if callable(post_init):
            post_init()

        return obj