import pandas as pd
import numpy as np
import cost_benefit_calculator as cbc

class Recommender:
    def __init__(self, person, card_list, years=1):
        net_benefits = []
        net_costs = []
        for card in card_list:
            cba = cbc.calculator(person.getExpenses(), card, years=years)
            net_benefits.append(cba.getAnnualBenefits())
            net_costs.append(cba.getAnnualCost())
        self.recommendation_df = pd.DataFrame({
            "Card": [x.getName() for x in card_list],
            "Net Benefit ($)": net_benefits,
            "Net Costs ($)": net_costs,
            "Net Value ($)": np.array(net_benefits) - np.array(net_costs)
        })

    def getRecommendation(self):
        # Return the card name with the maximum net value
        return self.recommendation_df.loc[self.recommendation_df["Net Value ($)"].idxmax()]

    def getRecommendationName(self):
        return self.getRecommendation()["Card"]

    def getRecommendationNetValue(self):
        return self.getRecommendation()["Net Value ($)"]




