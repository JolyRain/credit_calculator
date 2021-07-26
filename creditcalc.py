from abc import ABC, abstractmethod


class CreditCalc(ABC):
    def __init__(self, loan_amount=0, period=0, rate=0):
        self.loan = loan_amount
        self.period = period
        self.rate = rate

    @abstractmethod
    def all_payments(self):
        pass

    @abstractmethod
    def total_payment(self):
        pass

    @abstractmethod
    def overpayment(self):
        pass

    @abstractmethod
    def monthly_payment(self, month):
        pass

    @abstractmethod
    def monthly_percent(self, month):
        pass

    @abstractmethod
    def monthly_credit_body(self, month):
        pass

    @abstractmethod
    def monthly_remainder(self, month):
        pass


class DiffCalc(CreditCalc):

    def all_payments(self):
        payments_array = []
        months_count = self.period * 12
        remainder = self.loan
        while months_count != 0:
            monthly_payment = self.credit_body() + (remainder * self.rate / 1200)
            payments_array.append(round(monthly_payment, 2))
            remainder -= self.credit_body()
            months_count -= 1
        return payments_array

    def monthly_payment(self, month):
        if month < 0 or month > self.period * 12:
            return
        return round(self.all_payments()[month], 2)

    def monthly_percent(self, month):
        return round(self.monthly_payment(month) - self.credit_body(), 2)

    def credit_body(self):
        return round(self.loan / (self.period * 12), 2)

    def total_payment(self):
        return round(sum(self.all_payments()), 2)

    def overpayment(self):
        return round(self.total_payment() - self.loan, 2)

    def monthly_credit_body(self, month):
        return round(self.credit_body(), 2)

    def monthly_remainder(self, month):
        if month + 1 == self.period * 12:
            return 0
        remainder = self.loan
        while month >= 0:
            remainder -= self.credit_body()
            month -= 1
        return round(remainder, 2)


class AnnCalc(CreditCalc):

    def monthly_payment(self, month=0):
        months_count = self.period * 12
        period_rate = self.rate / 1200
        annuity = (period_rate * (1 + period_rate) ** months_count) / (((1 + period_rate) ** months_count) - 1)
        return round(self.loan * annuity, 2)

    def total_payment(self):
        return round(self.monthly_payment() * self.period * 12, 2)

    def overpayment(self):
        return round(self.total_payment() - self.loan, 2)

    def __month_data(self, month):
        period_rate = self.rate / 1200
        remainder = self.loan
        percent_payment, credit_body = 0, 0
        while month >= 0:
            percent_payment = remainder * period_rate
            credit_body = self.monthly_payment() - percent_payment
            remainder -= credit_body
            month -= 1
        return round(percent_payment, 2), round(credit_body, 2), round(remainder, 2)

    def all_payments(self):
        payments = []
        for i in range(self.period * 12):
            payments.append(self.monthly_payment())
        return payments

    def monthly_percent(self, month):
        return self.__month_data(month)[0]

    def monthly_credit_body(self, month):
        return self.__month_data(month)[1]

    def monthly_remainder(self, month):
        return self.__month_data(month)[2] if month + 1 != self.period * 12 else 0
