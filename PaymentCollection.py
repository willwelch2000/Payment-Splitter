from Payment import *

class PaymentCollection:
    """
    A collection of necessary payments that can be condensed into a few transactions
    """
    def __init__(self, payments : list[Payment] = [], people : set[str] = set()):
        """
        Initialize new payment collection
        
        :param payments: Starting list of necessary payments
        :type payments: list[Payment]
        :param people: People to be considered when referring to "all"
        :type people: set[str]
        
        """
        self.payments = payments
        self.people = people

    @property
    def payments(self) -> list[Payment]:
        """
        Get list of payments
        
        :return: List of payments
        :rtype: list[Payment]
        """
        return self._payments

    @property
    def people(self) -> set[str]:
        """
        Get group of people to be considered when referring to "all"
        
        :return: Set of people to be considered when referring to "all"
        :rtype: set[str]
        """
        return self._people

    @payments.setter
    def payments(self, value : list[Payment]):
        """
        Set list of payments
        
        :param value: List of payments
        :type value: list[Payment]
        """
        self._payments = value

    @people.setter
    def people(self, value : set[str]):
        """
        Set group of people to be considered when referring to "all"
        
        :param value: Set of people to be considered when referring to "all"
        :type value: set[str]
        """
        self._people = value

    def getOverallAmountsOwed(self) -> dict[str, float]:
        """
        Get a dictionary mapping people to how much they are owed based on the added payments
        
        :return: Dictionary mapping people to how much they are owed based on the added payments
        :rtype: dict[str, float]
        """
        owed = {}
        for payment in self.payments:
            paymentAmountsOwed = payment.getAmountsOwed()
            for person in paymentAmountsOwed:
                if person in owed:
                    owed[person] += paymentAmountsOwed[person]
                else:
                    owed[person] = paymentAmountsOwed[person]
        return owed

    def getSimplifiedPayments(self) -> list[DirectPayment]:
        """
        Simplify the payments into as few transactions as possible by calculating the total amount owed each person
        
        :return: List of direct payments to be made in place of every individual payment in the list
        :rtype: list[DirectPayment]
        """
        owed = self.getOverallAmountsOwed()
        newPaymentList : list[DirectPayment] = []
        while True:
            # Find highest debt and credit
            minOwed : tuple[str, float] = ("", 0.0)
            maxOwed : tuple[str, float] = ("", 0.0)
            for p in owed:
                val = owed[p]
                if val < minOwed[1]:
                    minOwed = (p, val)
                if val > maxOwed[1]:
                    maxOwed = (p, val)
            # Check for end case or impossibility
            if minOwed[1] > -1e-5 or maxOwed[1] < 1e-5:
                if not (minOwed[1] > -1e-5 and maxOwed[1] < 1e-5):
                    raise Exception("Something impossible happened")
                return newPaymentList
            # Add new transaction to list and adjust amounts owed
            payer, recipient, amount = minOwed[0], maxOwed[0], min(-minOwed[1], maxOwed[1])
            newPaymentList.append(DirectPayment(payer, recipient, amount))
            owed[payer] += amount
            owed[recipient] -= amount

    def addSharedPayment(self, recipient : str, amount : float, peopleToExclude : set[str] = set()):
        """
        Shortcut to add a payment that is shared by all people in the set of people for this object
        
        :param recipient: Name of person that needs to be paid
        :type recipient: str
        :param peopleToExclude: People to exclude from the full set of people for this object (for the shared payment)
        :type peopleToExclude: set[str]
        """
        payers = self.people.difference(peopleToExclude)
        if len(payers) == 0:
            raise Exception("Must have at least one payer--make sure list of people is set")
        self.payments.append(SharedPayment(payers, recipient, amount))