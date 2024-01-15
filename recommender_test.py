import unittest
from credit_card import CreditCard
from person import Person, Expense
from recommender import Recommender


class MyTestCase(unittest.TestCase):
    def test_recommend_amex_gold_and_platinum(self):
        amex_platinum = CreditCard(name="Platinum Card", comp="American Express", ratio=1 / 100)
        amex_platinum.setAnnualFee(695)
        amex_platinum.setOpeningBonus(80_000, 6_000, 6)
        amex_platinum.addPointsMultiplier("Travel", 5, 500_000)

        amex_gold = CreditCard(name="Gold Card", comp="American Express", ratio=1 / 100)
        amex_gold.setAnnualFee(250)
        amex_gold.setOpeningBonus(60_000, 4_000, 6)
        amex_gold.addPointsMultiplier("Dining", 4)
        amex_gold.addPointsMultiplier("Groceries", 4, 25_000)
        amex_gold.addPointsMultiplier("Travel", 3)

        card_list = [amex_platinum, amex_gold]

        test_person_travel = Person("Travel", "User")
        test_person_travel.addExpense(Expense("Travel", 50_000))
        test_person_travel.addExpense(Expense("Dining", 10_000))

        test_person_food = Person("Food", "User")
        test_person_food.addExpense(Expense("Travel", 10_000))
        test_person_food.addExpense(Expense("Dining", 50_000))

        recommender_travel = Recommender(test_person_travel, card_list, years=1)
        self.assertEqual(recommender_travel.getRecommendationName(), "Platinum Card")
        self.assertEqual(recommender_travel.getRecommendationNetValue(), 2705)

        recommender_food = Recommender(test_person_food, card_list, years=1)
        self.assertEqual(recommender_food.getRecommendationName(), "Gold Card")
        self.assertEqual(recommender_food.getRecommendationNetValue(), 2650)

        recommender_travel = Recommender(test_person_travel, card_list, years=2)
        self.assertEqual(recommender_travel.getRecommendationName(), "Platinum Card")
        self.assertEqual(recommender_travel.getRecommendationNetValue(), 2705 + 1905)

        recommender_food = Recommender(test_person_food, card_list, years=2)
        self.assertEqual(recommender_food.getRecommendationName(), "Gold Card")
        self.assertEqual(recommender_food.getRecommendationNetValue(), 2650 + 2050)


if __name__ == '__main__':
    unittest.main()
