import math


class Category:

    def __init__(self, cat_name):
        self.name = cat_name
        self.ledger = []
        self.balance = 0

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def get_balance(self):
        return self.balance

    def check_funds(self, amount):
        if self.balance >= amount:
            return True
        else:
            return False

    def withdraw(self, amount, description=""):
        if amount < self.balance:
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False

    def transfer(self, amount, dest_category):
        if self.balance >= amount:
            self.ledger.append(
                {"amount": -amount, "description": "Transfer to {}".format(dest_category.name)})
            self.balance -= amount
            dest_category.deposit(amount, "Transfer from {}".format(self.name))
            return True
        else:
            return False

    def __str__(self):

        star_1 = "*" * int((30-len(self.name))/2)
        star_2 = "*" * (30-len(self.name)-len(star_1))

        string_list = [f"{star_1}{self.name}{star_2}\n",
                       f"Total: {self.balance}"]

        # Now I append to the list the value of each pair in the ledger dictionary,
        # of which I keep only 23 and 7 characters respectively

        for i in range(0, len(self.ledger)):
            string_list.insert(i+1, [list(self.ledger[i].values())[1],
                               "{:.2f}".format(list(self.ledger[i].values())[0])])

        for i in range(1, len(string_list)-1):
            final_string_1 = string_list[i][0][:23]
            final_string_2 = string_list[i][1][-7:]
            length_final_string = len(final_string_1)+len(final_string_2)

            if length_final_string < 30:
                string_list[i] = final_string_1+" " * \
                    (30-length_final_string)+final_string_2+"\n"
            else:
                string_list[i] = final_string_1 + final_string_2 + "\n"

        output = ''
        for item in string_list:
            output = output + item
        return output


def create_spend_chart(categories):

    withdrawals = []
    for cat in categories:
        withdrawals.append([list(cat.ledger[i].values())[0] for i in range(
            0, len(cat.ledger)) if list(cat.ledger[i].values())[0] < 0])

    total_by_category = [sum(expenses) for expenses in withdrawals]
    overall_total = sum(total_by_category)
    percentages = [math.floor(total_by_category[i]/overall_total*10)
                   * 10 for i in range(0, len(total_by_category))]

    strings = ["  0| "]+[" "+str(i*10)+"| " for i in range(1, 10)]+["100| "]

    for i in range(0, len(strings)):
        for j in range(0, len(percentages)):
            if percentages[j] < 10*i:
                strings[i] = strings[i] + " "*3
            else:
                strings[i] = strings[i] + "o" + (" "*2)

    rev_strings = ["Percentage spent by category"] + \
        strings[::-1]+[" "*4+"-"*3*(len(categories))+"-"]
    rev_ind_strings = [rev_strings[i]+"\n" for i in range(0, len(rev_strings))]

    cat_names = [cat.name for cat in categories]
    bottom_length = max([len(name) for name in cat_names])

    name_strings = [" "*5 for i in range(0, bottom_length)]

    for i in range(0, bottom_length):
        for j in range(0, len(cat_names)):
            if j < len(cat_names)-1:
                if i+1 <= len(cat_names[j]):
                    name_strings[i] = name_strings[i] + cat_names[j][i] + " "*2
                else:
                    name_strings[i] = name_strings[i] + " "*3
            else:
                if i+1 <= len(cat_names[j]):
                    name_strings[i] = name_strings[i] + \
                        cat_names[j][i] + " "*2 + "\n"
                else:
                    name_strings[i] = name_strings[i] + " "*3 + "\n"

    all_strings = rev_ind_strings+name_strings

    # I must remove the last \n in order to compy with the project requests.
    result = ''.join(string for string in all_strings)
    result = result[:-1]

    return result
