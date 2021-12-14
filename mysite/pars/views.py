import json
from datetime import datetime
from requests import get
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render


# adress = ('0xc381F21CB49CC30cb0A27e495aB9f0aF95101f79') Ethereum
# adress = ('1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ') BTC
# adress = ('0xdac17f958d2ee523a2206206994597c13d831ec7') USDT
def Coins(request):
    adress = request.GET.get('message')
    print()
    print(adress)
    print()
    coin = request.GET.get('user_coin')
    print(coin)
    if request.GET.get('user_coin') == '1':
        url = "https://chain.so/api/v2/address/BTC/{}".format(adress)
        response = get(url)
        data = json.loads(response.text)
        dicts = []
        if data['status'] == 'success':
            try:
                for i in range(int(data['data']['total_txs'])):
                    time = data['data']['txs'][i]['time']
                    obj = {
                        'number': i + 1,
                        'time': datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'),
                        'fee': data['data']['txs'][i]["incoming"],
                        'confirms': data['data']['txs'][i]['confirmations'],
                        # 'source': data['result'][i]['from'], 'recipient': data['result'][i]['to']
                    }
                    dicts.append(obj)
                    if len(dicts) == 50:
                        pass
            except IndexError:
                pass
            print(len(dicts))

            return JsonResponse({'dicts': dicts})
        else:
            error = 'Неверный адресс'
            print(error)
            return render(request, 'pars/chous.html', {'error': error})

    if request.GET.get('user_coin') == '2':
        url = "https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset=100&sort=desc&apikey=A3IZNWUNSQW4WPWFCGWSCS4QWSB5S24UJQ".format(
            adress)
        response = get(url)
        data = json.loads(response.text)
        dicts = []
        if data['status'] == '1':
            try:
                for i in range(100):
                    time = int(data['result'][i]['timeStamp'])
                    obj = {
                        'number': i + 1,
                        'time': datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'),
                        'fee': data['result'][i]['gasUsed'],
                        'confirms': data['result'][i]['confirmations'],
                        'source': data['result'][i]['from'], 'recipient': data['result'][i]['to']
                    }
                    dicts.append(obj)
                    if len(dicts) == 50:
                        pass
            except IndexError:
                pass
            print(len(dicts))
            return JsonResponse({'dicts': dicts})
        else:
            error = 'Неверный адресс'
            print(error)
            return render(request, 'pars/chous.html', {'error': error})

    if request.GET.get('user_coin') == '3':
        url = "https://api.etherscan.io/api?module=account&action=tokentx&address={}&page=1&offset=100&startblock=0&endblock=27025780&sort=asc&apikey=A3IZNWUNSQW4WPWFCGWSCS4QWSB5S24UJQ".format(
            adress)
        response = get(url)
        data = json.loads(response.text)
        if data['status'] == '1':
            dicts = []
            try:
                for i in range(100):
                    if data['result'][i]['tokenSymbol'] == "USDT":
                        time = int(data['result'][i]['timeStamp'])
                        obj = {
                            'number': i + 1,
                            # 'name': data['result'][i]['tokenName'],
                            'time': datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'),
                            'fee': data['result'][i]['gasUsed'],
                            'confirms': data['result'][i]['confirmations'],
                            'source': data['result'][i]['from'], 'recipient': data['result'][i]['to']}
                        dicts.append(obj)
                    if len(dicts) == 50:
                        pass
            except IndexError:
                pass
            print(len(dicts))
            return JsonResponse({'dicts': dicts})
        else:
            error = 'Неверный адресс'
            print(error)
            return render(request, 'pars/chous.html', {'error': error})

    return render(request, 'pars/chous.html')
