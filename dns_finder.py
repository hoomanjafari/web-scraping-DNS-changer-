import requests
import re
import bs4
import tkinter as tk
from tkinter import messagebox
import os
import win32com.shell.shell as shell
import re
from itertools import zip_longest  # use zip, buit-in, if even list
import random

window = tk.Tk()
window.geometry('400x320')
window.resizable(False, False)
window.title('Dns finder')

# to get user current dns addresses
my_dns = os.popen('ipconfig /all').read()
preferred_dns = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', my_dns)[4]
alternate_dns = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', my_dns)[5]
# to show the current dns as label
current_dns_text = f"You'r current DNS \n \n Preferred DNS {preferred_dns} \n Alternate DNS {alternate_dns}"
current_dns = tk.Label(
    master=window, text=current_dns_text,  bg='white', font=('Courier bold', 15), justify='left', padx=33, pady=33, width=28
)
current_dns.pack(anchor="w", padx=22, pady=22)


def read_file():  # to read the proxies from database
    with open('proxies.txt', 'r') as f:
        r = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', f.read())

        def sort_proxy(x):  # to separate proxies two by two as preferred and alternate
            for first, second in zip_longest(x[::2], x[1::2]):
                yield first, second

        proxy_list = [pair for pair in sort_proxy(r)]
    return proxy_list
# print(read_file())


repeated_dns = []


def set_dns():
    global preferred_dns
    global alternate_dns
    global current_dns_text
    rand_int = int(random.random() * len(read_file()))
    get_dns = read_file()[rand_int]
    if get_dns not in repeated_dns:
        repeated_dns.append(get_dns)
        # shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + f'netsh interface ip set dns name="Ethernet" source="static" address="{get_dns[0]}" & netsh interface ip add dns name="Ethernet" addr="{get_dns[1]}" index=2' )
        print('dns has been changed', f'repeated list is :', repeated_dns)
        preferred_dns = get_dns[0]
        alternate_dns = get_dns[1]
        dns_text = f"You'r DNS changed to \n \n Preferred DNS {preferred_dns} \n Alternate DNS {alternate_dns}"
        current_dns.config(text=dns_text)
    else:
        if len(repeated_dns) != len(read_file()):
            set_dns()
            print('dns was repeated')
        else:
            print('all dns addresses has been selected')





# loading animation functions
def start_loading():
    pass


def stop_loading():
    pass






def save_proxy():  # to request to the specific website for getting the proxy addresses
    r = requests.get(
        'https://spaceiran.com/blog/best-iranian-dns-proxy-list').text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    code_list = []
    proxies = []
    code = soup.find_all("code")
    for c in code:
        code_list.append(c.get_text())

    for t in code_list:
        proxies.append(re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', t))
    with open('proxies.txt', 'w') as f:
        for proxy in proxies:
            f.write(
                'preferred dns :' + proxy[0] + '\n' +
                'alternate dns :' + proxy[1] + '\n' + '\n'
            )
    messagebox.showinfo("Message", "You'r DNS list has been updated")


# dns change button
tk_btn = tk.Button(text='Change DNS', font=('bold', 14), bg='#00e1a7',
                   relief='solid', command=set_dns).pack(padx=22, anchor='center')
# get new dns addresses button
update_btn = tk.Button(text='Update my DNS list', bg='#00bfe1', relief='solid', font=('bold', 12), command=save_proxy).pack(padx=22, pady=10, anchor='center')

window.mainloop()




