from PaymentCollection import *
from PaymentCollectionFile import *
from Util import checkValidAmount
import time

class CommandLineBuilder:
    def __init__(self):
        self.collection : PaymentCollection = PaymentCollection()
        self.condenseSharedPayers = True

    @property
    def condenseSharedPayers(self) -> bool:
        """
        If true, payers in a shared payment will be described using 'All' if possible
        """
        return self._condenseSharedPayers

    @condenseSharedPayers.setter
    def condenseSharedPayers(self, value : bool):
        """
        If true, payers in a shared payment will be described using 'All' if possible
        """
        self._condenseSharedPayers = value

    @staticmethod
    def create(condenseSharedPayers : bool = True) -> PaymentCollection:
        """
        Create a PaymentCollection via the command line
        
        :return: The collection
        :rtype: PaymentCollection
        """
        builder = CommandLineBuilder()
        builder.condenseSharedPayers = condenseSharedPayers
        while builder._runLoop():
            pass
        return builder.collection

    # Returns true if it should keep going
    def _runLoop(self) -> bool:
        options = {
            "Add person" : "Add someone to the list of 'all' people",
            "View people" : "View list of 'all' people",
            "Add payment" : "Add a new shared payment",
            "View payments" : "View all payments included in the collection",
            "Save" : "Save payment collection to a file",
            "Finish" : "Exit the command line loop and analyze the payment collection",
            "Condense" : "Set the system to output payers in a shared payment using 'All' if possible",
            "No condense" : "Set the system to output individual payers in a shared payment rather than using 'All'",
        }
        print("What would you like to do? Options:")
        for option, description in options.items():
            print(f"\t{option}: {description}")
        selection = input("Selection: ").lower().strip()
        match selection:
            case "add person":
                self.collection.people.add(input("Person to add: "))
                print("New people list: " + ", ".join(self.collection.people))
            case "remove person":
                person = input("Person to remove: ")
                if person in self.collection.people:
                    self.collection.people.remove(person)
                print("New people list: " + ", ".join(self.collection.people))
            case "view people":
                print("People list: " + ", ".join(self.collection.people))
            case "add payment":
                self._addPayment()
            case "view payments":
                self._printPayments()
            case "save":
                filename = input("File name: ")
                createFile(self.collection, Path(filename))
            case "finish":
                for payment in self.collection.getSimplifiedPayments():
                    print(payment)
                return False
            case "condense":
                self.condenseSharedPayers = True
            case "no condense":
                self.condenseSharedPayers = False
        time.sleep(1)
        print()
        return True

    def _printPayments(self):
        for payment in self.collection.payments:
            if isinstance(payment, DirectPayment):
                print("Direct payment: ")
                print(f"\tPayer: {payment.payer}")
                print(f"\tRecipient: {payment.recipient}")
                print(f"\tAmount: ${payment.amount:0.2f}")
            elif isinstance(payment, SharedPayment):
                payers = payment.payers
                nonPayers = self.collection.people.difference(payers)
                print("Shared payment")
                print(f"\tPayers: ", end="")
                if (not self.condenseSharedPayers) or len(payers) <= len(nonPayers) or any(p not in self.collection.people for p in payers):
                    print(", ".join(payers))
                elif self.collection.people == payers:
                    print("All")
                else:
                    print(f"All except {', '.join(nonPayers)}")
                print(f"\tRecipient: {payment.recipient}")
                print(f"\tAmount: ${payment.amount:0.2f}")
            else:
                raise Exception("Unknown payment type")

    def _addPayment(self):
        type = input("Direct or shared payment (Enter 'Direct' or 'Shared'): ").lower().strip()
        if type not in ["direct", "shared"]:
            print("Must choose 'Direct' or 'Shared")
            return
        if type == "direct":
            payer = checkValidName(input("Payer: ").strip())
            recipient, amount = _getRecipientAndAmount()
            self.collection.payments.append(DirectPayment(payer, recipient, amount))
        else:
            usingAll = input("Shared between all? (y/n): ").lower().strip() == "y"
            if usingAll:
                exclude = [checkValidName(s.strip()) for s in input("People to exclude (comma separated): ").split(",")]
                recipient, amount = _getRecipientAndAmount()
                self.collection.addSharedPayment(recipient, amount, set(exclude))
            else:
                payers = [checkValidName(s.strip()) for s in input("Payers (comma separated): ").split(",")]
                recipient, amount = _getRecipientAndAmount()
                self.collection.payments.append(SharedPayment(set(payers), recipient, amount))
            self.collection

def _getRecipientAndAmount() -> tuple[str, float]:
    recipient = checkValidName(input("Recipient: ").strip())
    amount = checkValidAmount(input("Amount: ").strip())
    return recipient, amount