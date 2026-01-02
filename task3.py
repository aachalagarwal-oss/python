from abc import ABC,abstractmethod

class loggerMixin:
    def log_transaction(self,amount):
        print("payment received",amount)



class payment(ABC):
    def process_payment():
        pass

class Credit_class(payment,loggerMixin):
    def credit_fun(self,amount):
        print("Credit card evaluated")
        self.log_transaction(amount)

class Paypal(payment,loggerMixin):
    def paypal(self,amount):
        print("Paypal")
        self.log_transaction(amount)


cc=Credit_class()
pp=Paypal()

cc.credit_fun(5000)
pp.paypal(6000)