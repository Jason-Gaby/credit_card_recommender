import unittest
import cost_benefit_calculator as cbc
from credit_card import CreditCard
from person import Person, Expense


class SingleYearTestCases(unittest.TestCase):
    def test_single_category_calculator(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.addPointsMultiplier("Travel", 5, 500_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Travel", 1_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(5_000, cba.getAnnualPoints())

    def test_multi_category_calculator(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.addPointsMultiplier("Travel", 5, 500_000)
        self.test_card.addPointsMultiplier("Dining", 3, 500_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Travel", 1_000))
        self.test_person.addExpense(Expense("Dining", 1_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(8_000, cba.getAnnualPoints())

    def test_single_category_cash_back(self):
        self.test_card = CreditCard(name="Cash Back", comp="American Express", ratio=1, default_point_multiplier=0.01)
        self.test_card.addPointsMultiplier("Travel", 0.05, 5_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Travel", 1_000))
        self.test_person.addExpense(Expense("Other", 1_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(60, cba.getAnnualBenefits())

    def test_category_over_limit(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.addPointsMultiplier("Travel", 5, 1_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Travel", 2_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(6_000, cba.getAnnualPoints())

    def test_cash_back_category_over_limit(self):
        self.test_card = CreditCard(name="Cash Back", comp="American Express", ratio=1, default_point_multiplier=0.01)
        self.test_card.addPointsMultiplier("Travel", 0.05, 5_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Travel", 6_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(260, cba.getAnnualBenefits())

    def test_expense_category_has_no_multiplier(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.addPointsMultiplier("Travel", 5, 1_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Dining", 2_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(2_000, cba.getAnnualPoints())

    def test_meet_bonus_toggle_on(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setOpeningBonus(80_000, 6_000, 6)

        self.test_person = Person("Test", "User")
        expenses = [1_000] * 12
        self.test_person.addExpense(Expense("Dining", expenses))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(12_000 + 80_000, cba.getAnnualPoints())

    def test_meet_bonus_toggle_off(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setOpeningBonus(80_000, 6_000, 6)

        self.test_person = Person("Test", "User")
        expenses = [1_000] * 12
        self.test_person.addExpense(Expense("Dining", expenses))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(12_000 + 80_000, cba.getAnnualPoints())

    def test_miss_bonus(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setOpeningBonus(80_000, 6_000, 6)

        self.test_person = Person("Test", "User")
        expenses = [500] * 12
        self.test_person.addExpense(Expense("Dining", expenses))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(6_000, cba.getAnnualPoints())

    def test_annual_fee_no_free(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setAnnualFee(200, 0)

        self.test_person = Person("Test", "User")

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(200, cba.getAnnualCost())

    def test_annual_fee_free_year(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setAnnualFee(200, 12)

        self.test_person = Person("Test", "User")

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card)
        self.assertEqual(0, cba.getAnnualCost())

class MultiYearTestCases(unittest.TestCase):
    def test_meet_bonus_year_one(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setOpeningBonus(80_000, 6_000, 6)

        self.test_person = Person("Test", "User")
        expenses = [1_000] * 12
        self.test_person.addExpense(Expense("Dining", expenses))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card, years=2)
        self.assertEqual(24_000 + 80_000, cba.getAnnualPoints())

    def test_annual_fee_free_first_year(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.setAnnualFee(200, 12)

        self.test_person = Person("Test", "User")

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card, years=2)
        self.assertEqual(200, cba.getAnnualCost())

    def test_multi_category_calculator_two_years(self):
        self.test_card = CreditCard(name="Platinum Card", comp="American Express")
        self.test_card.addPointsMultiplier("Travel", 5, 500_000)
        self.test_card.addPointsMultiplier("Dining", 3, 500_000)

        self.test_person = Person("Test", "User")
        self.test_person.addExpense(Expense("Travel", 1_000))
        self.test_person.addExpense(Expense("Dining", 1_000))

        cba = cbc.calculator(self.test_person.getExpenses(), self.test_card, years=2)
        self.assertEqual(16_000, cba.getAnnualPoints())

if __name__ == '__main__':
    unittest.main()
