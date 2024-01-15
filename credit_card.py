class CreditCard:
    def __init__(self, name, comp, ratio=1/100, default_point_multiplier=1):
        self.name = name
        self.company = comp
        self.point_ratio = ratio

        self.point_category_none_value = 10**100

        self.default_point_multiplier = default_point_multiplier


        # Initialize some required variables with 0 values
        self.point_categories = []
        self.setOpeningBonus()
        self.setAnnualFee()

    def getName(self):
        return self.name

    def getCompany(self):
        return self.company

    def addPointsMultiplier(self, category, multiplier, limit=None):
        # Set the point category limit to an arbitrarily large number if there is no limit.
        if limit is None:
            limit = self.point_category_none_value
        self.point_categories.append({"category": category, "multiplier": multiplier, "limit": limit})

    def getPointsMultiplier(self, category):
        # Get the points multiplier associated with a category. If a category cannot be found,
        # set the value to the default point multiplier
        return self.getPointsCategoryHelper(category, key="multiplier", default_value=self.default_point_multiplier)

    def getDefaultMultiplier(self):
        return self.default_point_multiplier

    def getPointsLimit(self, category):
        # Get the points multiplier limit with a category. If a category cannot be found,
        # set the default value to an arbitrarily large value for when no limit exists.
        return self.getPointsCategoryHelper(category, key="limit", default_value=self.point_category_none_value)

    def getPointsCategoryHelper(self, category, key, default_value=None):
        # Helper function to search through the point_categories list and extract details
        # based on the key. Returns a given default value if it cannot find a category.
        for category_dict in self.point_categories:
            if category_dict["category"] == category:
                return category_dict[key]
        return default_value

    def getPointToDollarRatio(self):
        return self.point_ratio

    def setOpeningBonus(self, points=0, spending_criteria=0, months_limit=0):
        self.bonus_points = points
        self.bonus_threshold = spending_criteria
        self.bonus_limit = months_limit

    def getBonusThreshold(self):
        return self.bonus_threshold

    def getBonusPoints(self):
        return self.bonus_points

    def getBonusLimit(self):
        return self.bonus_limit

    def setAnnualFee(self, amount=0, free_months=0):
        self.annual_fee = amount
        self.annual_fee_free_months = free_months

    def addToAnnualFee(self, additional_amount):
        self.annual_fee = self.annual_fee + additional_amount

    def getAnnualFee(self):
        return self.annual_fee

    def getAnnualFeeFreeMonths(self):
        return self.annual_fee_free_months