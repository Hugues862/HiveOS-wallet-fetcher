import json, os, requests, time
from connector import *


# DATA VARIABLES
token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkiLCJpYXQiOjE2MTI0MjQ1NzgsImV4cCI6MTkyNzc4NDU3OCwibmJmIjoxNjEyNDI0NTc4LCJqdGkiOjI0OTMzMzUzLCJzdWIiOjI0OTMzMzUzfQ.AQ87NYJ7sl3B_7YWB20Pos0xDBxfUW3bWdqDft8FNgE"
farm_id="355390"


local = False


class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():

    cHive = connect_api()

    # Displays Wallet and converts in EUR and USD
    getWallets(cHive)
    # Displays GPU info
    getGPU(cHive)


def getFarmsJSON(cHive):
    data = ""
    if local:
        with open("file", 'r') as f:
            data = f.read()
    else:
        res = cHive.get_workers(farm_id)
        json_str = json.dumps(res)
        with open("file", 'w') as f:
            f.write(json_str)
        data = res
    return data


def getWallets(cHive):
    print()
    try:
        clear()
        wallets = cHive.get_wallets(farm_id)

        wallets = wallets["data"]

        for i in range(1, len(wallets)):
            wallet_bal_crypto = False
            wallet_bal_fiat = False
            pool = False
            pool_bal_crypto = False
            pool_bal_fiat = False

            name = wallets[i]["name"]
            print(name)
            if "balance" in wallets[i]:
                wallet_bal_crypto = wallets[i]["balance"]['value']
                wallet_bal_fiat = wallets[i]['balance']['value_fiat']

            if "pool_balances" in wallets[i]:
                for j in range(0, len(wallets[i]["pool_balances"])):
                    pool = wallets[i]["pool_balances"][j]['pool']
                    pool_bal_crypto = wallets[i]["pool_balances"][j]['value']
                    pool_bal_fiat = wallets[i]['pool_balances'][j]['value_fiat']

            pwcrypto, pwfiatusd, pwfiateur, ppool, ppcrypto, ppfiatusd, ppfiateur = 0, 0, 0, 0, 0, 0, 0
            try:
                pwcrypto = wallet_bal_crypto
            except:
                pass
            try:
                pwfiatusd = wallet_bal_fiat
            except:
                pass
            try:
                pwfiateur = ETHconvert(wallet_bal_crypto, 'EUR')
            except:
                pass
            try:
                ppool = pool
            except:
                pass
            try:
                ppcrypto = pool_bal_crypto
            except:
                pass
            try:
                ppfiatusd = pool_bal_fiat
            except:
                pass
            try:
                ppfiateur = ETHconvert(pool_bal_crypto, 'EUR')
            except:
                pass
            totalusd = ETHconvert(pwcrypto+ppcrypto, "USD")
            totaleur = ETHconvert(pwcrypto+ppcrypto, "EUR")
            totalcrypto = pwcrypto+ppcrypto

            print(
                f"{fg.lightred}WALLET {fg.ENDC}| {fg.cyan}{pwcrypto} ETH{fg.ENDC} | {fg.orange}{pwfiatusd} ${fg.ENDC} | {fg.green}{pwfiateur} €{fg.ENDC}")
            print(
                f"{fg.lightblue}{ppool} {fg.ENDC}| {fg.cyan}{ppcrypto} ETH{fg.ENDC} | {fg.orange}{ppfiatusd} $ {fg.ENDC}| {fg.green}{ppfiateur} €{fg.ENDC}")
            print(
                f"{fg.pink}Total{fg.ENDC} | {fg.lightcyan}{totalcrypto} ETH {fg.ENDC}| {fg.orange}{totalusd} $ {fg.ENDC}| {fg.lightgreen}{totaleur} €{fg.ENDC}")
            print("---------------------------------------")
        
        print(f"ETH PRICE : {fg.pink}{ETHconvert(1, 'USD')} ${fg.ENDC}")
        
    except Exception as e:
        print(f'Fetching Data | Status : {fg.red}{e}{fg.ENDC}')
        time.sleep(5)
    print()


def getGPU(cHive):
    farms = getFarmsJSON(cHive)
    gpus = farms["data"][0]

    for i in range(0, len(gpus["gpu_stats"])):
        mhs = round(gpus["gpu_stats"][i]['hash']*0.001, 2)
        power = gpus["gpu_stats"][i]['power']
        fan = gpus["gpu_stats"][i]['fan']
        temp = gpus["gpu_stats"][i]['temp']

        print(f'{fg.red}{gpus["gpu_summary"]["gpus"][i]["name"]}{fg.ENDC}')
        print(" " + str(mhs) + " Mh/s | " +
              str(power) + " W | " + str(fan) + "%")
        print(" " + str(round((mhs/power), 4)) + "Mh/W | " + str(temp) + "°C")
        print("-------------------------")


def connect_api():
    return Hive(token)


def ETHconvert(val, curr):
    res = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=EUR,USD')
    if curr == "EUR":
        ethrate = res.json()['EUR']
    elif curr == "USD":
        ethrate = res.json()['USD']

    return round(ethrate*val, 2)


def clear():
    os.system("clear")


""" if __name__ == '__main__':
    main()
 """
