import numpy as np
from numbers import Number

class Expense:
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount

    def getCategory(self):
        return self.category

    def getAmountOverMonthRange(self, start=0, end=11):
        return round(self.amount[start:end+1].sum(), 2)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        if isinstance(amount, Number):
            self._amount = np.array([amount / 12] * 12)
        elif len(amount) == 12:
            self._amount = np.array(amount)
        else:
            print(f"Unable to add amount because only {len(amount)} entries were given. An expense should be a list with 12 entries corresponding to each month.")


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.expenses = []

    def addExpense(self, expense: Expense):
        self.expenses.append(expense)

    def getExpenses(self):
        return self.expenses