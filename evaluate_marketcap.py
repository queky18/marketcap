import numpy as np
import matplotlib.dates as md
import matplotlib.pyplot as plt
import datetime as dt

from requests import get  # to make GET request

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def load_date(csvfile):
    f = open(csvfile, 'r')
    dates = []
    for i, line in enumerate(f):
        if i==0:
            continue
        date = line.split(',')[0].replace('"','')
        datetime_object = dt.datetime.strptime(date, '%m/%d/%Y')
        dates.append(datetime_object)
    return dates
def load_date_bitcoin(csvfile):
    f = open(csvfile, 'r')
    dates = []
    for line in f:
        date = line.split(' ')[0]
        datetime_object = dt.datetime.strptime(date, '%Y-%m-%d')
        dates.append(datetime_object)
    return dates

# download newest data
download('https://etherscan.io/chart/tx?output=csv', 'tx_ethereum')
download('https://etherscan.io/chart/marketcap?output=csv', 'marketcap_ethereum')
download('https://api.blockchain.info/charts/n-transactions?format=csv&timespan=all', 'tx_bitcoin')
download('https://api.blockchain.info/charts/market-cap?format=csv&timespan=all', 'marketcap_bitcoin')
download('https://api.blockchain.info/charts/total-bitcoins?format=csv&timespan=all', 'num_bitcoins')

# load data
###BITCOIN
# num of bitcoins
rawdata = np.genfromtxt('num_bitcoins', delimiter=',')
coins_bitcoin = np.array([float(x) for x in rawdata[:,-1]])
 
# market cap
dates = load_date_bitcoin('marketcap_bitcoin')
datenums_bitcoin=md.date2num(dates)
rawdata = np.genfromtxt('marketcap_bitcoin', delimiter=',')
marketcap_bitcoin = np.array([float(x) for x in rawdata[:,-1]])
marketcap_bitcoin /= coins_bitcoin
# tx
tx_dates= load_date_bitcoin('tx_bitcoin')
tx_datenums_bitcoin=md.date2num(tx_dates)

rawdata = np.genfromtxt('tx_bitcoin', delimiter=',')
tx_bitcoin = rawdata[:,-1]

###ETHEREUM
# market cap
dates = load_date('marketcap_ethereum')
datenums_ethereum = md.date2num(dates)
rawdata = np.genfromtxt('marketcap_ethereum', delimiter='","', skip_header=1)
num_coins = np.array([float(x) for x in rawdata[:,2]])
marketcap = np.array([float(x)*1e6 for x in rawdata[:,3]]) 
marketcap /= num_coins

# tx
f = open('tx_ethereum', 'r')
tx = []
for i, line in enumerate(f):
    if i == 0:
        continue
    tx.append(float(line.replace('"', '').split(',')[2]))
tx=np.array(tx)
f.close()
rawdata = np.genfromtxt('tx_ethereum', delimiter='","', skip_header=1)
tx_dates= load_date('tx_ethereum')
tx_datenums=md.date2num(tx_dates)



# PLOT DATA
fig = plt.figure(figsize=(10,6))
ax_ethereum = fig.add_subplot(211)
ax_bitcoin = fig.add_subplot(212)

ax_ethereum.plot(datenums_ethereum, marketcap, label='Ether Price')
ax_ethereum.plot(tx_datenums, 100*tx**(3/2)/num_coins, label='T(# transaction)')

ax_bitcoin.plot(datenums_bitcoin, marketcap_bitcoin, label='Bitcoin Price')
ax_bitcoin.plot(tx_datenums_bitcoin, 100*tx_bitcoin**(3/2)/coins_bitcoin, label='T(# transaction)')


first_date = datenums_ethereum[-800]
last_date = datenums_ethereum[-1]+20
xfmt = md.DateFormatter('%d/%m/%Y')
# xfmt = md.DateFormatter('%m/%Y')
ax_ethereum.get_xaxis().set_major_formatter(xfmt)
ax_ethereum.set_xlabel('$Time$')
ax_ethereum.set_ylabel('$Price \,/\, \$ $')
ax_ethereum.set_yscale('log')
ax_ethereum.grid(b=True, which='major', ls='-')
ax_ethereum.grid(b=True, which='minor', ls='--')
ax_ethereum.set_xlim([first_date, last_date])
ax_ethereum.set_ylim([.5, None])
ax_ethereum.legend(loc='best').draw_frame(True)

ax_bitcoin.get_xaxis().set_major_formatter(xfmt)
ax_bitcoin.set_xlabel('$Time$')
ax_bitcoin.set_ylabel('$Price \,/\, \$ $')
ax_bitcoin.set_yscale('log')
ax_bitcoin.grid(b=True, which='major', ls='-')
ax_bitcoin.grid(b=True, which='minor', ls='--')
ax_bitcoin.set_xlim([first_date, last_date])
ax_bitcoin.set_ylim([100, None])
ax_bitcoin.legend(loc='best').draw_frame(True)

fig.tight_layout()
fig.savefig('Marketcap.png')
plt.show()