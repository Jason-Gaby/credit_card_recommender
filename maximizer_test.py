import unittest
from person import Person, Expense
from credit_card import CreditCard
from maximizer import Maximizer
from globals import global_vars


class MyTestCase(unittest.TestCase):
    def test_amex_gold_and_platinum_no_bonus_two_categories_mixed_outcome(self):
        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1 / 100)
        amex_gold.setAnnualFee(250)
        amex_gold.addPointsMultiplier("Dining", 4)
        amex_gold.addPointsMultiplier("Groceries", 4, 25_000)
        amex_gold.addPointsMultiplier("Travel", 3)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        test_person_travel.addExpense(Expense("Travel", 100_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))

        maximizer = Maximizer(test_person_travel, card_list)
        recommendations = maximizer.getRecommendations()
        self.assertEqual("Platinum Card", recommendations["Travel"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Dining"]["card"].getName())
        self.assertEqual(4455, maximizer.getRecommendationValue())


    def test_amex_gold_and_platinum_no_bonus_three_categories_mixed_outcome(self):
        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1 / 100)
        amex_gold.setAnnualFee(250)
        amex_gold.addPointsMultiplier("Dining", 4)
        amex_gold.addPointsMultiplier("Groceries", 4, 25_000)
        amex_gold.addPointsMultiplier("Travel", 3)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        test_person_travel.addExpense(Expense("Travel", 100_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))
        test_person_travel.addExpense(Expense("Groceries", 10_000))

        maximizer = Maximizer(test_person_travel, card_list)
        recommendations = maximizer.getRecommendations()
        self.assertEqual("Platinum Card", recommendations["Travel"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Dining"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Groceries"]["card"].getName())
        self.assertEqual(4855, maximizer.getRecommendationValue())

    def test_amex_gold_and_platinum_no_bonus_gold_is_best_outcome(self):
        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1 / 100)
        amex_gold.setAnnualFee(250)
        amex_gold.addPointsMultiplier("Dining", 4)
        amex_gold.addPointsMultiplier("Groceries", 4, 25_000)
        amex_gold.addPointsMultiplier("Travel", 3)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        # NOTE: This test has sensitivity to initial conditions. Do not change the order of the below expenses.
        # Also, do not change the values.
        test_person_travel.addExpense(Expense("Travel", 25_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))
        test_person_travel.addExpense(Expense("Groceries", 10_000))

        maximizer = Maximizer(test_person_travel, card_list)
        recommendations = maximizer.getRecommendations()
        self.assertEqual("Gold Card", recommendations["Travel"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Dining"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Groceries"]["card"].getName())
        self.assertEqual(1300, maximizer.getRecommendationValue())

    def test_amex_gold_cash_and_platinum_card_no_bonus_gold_is_best_outcome(self):
        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1)
        amex_gold.setAnnualFee(250)
        amex_gold.addPointsMultiplier("Dining", 0.04)
        amex_gold.addPointsMultiplier("Groceries", 0.04, 25_000)
        amex_gold.addPointsMultiplier("Travel", 0.03)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        # NOTE: This test has sensitivity to initial conditions. Do not change the order of the below expenses.
        # Also, do not change the values.
        test_person_travel.addExpense(Expense("Travel", 25_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))
        test_person_travel.addExpense(Expense("Groceries", 10_000))

        maximizer = Maximizer(test_person_travel, card_list)
        recommendations = maximizer.getRecommendations()
        self.assertEqual("Gold Card", recommendations["Travel"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Dining"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Groceries"]["card"].getName())
        self.assertEqual(1300, maximizer.getRecommendationValue())

    def test_amex_gold_cash_and_platinum_card_with_bonus(self):
        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)
        amex_platinum.setOpeningBonus(points=80_000, spending_criteria=6_000, months_limit=6)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1 / 100)
        amex_gold.setAnnualFee(250)
        amex_gold.addPointsMultiplier("Dining", 4)
        amex_gold.addPointsMultiplier("Groceries", 4, 25_000)
        amex_gold.addPointsMultiplier("Travel", 3)
        amex_gold.setOpeningBonus(points=60_000, spending_criteria=4_000, months_limit=6)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        test_person_travel.addExpense(Expense("Travel", 25_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))
        test_person_travel.addExpense(Expense("Groceries", 10_000))

        maximizer = Maximizer(test_person_travel, card_list, years=3)
        recommendations = maximizer.getRecommendations()
        self.assertEqual(4715, maximizer.getRecommendationValue())
        self.assertEqual("Platinum Card", recommendations["Travel"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Dining"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Groceries"]["card"].getName())

    def test_amex_gold_cash_and_platinum_card_with_bonus_and_toggle_off(self):
        global_vars.setBonusToggle(False)

        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)
        amex_platinum.setOpeningBonus(points=80_000, spending_criteria=6_000, months_limit=6)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1 / 100)
        amex_gold.setAnnualFee(250)
        amex_gold.addPointsMultiplier("Dining", 4)
        amex_gold.addPointsMultiplier("Groceries", 4, 25_000)
        amex_gold.addPointsMultiplier("Travel", 3)
        amex_gold.setOpeningBonus(points=60_000, spending_criteria=4_000, months_limit=6)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        test_person_travel.addExpense(Expense("Travel", 25_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))
        test_person_travel.addExpense(Expense("Groceries", 10_000))

        maximizer = Maximizer(test_person_travel, card_list, years=3)
        recommendations = maximizer.getRecommendations()
        self.assertEqual(3900, maximizer.getRecommendationValue())
        self.assertEqual("Gold Card", recommendations["Travel"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Dining"]["card"].getName())
        self.assertEqual("Gold Card", recommendations["Groceries"]["card"].getName())


if __name__ == '__main__':
    unittest.main()
