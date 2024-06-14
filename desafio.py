user_db = []
account_db = []

def create_user(user_db, cpf, name, birth_date, address):
    
    cpf = cpf.replace('-', '')
    cpf = cpf.replace('.', '')
    cpf = cpf.replace(' ', '')
       
    for u in user_db:
        if u['cpf'] == cpf:
            print("Usuário já cadastrado")
            return user_db
    new_user = {
            "nome": name,
            "cpf": cpf,
            "nascimento": birth_date,
            "endereco": address
        }
    user_db.append(new_user)
    return user_db

def create_account(logged_user): 
    global account_db   
    account_number = len(account_db) + 1    
    account = {
        "agencia": "0001",
        "numero": account_number,
        "cpf": logged_user["cpf"],
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0,
        "limite_saques": 3,
        "limite_valor": 500.0
    }
    account_db.append(account)
    print(account_db)

def withdraw(account_number, amount):
    current_account = {}
    account_number = int(account_number)
    global account_db
                
    current_account = next((c for c in account_db if c['numero'] == account_number), None)
            
    exceeded_balance = amount > current_account['saldo']
    exceeded_limit = amount > current_account['limite_valor']
    exceeded_withdrawals = current_account['numero_saques'] >= current_account['limite_saques']
        
    if exceeded_balance:
        print("Operação falhou. A sua conta não tem limite suficiente para essa operação")
        
    elif exceeded_limit:
        print("Operação falhou. Valor do saque superior ao limite por saque")
    
    elif exceeded_withdrawals:
        print("Operação falhou. Você excedeu o limite diário de saques ")        
               
    elif amount > 0:
        current_account['saldo'] -= amount
        current_account['extrato'] += f"Saque: R$ {amount:.2f}\n"
        current_account['numero_saques'] += 1        
    
    else:
        print("Operação não concluída. O valor que você tentou depoisitar não é válido.")
        
def deposit(account_number, amount):
    global account_db
    amount = float(amount)   
    for c in account_db:
        if c['numero'] == account_number:
            c['saldo'] += amount
            c['extrato'] += f"Depósito: R$ {amount:.2f}\n"
            print(f"R$ {amount} foi depositado com sucesso")
            return None
    return f"Conta Nº {account_number} não identificada"
                    
def log_in_user(user_db, cpf):
    for u in user_db:
        if u["cpf"] == cpf:
            return u
    return False

def account_menu(user, account):
    pass

def list_user_accounts(user):
    global account_db
    accounts = "=========================="
    for c in account_db:
        if c['cpf'] == user['cpf']:
            accounts += f"\nNº Conta: {c['numero']}\n Saldo: {c['saldo']}\n-------------------------\n"
    if accounts == "==========================":
        print("Usuário sem conta cadastrada")
    else:
        print(accounts)
        
def access_account(account_number):
    account_menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [x] Sair Conta
    => """
    
    account_number = int(account_number)
    
    while True:
        print("=================================================")
        print(f"Conta Nº: {account_number}")
        print("O que deseja fazer?")
        print("=================================================")
        option = input(account_menu)
        
        if option == 'd':
            amount = input(f"Digite o valor que deseja depositar na conta {account_number}: ")
            deposit(account_number, amount)
        elif option == 's':
            amount = float(input("Digite o valor que deseja sacar: R$ "))
            withdraw(account_number, amount)
        elif option == 'e':
            for c in account_db:
                if c['numero'] == account_number:
                    statement = c['extrato']
                    balance = c['saldo']
            
            print("\n================= EXTRATO =================")
            print("Não foram realizadas movimentações na conta." if not statement else statement)
            print(f"\nSaldo: R$ {balance:.2f}")
            print("=============================================")
                                    
        elif option == 'x':
            break 
            
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def user_menu(logged_user):
    user_menu = """
    [l] Listar Contas
    [a] Acessar Conta
    [c] Criar Conta
    [f] Fechar Usuario
    => """
    
    accounts = ""
    global account_db
    
    while True:
        print("=================================================")
        print(f"Seja bem vindo {logged_user['nome']}")
        print("O que deseja fazer?")
        print("=================================================")
        option = input(user_menu)
        
        if option == 'c':
            create_account(logged_user)
        elif option == 'l':
            list_user_accounts(logged_user)
        elif option == 'a':
            account_number = int(input("Digite o número da conta que deseja acessar: "))
            account_exists = False        
            for c in account_db:
                if c['numero'] == account_number:
                    print(logged_user['cpf'])
                    account_exists = True
                    if c['cpf'] == logged_user['cpf']:
                        access_account(account_number)
                    else:
                        print("Essa conta não pertence a esse usuário")
            if not account_exists:
                print("Essa conta não existe")
                
        elif option == 's':
            amount = float(input("Informe o valor do saque: "))
            
            balance, statement = withdraw(balance=balance, amount=amount, statement=statement, limit=limit, number_of_withdrawals=number_of_withdrawals, withdrawal_limit=WITHDRAWAL_LIMIT)
            
        elif option == 'e':
            get_statement(balance, statement=statement)
            
        elif option == 'f':
            break 
            
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    agency_menu = """
    [u] Criar Usuário
    [a] Acessar Usuario
    [q] Sair

    => """

    while True:
        option = input(agency_menu)
        
        if option == "a":
            cpf = input("Informe o CPF do usuário a ser logado: ")
            user = log_in_user(user_db, cpf)
            print(user)
            if user:
                user_menu(user)
            else:
                print("Usuáiro não existe na base.")
        
        elif option == "u":
            name = input("Informe o nome do usuario: ")
            cpf = input("Informe o CPF do usuario: ")
            birth_date = input("Informe a data de nascimento: ")
            address = input("Informe endereço (logadrouro, numero - bairro - cidade/siga estado): ")
            
            user_db = create_user(user_db, cpf, name, birth_date, address)
            print(user_db)
        elif option == 'q':
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
