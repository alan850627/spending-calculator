import csv

spent = {}
paid = {}

with open('in.csv', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(rows) # get rid of first row
    for row in rows:
        payer = row[1]
        spenders = row[2].split(', ')
        amount = int(row[3])

        if paid.get(payer, None) is None:
            paid[payer] = 0
        paid[payer] += amount

        for spender in spenders:
            if spent.get(spender, None) is None:
                spent[spender] = 0
            spent[spender] += amount / len(spenders)


# ChatGPT Wrote this function. Makes sense to me.
def settle_expenses(spent, paid):
    # Calculate the net balance for each person
    balances = {person: paid.get(person, 0) - spent.get(person, 0) for person in set(spent) | set(paid)}

    # Create lists for creditors and debtors
    creditors = [(p, amt) for p, amt in balances.items() if amt > 0]
    debtors = [(p, -amt) for p, amt in balances.items() if amt < 0]

    transactions = []

    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt = debtors[i]
        creditor, credit = creditors[j]

        amount = min(debt, credit)
        transactions.append((debtor, creditor, amount))

        # Update balances
        debtors[i] = (debtor, debt - amount)
        creditors[j] = (creditor, credit - amount)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return transactions

print("Spendings", spent)
print("Paid", paid)

print("\nTo Settle:")
transactions = settle_expenses(spent, paid)
for t in transactions:
    print(t[0], 'pay', t[1], t[2])

