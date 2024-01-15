from globals import global_vars


class CBA:
    # Cost Benefit Analysis of a credit card based on annual expense assumptions
    def __init__(self, ratio=1):
        self.annual_cost = 0
        self.annual_points = 0
        self.point_to_dollar_ratio = ratio
        self.bonus_toggle = global_vars.bonus_toggle

    def addPoints(self, points):
        self.annual_points = self.annual_points + points

    def addCost(self, cost):
        self.annual_cost = self.annual_cost + cost

    def getAnnualCost(self):
        return self.annual_cost

    def getAnnualPoints(self):
        return self.annual_points

    def getAnnualBenefits(self):
        return self.annual_points * self.point_to_dollar_ratio

    def getNetValue(self):
        return self.getAnnualBenefits() - self.getAnnualCost()


def calculator(expenses, credit_card, years=1):
    cba = CBA(ratio=credit_card.getPointToDollarRatio())
    for year in range(1, years + 1):
        threshold_total = 0
        threshold_month_limit = credit_card.getBonusLimit()
        for expense in expenses:
            expense_category = expense.getCategory()
            spending_amount = expense.getAmountOverMonthRange()
            multiplier = credit_card.getPointsMultiplier(expense_category)
            expense_limit = credit_card.getPointsLimit(expense_category)

            # If the spending_amount is greater than the point limit, then calculate the earned
            # points by only giving the multiplier to the amount below the spending limit.
            if spending_amount > expense_limit:
                default_multiplier = credit_card.getDefaultMultiplier()
                points = (expense_limit * multiplier) + (spending_amount - expense_limit) * default_multiplier
            else:
                points = spending_amount * multiplier
            cba.addPoints(points)
            threshold_total = threshold_total + expense.getAmountOverMonthRange(0, threshold_month_limit - 1)

        # If the spending total meets the bonus threshold within the month limit, add the bonus points
        if cba.bonus_toggle:
            bonus_threshold = credit_card.getBonusThreshold()
            if threshold_total >= bonus_threshold and year == 1:
                bonus_points = credit_card.getBonusPoints()
                cba.addPoints(bonus_points)

        annual_fee_check = credit_card.getAnnualFeeFreeMonths()
        if annual_fee_check < year * 12:
            cba.addCost(credit_card.getAnnualFee())

    return cba
