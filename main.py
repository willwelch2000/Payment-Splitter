from PaymentCollection import *
from PaymentCollectionFile import *
from CommandLineBuilder import *
from GUI import run_GUI

# Example simply using Python
collection1 = PaymentCollection()
collection1.payments.append(DirectPayment("Will", "Mari", 100.0))
collection1.payments.append(SharedPayment(set(["Mari", "Cole", "Will"]), "Will", 60))
collection1.people = {"Mari", "Cole", "Will"}
collection1.addSharedPayment("Will", 60, {"Mari"})
print(collection1.getOverallAmountsOwed())
for payment in collection1.getSimplifiedPayments():
    print(payment)

# Example parsing from file
collection2 = parseFile(Path("ExampleFiles/example1.txt"))
print(collection2.getOverallAmountsOwed())
for payment in collection2.getSimplifiedPayments():
    print(payment)

# Use command-line builder or GUI
# collection = CommandLineBuilder.create()
run_GUI()