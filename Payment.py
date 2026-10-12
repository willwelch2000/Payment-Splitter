from abc import ABC, abstractmethod

class Payment(ABC):
    """
    Abstract base class describing a payment involving 2 or more people
    """

    @abstractmethod
    def getAmountsOwed(self) -> dict[str, float]:
        """
        Get a dictionary mapping people to how much they are owed based on this payment
        
        :return: Dictionary mapping people to how much they are owed based on this payment
        :rtype: dict[str, float]
        """
        pass

class DirectPayment(Payment):
    """
    A payment that needs to be made directly from one person to another
    """

    def __init__(self, payer : str, recipient : str, amount : float):
        """
        Initialize new direct payment
        
        :param payer: Name of person that needs to pay
        :type payer: str
        :param recipient: Name of person that needs to be paid
        :type recipient: str
        :param amount: Amount, in dollars, to be paid
        :type amount: float
        """
        super().__init__()
        self.payer = payer
        self.recipient = recipient
        self.amount = amount

    @property
    def payer(self) -> str:
        """
        Get name of payer
        
        :return: Name of payer
        :rtype: str
        """
        return self._payer

    @property
    def recipient(self) -> str:
        """
        Get name of recipient
        
        :return: Name of recipient
        :rtype: str
        """
        return self._recipient

    @property
    def amount(self) -> float:
        """
        Get amount, in dollars, to be paid
        
        :return: Amount, in dollars, to be paid
        :rtype: float
        """
        return self._amount

    @payer.setter
    def payer(self, value : str):
        """
        Set name of payer
        
        :param value: Name of payer
        :type value: str
        """
        self._payer = value

    @recipient.setter
    def recipient(self, value : str):
        """
        Set name of recipient
        
        :param value: Name of recipient
        :type value: str
        """
        self._recipient = value

    @amount.setter
    def amount(self, value : float):
        """
        Set amount, in dollars, to be paid
        
        :param value: Amount, in dollars, to be paid
        :type value: float
        """
        self._amount = value

    def getAmountsOwed(self) -> dict[str, float]:
        return {
            self._payer : -self._amount,
            self._recipient : self._amount,
        }

    def __str__(self) -> str:
        return f"{self.payer} to {self.recipient}: ${self.amount:.2f}"
    
class SharedPayment(Payment):
    """
    A payment that needs to be shared between 2 or more people
    """

    def __init__(self, payers : set[str], recipient : str, amount : float):
        """
        Initialize new shared payment
        
        :param payers: List of people responsible for the payment who together need to pay the recipient (may include the recipient)
        :type payers: list[str]
        :param recipient: The person who paid the expense initially and needs to be paid
        :type recipient: str
        :param amount: Amount, in dollars, of expense
        :type amount: float
        """
        super().__init__()
        self.recipient = recipient
        self.payers = payers
        self.amount = float(amount)

    @property
    def recipient(self) -> str:
        """
        Get name of recipient, the person who paid for the expense initially
        
        :return: Name of recipient
        :rtype: str
        """
        return self._recipient

    @property
    def payers(self) -> set[str]:
        """
        Get set of people responsible for payment who together need to pay the recipient
        
        :return: Set of people responsible for payment who together need to pay the recipient
        :rtype: set[str]
        """
        return self._payers

    @property
    def amount(self) -> float:
        """
        Get amount, in dollars, of expense
        
        :return: Amount, in dollars, of expense
        :rtype: float
        """
        return self._amount

    @recipient.setter
    def recipient(self, value : str):
        """
        Set name of recipient, the person who paid for the expense initially
        
        :param value: Name of recipient
        :type value: str
        """
        self._recipient = value

    @payers.setter
    def payers(self, value : set[str]):
        """
        Set the set of people responsible for payment who together need to pay the recipient
        
        :param value: Set of people responsible for payment who together need to pay the recipient
        :type value: set[str]
        """
        if len(value) == 0:
            raise Exception("Payers set must have length > 0")
        self._payers = value

    @amount.setter
    def amount(self, value : float):
        """
        Set amount, in dollars, of expense
        
        :param value: Amount, in dollars, of expense
        :type value: float
        """
        self._amount = float(value)

    def getAmountsOwed(self) -> dict[str, float]:
        # Because of rounding, recipient may get slightly more or less than expected
        numPayers = len(self.payers)
        dividedValue = round(self.amount/numPayers, 2)
        owed = {payer: -dividedValue for payer in self.payers}
        if self.recipient in owed:
            owed[self.recipient] += dividedValue*numPayers
        else:
            owed[self.recipient] = dividedValue*numPayers
        return owed