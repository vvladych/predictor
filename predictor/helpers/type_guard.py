

def typecheck(func):
    def func_wrapper(*args,**kwargs):
        if not isinstance(args[1], args[0].dao):
            raise BaseException("cannot add, type doesn't match %s %s" % (args[0], args[0].dao.__name__))
        return func(*args)
    return func_wrapper


def consistcheck(s=None):
    def wrap(f):
        def func_wrapper(*args):            
            if not hasattr(args[0], "entity") or args[0].entity is None:
                raise NotImplementedError("entity for dao %s is None" % args[0].dao_class)
            # TODO: else: test for entity in db with simple select
            if not s in args[0].sql_dict or args[0].sql_dict[s] is None:
                raise NotImplementedError("%s in sql_dict not available" % s)
            return f(*args)
        return func_wrapper
    return wrap