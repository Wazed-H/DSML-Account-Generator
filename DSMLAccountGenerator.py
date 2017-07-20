import requests
import json
import bs4
from time import sleep, strftime


def gmail_dot_gen(username, number):
    emails = list()
    username_length = len(username)
    padding = "{0:0" + str(username_length - 1) + "b}"
    for i in range(0, number):
        bin = padding.format(i)
        full_email = ""

        for j in range(0, username_length - 1):
            full_email += (username[j]);
            if bin[j] == "1":
                full_email += "."
        full_email += (username[j + 1])
        emails.append(full_email + "@gmail.com")
    return emails


def register(email):
    print(strftime("[%H:%M:%S]: "), "Creating Account with", email)

    r = requests.Session()
    r.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.66 Safari/537.36'
    })

    form_url = "https://shop.doverstreetmarket.com/customer/account/create/"
    reg_url = "https://shop.doverstreetmarket.com/customer/account/createpost/"

    config_file = open('config.json', 'r')
    config = json.load(config_file)
    config_file.close()

    error = []
    success = []
    form = r.get(form_url).text
    form_soup = bs4._soup(form, 'html.parser')
    for i in form_soup.find_all('input', {'name': 'form_key'}):
        form_key = i['value']

    form_data = {
        'form_key': str(form_key),
        'firstname': config['firstName'],
        'lastname': config['lastName'],
        'email': email,
        'password': config['password'],
        'confirmation': config['password'],
        'is_subscribed': '0'
    }

    x = bs4._soup(r.post(reg_url, data=form_data).text,'html.parser')

    for i in x.find_all('li', {'class': 'error-msg'}):
        error.append(str(i.string))
    for i in x.find_all('li', {'class': 'success-msg'}):
        success.append(str(i.string))

    print(strftime("[%H:%M:%S]: "), "Created Account with", email)
    return str(email+":"+config['password'])


if __name__ == "__main__":
    conf_file = open('config.json', 'r')
    conf = json.load(conf_file)
    conf_file.close()

    prefix = conf['gmailPrefix']

    no = int(input("How many accounts would you like?: "))
    combos = gmail_dot_gen(prefix, no)
    combos.append((str(prefix+"@gmail.com")))
    accounts = []

    for each in combos:
        account = register(each)
        accounts.append(account)
        sleep(5)
    f = open('accounts.txt', 'w')
    for each in accounts:
        f.write("%s\n" % each)