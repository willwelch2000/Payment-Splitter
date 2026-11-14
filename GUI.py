import tkinter as tk
from tkinter import ttk
from PaymentCollection import PaymentCollection
from Payment import *
import re

# Top-level GUI
root = tk.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

# Create payment collection
collection = PaymentCollection()

# Variables
newPersonVar = tk.StringVar()
paymentTypeVar = tk.StringVar()
directPayerVar = tk.StringVar()
recipientVar = tk.StringVar()
amountVar = tk.StringVar()
sharedPayersVar = tk.StringVar()
allPayersVar = tk.IntVar()

# Commands
def addNewPerson():
    newPerson = newPersonVar.get()
    collection.people.add(newPerson)
    newPersonVar.set("")
    refreshGUI()
    print(f"Adding {newPerson}")
    
def removePerson(person : str):
    collection.people.remove(person)
    refreshGUI()
    print(f"Removing {person}")

def setPaymentType(type : str):
    if type == 'direct':
        directPaymentFrm.grid()
        sharedPaymentFrm.grid_remove()
    elif type == 'shared':
        sharedPaymentFrm.grid()
        directPaymentFrm.grid_remove()
    allPaymentsFrm.grid()

def addPayment():
    type = paymentTypeVar.get()
    if type == 'direct':
        collection.payments.append(DirectPayment(directPayerVar.get(), recipientVar.get(), float(amountVar.get())))
    elif type == 'shared':
        if allPayersVar.get() == 1:
            collection.addSharedPayment(recipientVar.get(), float(amountVar.get()))
        else:
            payers = [x.strip() for x in sharedPayersVar.get().split(",") if len(x.strip()) > 0]
            collection.payments.append(SharedPayment(set(payers), recipientVar.get(), float(amountVar.get())))
    directPayerVar.set("")
    recipientVar.set("")
    amountVar.set("")
    sharedPayersVar.set("")
    refreshGUI()
    
def removePayment(payment : Payment):
    collection.payments.remove(payment)
    refreshGUI()

def allPayersCheckboxToggle():
    widgets : list[tk.Widget] = [sharedPayersLabel, sharedPayersEntry]
    allPayers = allPayersVar.get()
    [w.grid_remove() if allPayers else w.grid() for w in widgets]

def refreshGUI():
    # Manage people
    for person in collection.people:
        if person not in addedPeopleFrames:
            addedPeopleFrames[person] = getAddedPersonFrame(person)
    for person in list(addedPeopleFrames):
        if person not in collection.people:
            addedPeopleFrames.pop(person).destroy()
    # Manage payments
    for payment in collection.payments:
        if payment not in addedPaymentFrames:
            addedPaymentFrames[payment] = getAddedPaymentFrame(payment)
    for payment in list(addedPaymentFrames):
        if payment not in collection.payments:
            addedPaymentFrames.pop(payment).destroy()

def getAddedPersonFrame(person : str) -> ttk.Frame:
    frm = ttk.Frame(peopleFrm)
    frm.pack(side="top", anchor="w")
    ttk.Label(frm, text=person, font=font_normal).grid(row=0, column=0)
    remove = lambda : removePerson(person)
    ttk.Button(frm, text="Remove", command=remove).grid(row=0, column=1)
    return frm

def getAddedPaymentFrame(payment : Payment) -> ttk.Frame:
    frm = ttk.Frame(addedPaymentsFrame)
    frm.pack(side="top", anchor="w")
    if isinstance(payment, DirectPayment):
        ttk.Label(frm, text=str(payment), font=font_normal).grid(row=0, column=0)
    elif isinstance(payment, SharedPayment):
        text = f"Multiple to {payment.recipient}: ${payment.amount:.2f}"
        ttk.Label(frm, text=text, font=font_normal).grid(row=0, column=0)
    remove = lambda : removePayment(payment)
    ttk.Button(frm, text="Remove", command=remove).grid(row=0, column=1)
    return frm

# Data validation
def validateAmount(val):
    return re.fullmatch(r"\d*\.?\d{0,2}", val) is not None
amountValidate = root.register(validateAmount)

# General GUI settings
font_header = ("Arial", 16, "bold")
font_normal = ("Arial", 12, "")

