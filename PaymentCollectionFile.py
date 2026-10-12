from PaymentCollection import *
from pathlib import Path

def createFile(collection : PaymentCollection, path : Path):
    lines : list[str] = []
    if len(collection.people) > 0:
        lines.append("People: " + ", ".join(collection.people))
    for payment in collection.payments:
        if isinstance(payment, DirectPayment):
            lines.append(f"Direct payment: {payment.payer}, {payment.recipient}, ${payment.amount:0.2f}")
        elif isinstance(payment, SharedPayment):
            payers = payment.payers
            nonPayers = collection.people.difference(payers)
            line = "Shared payment: "
            if len(payers) <= len(nonPayers) or any(p not in collection.people for p in payers):
                line += f"[{', '.join(payers)}]"
            elif collection.people == payers:
                line += "All"
            else:
                line += f"All except [{', '.join(nonPayers)}]"
            line += f", {payment.recipient}, ${payment.amount:0.2f}"
            lines.append(line)
        else:
            raise Exception("Unknown payment type")
    path.write_text("\n".join(lines))

def parseFile(path : Path) -> PaymentCollection:
    collection = PaymentCollection()
    for line in path.read_text().splitlines():
        colonIndex = line.index(":")
        if colonIndex < 0:
            raise Exception("':' should be included in each line")
        keyword, remaining = line[0:colonIndex].strip().lower(), line[(colonIndex+1):].strip()
        match keyword:
            case "people":
                people = [_checkValidName(p) for p in _splitCommasWithBracketAwareness(remaining)]
                collection.people = set(people)
            case "direct payment":
                values = _splitCommasWithBracketAwareness(remaining)
                if len(values) != 3:
                    raise Exception("Direct payment statement should be: {payer}, {recipient}, {value}")
                payer = _checkValidName(values[0])
                recipient = _checkValidName(values[1])
                amount = _checkValidAmount(values[2])
                collection.payments.append(DirectPayment(payer, recipient, amount))
            case "shared payment":
                values = _splitCommasWithBracketAwareness(remaining)
                if len(values) != 3:
                    raise Exception("Direct payment statement should be: {[payers]}, {recipient}, {value}")
                
                recipient = _checkValidName(values[1])
                amount = _checkValidAmount(values[2])

                lowerCaseFirstGroup = values[0].lower()
                if lowerCaseFirstGroup.startswith("["):
                    payers = set([_checkValidName(p) for p in _splitCommasWithBracketAwareness(values[0][1:-1])])
                    collection.payments.append(SharedPayment(payers, recipient, amount))
                elif lowerCaseFirstGroup == "all":
                    collection.addSharedPayment(recipient, amount)
                elif lowerCaseFirstGroup.startswith("all except ["):
                    excepted = [_checkValidName(p) for p in _splitCommasWithBracketAwareness(values[0][12:-1])]
                    collection.addSharedPayment(recipient, amount, set(excepted))
            case _:
                raise Exception("Unknown keyword: " + keyword)
    return collection

def _splitCommasWithBracketAwareness(line : str) -> list[str]:
    """
    Split a string by commas, avoiding splitting sections in brackets.
    Keeps up with levels of brackets
    
    :param line: Input string
    :type line: str
    """
    pieces : list[str] = []
    bracketCount = 0
    start = 0
    current = 0
    for current in range(len(line)):
        if line[current] == "," and bracketCount == 0:
            pieces.append(line[start:current].strip())
            start = current + 1
        elif line[current] == "[":
            bracketCount += 1
        elif line[current] == "]":
            bracketCount -= 1
        if bracketCount < 0:
            raise Exception("Closing bracket ']' before opening bracket '['")
    if bracketCount > 0:
        raise Exception(f"Brackets don't cancel out--should have {bracketCount} more closing brackets")
    pieces.append(line[start:].strip())
    return pieces

def _checkValidName(name : str) -> str:
    if len(name) == 0:
        raise Exception("Name must have > 0 characters")
    invalidChars = [" ", "[", "]", ","]
    if any(char in name for char in invalidChars):
        raise Exception("Invalid name: " + name)
    return name

def _checkValidAmount(amount : str) -> float:
    if len(amount) == 0:
        raise Exception("Amount must have > 0 characters")
    start = 1 if amount[0] == "$" else 0
    return float(amount[start:])