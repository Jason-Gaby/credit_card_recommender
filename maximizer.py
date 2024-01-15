from credit_card import CreditCard
from person  import Person, Expense
import cost_benefit_calculator as cbc

class Maximizer:
    def __init__(self, person: Person, card_list: [CreditCard], years=1):
        # For each category, pick the best card based on the maximum net value
        # Once a card has been picked a single time, the fee is a sunk cost, so it should be omitted from future calculations
        # As a result of this "fee sunk cost", the algorithm is sensitive to initial conditions. As such, run the algorithm
        # starting with a different initial condition each time, and pick the run that returns the best net value.

        expenses = person.getExpenses()
        best_run = -1_000_000_000
        for run_iteration in range(len(expenses)):
            best_cards = {}
            fee_count, bonus_count = initializeCounters(card_list)
            for i in range(len(expenses)):
                expense = expenses[(run_iteration + i) % len(expenses)]
                max_category_net_value = -1_000_000_000
                expense_category = expense.getCategory()
                expense_amount = expense.getAmountOverMonthRange()
                for card in card_list:
                    temp_card = CreditCard(name=card.getName(), comp=card.getCompany(), ratio=card.getPointToDollarRatio())
                    temp_card.addPointsMultiplier(category=expense_category, multiplier=card.getPointsMultiplier(expense_category))

                    if fee_count.getKeyValue(card.getName()):
                        annual_fee = 0
                    else:
                        annual_fee = card.getAnnualFee()
                    temp_card.setAnnualFee(amount=annual_fee, free_months=card.getAnnualFeeFreeMonths())

                    if bonus_count.getKeyValue(card.getName()) < card.getBonusThreshold():
                        temp_card.setOpeningBonus(points=card.getBonusPoints(), spending_criteria=card.getBonusThreshold(), months_limit=card.getBonusLimit())
                    else:
                        temp_card.setOpeningBonus(points=0, spending_criteria=0, months_limit=0)

                    temp_person = Person("Temp", "User")
                    temp_person.addExpense(Expense(amount=expense_amount, category=expense_category))

                    cba = cbc.calculator(temp_person.getExpenses(), temp_card, years=years)
                    category_net_value = cba.getNetValue()
                    if max_category_net_value < category_net_value:
                        max_category_net_value = category_net_value
                        best_cards[expense_category] = {"card": temp_card, "value": category_net_value}

                # update credit card counters based on the card added to the best cards list
                new_card = best_cards[expense_category]["card"].getName()
                fee_count.setKeyValue(new_card, True)
                bonus_count.setKeyValue(new_card, bonus_count.getKeyValue(new_card) + expense_amount)

            cbas = [cbc.calculator([expenses[(run_iteration + i) % len(expenses)]], best_cards[key]["card"], years=years) for i, key in enumerate(best_cards)]
            total_net_value = getNetValueMultiCBA(cbas)
            if total_net_value > best_run:
                best_run = total_net_value
                self.optimal_cbas = cbas
                self.recommendations = best_cards

    def getRecommendations(self):
        return self.recommendations

    def getRecommendationValue(self):
        return getNetValueMultiCBA(self.optimal_cbas)


def initializeCounters(card_list):
    # Initialize the counters for use with the maximizer function
    fee_count = CreditCardCounter()
    bonus_count = CreditCardCounter()
    for card in card_list:
        fee_count.setKeyValue(card.getName(), False)
        bonus_count.setKeyValue(card.getName(), 0)
    return fee_count, bonus_count


def getNetValueMultiCBA(cbas):
    # Compute the net value for multi CBA objects (Cost Benefit Analysis)
    net_value = 0
    for cba in cbas:
        net_value = net_value + cba.getNetValue()
    return net_value


class CreditCardCounter:
    # This class is used to keep track of card information using a dictionary
    # It is a helper class to Maximizer
    def __init__(self):
        self.counter = {}

    def checkForKey(self, key):
        return key in self.counter

    def setKeyValue(self, key, value):
        self.counter[key] = value

    def getKeyValue(self, key):
        return self.counter[key]

# def _createOptimalCard(recommendations):
#     # This function creates a new CreditCard object that takes in a dictionary of recommended cards per category
#     # and creates an optimal card that is a combination of all of these best in category cards.
#     optimal_card = CreditCard(name="Optimal Card", comp="N/A")
#     optimal_card.setAnnualFee(amount=0, free_months=0)
#     optimal_card.setOpeningBonus(points=0, spending_criteria=0, months_limit=0)
#     for expense_category in recommendations:
#         expense_card = recommendations[expense_category]
#         optimal_card.addPointsMultiplier(category=expense_category, multiplier=expense_card.getPointsMultiplier(expense_category), limit=expense_card.getPointsLimit(expense_category))
#         optimal_card.addToAnnualFee(expense_card.getAnnualFee())
#     return optimal_card