# Top-level titles
ttk.Label(frm, text="People", font=font_header).grid(row=0, column=0)
ttk.Label(frm, text="Payments", font=font_header).grid(row=0, column=1)

# People
peopleFrm = ttk.Frame(frm)
peopleFrm.grid(row=1, column=0, padx=10, sticky="n")

newPersonFrm = ttk.Frame(peopleFrm)
newPersonFrm.pack(side="top")
ttk.Label(newPersonFrm, text="Add person: ", font=font_normal).pack(side="left")
ttk.Entry(newPersonFrm, textvariable=newPersonVar, font=font_normal).pack(side="left")
ttk.Button(newPersonFrm, text="Enter", command=addNewPerson).pack(side="left")
addedPeopleFrames : dict[str, ttk.Frame] = {}


# Payments
paymentsFrm = ttk.Frame(frm)
paymentsFrm.grid(row=1, column=1, padx=10)

paymentTypeFrm = ttk.Frame(paymentsFrm)
paymentTypeFrm.grid(row=0, column=0)
ttk.Label(paymentTypeFrm, text="Payment type: ", font=font_normal).pack(side="left")
for type in ['Direct', 'Shared']:
    ttk.Radiobutton(paymentTypeFrm, text=type, value=type.lower(), variable=paymentTypeVar, command=lambda type=type: setPaymentType(type.lower())).pack(side="left")

directPaymentFrm = ttk.Frame(paymentsFrm)
directPaymentFrm.grid(row=1, column=0)
ttk.Label(directPaymentFrm, text="Payer: ", font=font_normal).grid(row=0, column=0)
ttk.Entry(directPaymentFrm, textvariable=directPayerVar, font=font_normal).grid(row=0, column=1)
ttk.Label(directPaymentFrm, text="Recipient: ", font=font_normal).grid(row=1, column=0)
ttk.Entry(directPaymentFrm, textvariable=recipientVar, font=font_normal).grid(row=1, column=1)
ttk.Label(directPaymentFrm, text="Amount ($): ", font=font_normal).grid(row=2, column=0)
ttk.Entry(directPaymentFrm, textvariable=amountVar, font=font_normal,
          validate="key", validatecommand=(amountValidate, "%P")).grid(row=2, column=1)

sharedPaymentFrm = ttk.Frame(paymentsFrm)
sharedPaymentFrm.grid(row=2, column=0)
ttk.Checkbutton(sharedPaymentFrm, text="Shared between all", variable=allPayersVar,
                command=allPayersCheckboxToggle).grid(row=0, column=0)
sharedPayersLabel = ttk.Label(sharedPaymentFrm, text="Payers (A, B, C): ", font=font_normal)
sharedPayersLabel.grid(row=1, column=0)
sharedPayersEntry = ttk.Entry(sharedPaymentFrm, textvariable=sharedPayersVar, font=font_normal)
sharedPayersEntry.grid(row=1, column=1)
ttk.Label(sharedPaymentFrm, text="Recipient: ", font=font_normal).grid(row=2, column=0)
ttk.Entry(sharedPaymentFrm, textvariable=recipientVar, font=font_normal).grid(row=2, column=1)
ttk.Label(sharedPaymentFrm, text="Amount ($): ", font=font_normal).grid(row=3, column=0)
ttk.Entry(sharedPaymentFrm, textvariable=amountVar, font=font_normal,
          validate="key", validatecommand=(amountValidate, "%P")).grid(row=3, column=1)

# Widgets used for both payment types
allPaymentsFrm = ttk.Frame(paymentsFrm)
allPaymentsFrm.grid(row=3, column=0)
ttk.Button(allPaymentsFrm, text="Submit payment", command=addPayment).pack(side="left")

# List of added payments
addedPaymentsFrame = ttk.Frame(paymentsFrm)
addedPaymentsFrame.grid(row=4, column=0, sticky="w", pady=10)
addedPaymentFrames : dict[Payment, ttk.Frame] = {}

# Hide stuff
allPaymentsFrm.grid_remove()
directPaymentFrm.grid_remove()
sharedPaymentFrm.grid_remove()

root.mainloop()