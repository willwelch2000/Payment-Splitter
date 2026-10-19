from PaymentCollection import *
from PaymentCollectionFile import *
from CommandLineBuilder import *

# collection = PaymentCollection()
# collection.payments.append(DirectPayment("Will", "Mari", 100.0))
# collection.payments.append(SharedPayment(["Mari", "Cole", "Will"], "Will", 60))
# collection.people = {"Mari", "Cole", "Will"}
# collection.addSharedPayment("Will", 60, {"Mari"})
# collection = parseFile(Path("example1.txt"))
# print(collection.getOverallAmountsOwed())
# for payment in collection.getSimplifiedPayments():
#     print(payment)
collection = CommandLineBuilder.create()