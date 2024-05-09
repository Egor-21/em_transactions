from datetime import datetime


class Transaction:
    def __init__(self, date, category, amount, description):  # Инициализация транзакции
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def __str__(self):
        return f"Дата: {self.date}\nКатегория: {self.category}\nСумма: {self.amount}\nОписание: {self.description}\n"


def read_transactions(file_path):  # Функция получения транзакций из файла
    transactions = []
    with open(file_path, 'r') as file:
        transaction_info = {}
        for line in file:
            if line.strip():  # Преобразование данных
                key, value = line.strip().split(': ')
                if key == "Дата":
                    key = 'date'
                if key == "Категория":
                    key = 'category'
                if key == "Сумма":
                    key = 'amount'
                    value = float(value)
                if key == "Описание":
                    key = 'description'
                transaction_info[key] = value
            else:
                if transaction_info:
                    transactions.append(Transaction(**transaction_info))
                transaction_info = {}
    return transactions


def write_transactions_to_file(transactions, file_path):  # Функция записи транзакции в файл
    with open(file_path, 'w') as file:
        for transaction in transactions:
            file.write(f"Дата: {transaction.date}\n"
                       f"Категория: {transaction.category}\n"
                       f"Сумма: {transaction.amount}\n"
                       f"Описание: {transaction.description}\n\n")


def get_valid_date():  # Функция для корректного ввода даты
    while True:
        date_inp = input("Введите дату (гггг-мм-дд): ")
        try:
            date = datetime.strptime(date_inp, "%Y-%m-%d")
            return date
        except ValueError:
            print("Некорректный формат даты.")


def get_valid_category():  # Функция для корректного ввода категории
    while True:
        category_inp = input("Введите тип транзакции (0 - Расход, 1 - Доход): ")
        if category_inp in ('0', '1'):
            return "Расход" if category_inp == '0' else "Доход"
        else:
            print("Некорректный ввод. Введите 0 или 1.")


def get_valid_amount():  # Функция для корректного ввода суммы
    while True:
        try:
            amount = float(input("Введите сумму: "))
            return amount
        except ValueError:
            print("Некорректный формат суммы.")


def print_balance(transactions):  # Функция вывода баланса
    income = sum(transaction.amount for transaction in transactions if transaction.category == "Доход")
    consumption = sum(transaction.amount for transaction in transactions if transaction.category == "Расход")
    balance = income - consumption
    print(f"Общий баланс: {balance}\nДоходы: {income}\nРасходы: {consumption}\n")


def add_transaction(transactions):  # Функция добавления новой транзакции
    date = get_valid_date()
    category = get_valid_category()
    amount = get_valid_amount()
    description = input("Введите описание: ")
    transactions.append(Transaction(date, category, amount, description))


def search_transactions(transactions):  # Функция поиска транзакции по определённому критерию
    print("Выберите критерий для поиска:")
    print("1. По дате")
    print("2. По категории")
    print("3. По сумме")
    choice = input("Введите номер критерия: ")
    result = []
    if choice == '1':
        date = get_valid_date()
        result = [transaction for transaction in transactions if transaction.date == date]
    elif choice == '2':
        category = get_valid_category()
        result = [transaction for transaction in transactions if transaction.category == category]
    elif choice == '3':
        amount = get_valid_amount()
        result = [transaction for transaction in transactions if round(transaction.amount, 2) == round(amount, 2)]
    else:
        print("Некорректный выбор.")
    if not result:
        print("Ничего не найдено.")
    else:
        for transaction in result:
            print(transaction)


def edit_transaction(transactions):  # Функция редактирования транзакции по индексу
    index = int(input("Введите индекс записи для редактирования: "))
    index -= 1
    if 0 <= index < len(transactions):
        transaction = transactions[index]
        print(f"Изменение записи: {transaction}")
        print("Введите новые данные:")
        transaction.date = get_valid_date()
        transaction.category = get_valid_category()
        transaction.amount = get_valid_amount()
        transaction.description = input("Введите новое описание: ")
        print("Запись успешно изменена.")
    else:
        print("Некорректный индекс записи.")


def main_menu(transactions):  # Функция отображения главного меню
    while True:
        print("Главное меню:")
        print("1. Показать баланс")
        print("2. Добавить транзакцию")
        print("3. Найти транзакцию")
        print("4. Редактировать транзакцию")
        print("5. Выйти")
        choice = input("Выберите действие: ")
        if choice == '1':
            print_balance(transactions)
        elif choice == '2':
            add_transaction(transactions)
        elif choice == '3':
            search_transactions(transactions)
        elif choice == '4':
            edit_transaction(transactions)
        elif choice == '5':
            break
        else:
            print("Некорректный выбор.")


transactions = read_transactions('transactions.txt')
main_menu(transactions)
write_transactions_to_file(transactions, 'transactions.txt')  # Изменения в транзакциях записываются в файл после завершения программы
