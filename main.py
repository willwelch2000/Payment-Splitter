from PaymentCollection import *

collection = PaymentCollection()
collection.payments.append(DirectPayment("Will", "Mari", 100.0))
collection.payments.append(SharedPayment("Will", ["Mari", "Cole", "Will"], 60))
print(collection.getOverallAmountsOwed())
for payment in collection.getSimplifiedPayments():
    print(payment)