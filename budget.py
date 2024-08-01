class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = []
        self.balance = 0
        self.total_withdrawn = 0

    def __str__(self):

        # adds title line to output string
        self.output = f'{self.category_name:*^30}\n'

        # adds each description and amount to output string
        for item in self.ledger:
            formatted_amount = str(format(item['amount'], '.2f'))
            description = item['description']
            description = description[:23] if len(description) > 23 else description
            self.output += f'{description:23}{formatted_amount:>7}\n' 
        
        # adds total balance to output string
        formatted_balance = str(format(self.balance, '.2f'))
        self.output += 'Total: ' + formatted_balance

        return self.output

    # deposit in amount 
    def deposit(self, amount, description = ''):
        self.balance += amount
        self.ledger.append({'amount': amount, 'description': description})

    # withdraw amount
    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.balance -= amount
            self.total_withdrawn += amount
            self.ledger.append({'amount': amount * -1, 'description': description})
            return True
        return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.balance -= amount
            self.ledger.append({'amount': amount * -1, 'description': f'Transfer to {category.category_name}'})
            category.deposit(amount, f'Transfer from {self.category_name}')
            return True
        return False

    def check_funds(self, amount):
        if amount > self.balance:
            return False
        return True

    def percentage_spent(self, total_spent):
        return round((self.total_withdrawn / total_spent) * 100, -1)


def create_spend_chart(categories):
    spend_chart = 'Percentage spent by category\n'

    total_spent = sum(category.total_withdrawn for category in categories)
    
    for i in range(100, -10, -10):
        spend_chart += f'{i:>3}|'
        for category in categories:
            if category.percentage_spent(total_spent) >= i:
                spend_chart += ' o '
            else:
                spend_chart += '   '
        spend_chart += ' \n'
    
    spend_chart += '    ' + '---' * len(categories) + '-\n'

    end_point = max(len(category.category_name) for category in categories)

    for j in range(end_point):
        spend_chart += '    '
        for category in categories:
            name = getattr(category, 'category_name', '')
            if j < len(name):
                spend_chart += f' {name[j]} '
            else:
                spend_chart += '   '
        spend_chart += '\n'
        
    
    return spend_chart.rstrip('\n')
