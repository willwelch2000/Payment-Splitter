from PaymentCollection import *

def getPaymentListAsLines(collection : PaymentCollection, condense : bool = True) -> list[str]:
    lines : list[str] = []
    for payment in collection.payments:
        if isinstance(payment, DirectPayment):
            lines.append(f"Direct payment: {payment.payer}, {payment.recipient}, ${payment.amount:0.2f}")
        elif isinstance(payment, SharedPayment):
            payers = payment.payers
            nonPayers = collection.people.difference(payers)
            line = "Shared payment: "
            if (not condense) or len(payers) <= len(nonPayers) or any(p not in collection.people for p in payers):
                line += f"[{', '.join(payers)}]"
            elif collection.people == payers:
                line += "All"
            else:
                line += f"All except [{', '.join(nonPayers)}]"
            line += f", {payment.recipient}, ${payment.amount:0.2f}"
            lines.append(line)
        else:
            raise Exception("Unknown payment type")
    return lines

def checkValidAmount(amount : str) -> float:
    if len(amount) == 0:
        raise Exception("Amount must have > 0 characters")
    start = 1 if amount[0] == "$" else 0
    return float(amount[start:])

def checkValidName(name : str) -> str:
    if len(name) == 0:
        raise Exception("Name must have > 0 characters")
    invalidChars = [" ", "[", "]", ","]
    if any(char in name for char in invalidChars):
        raise Exception("Invalid name: " + name)
    return name