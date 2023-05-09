import requests
import secrets
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_email(email: str) -> bool:
    data = {
        'email': email,
        'request_id': 'adguard-website-api',
    }
    response = requests.post('https://auth.adguard.app/api/2.0/user_lookup', data=data)
    return response.json()['can_register']

def get_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
    return response.json()[0]

def register(email, password):
    data = {
        'email': email,
        'password': password,
        'source': 'ACCOUNT',
        'clientId': 'adguard-website-api',
        'applicationId': 'adguard-website-api',
        'marketingConsent': 'false',
        'product': 'ADBLOCK',
        'webmasterId': '32361',
    }
    response = requests.post('https://auth.adguard.app/api/2.0/registration', data=data)
    if response.json() == {}:
        return True
    return response.json()

def generate_password():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10))

def register_account(i):
    email = get_email()
    if check_email(email):
        password = STATIC_PASSWORD if STATIC_PASSWORD else generate_password()
        reg = register(email, password)
        if reg:
            print(f'Успешно зарегистрировал аккаунт!\nЛогин: {email}\nПароль: {password}')
            print('--------------------------------')
        else:
            print(f'Проблема с регистрацией!\nЛогин: {email}\nПароль: {password}')
            print(reg)
            print('--------------------------------')

def main():
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(register_account, i) for i in range(accounts_count)]
        for future in as_completed(futures):
            future.result()

def register_account(i):
    email = get_email()
    if check_email(email):
        password = STATIC_PASSWORD if STATIC_PASSWORD else generate_password()
        reg = register(email, password)
        if reg:
            print(f'Успешно зарегистрировал аккаунт!\nЛогин: {email}\nПароль: {password}')
            with open('accounts.txt', 'a') as f:
                f.write(f'{email}:{password}\n')
        else:
            print(f'Проблема с регистрацией!\nЛогин: {email}\nПароль: {password}')
            print(reg)
        print('--------------------------------')

if __name__ == '__main__':
    STATIC_PASSWORD = input('Введи пароль для всех аккаунтов (не короче 8 символов)\n-> ')
    accounts_count = int(input('Сколько аккаунтов зарегистрировать:\n-> '))
    main()