import collections
from predictor.helpers.db_connection import get_db_connection

def transactional(func):
    def func_wrapper(*args,**kwargs):
        with TransactionBrokerWrapper() as transaction_broker:
            return func(*args)
    return func_wrapper

    
class TransactionBrokerWrapper:

    def __enter__(self):
        TransactionBroker().start()
        
    def __exit__(self, type, value, traceback):
        if isinstance(value, BaseException):
            TransactionBroker().rollback()
        else:
            TransactionBroker().stop()
        

class TransactionBroker(object):
    class __TransactionBroker(object):
        def __init__(self):
            self.queue = collections.deque([])
            
        def __str__(self):
            return "%s" % len(self.queue)
        
        def start(self):
            self.queue.append("1")

        def stop(self):
            self.queue.pop()
            if len(self.queue) == 0:
                get_db_connection().commit()

        def rollback(self):
            get_db_connection().rollback()
            self.queue = collections.deque([])

    instance = None

    def __init__(self):
        if not TransactionBroker.instance:
            TransactionBroker.instance = TransactionBroker.__TransactionBroker()
            
    def __str__(self):
        return "%s" % self.instance
            
    def start(self):
        self.instance.start()

    def stop(self):
        self.instance.stop()

    def rollback(self):
        self.instance.rollback()
