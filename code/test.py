import requests
import json

def get(method="user.get", params={}):
#def get(method="department.get", params={}):
    req = f"https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/{method}"
    #req = f"https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/{method}"
    if params != {}:
        req += "?"
        for parem_key in params.keys():
            req+= f"&{parem_key}={params[parem_key]}"
    response = requests.get(req);
    return response.json()

def get_all(method, params={}):
    response = get(method)
    current = 50
    result = response['result']
    keys = []
    while current < int(response["total"]):
        params["start"] = current
        response = get(method, params);
        curr_result = response["result"]
        for curr_keys in curr_result:
            for k in curr_keys:
                if k not in keys:
                    keys.append(k)
                    print(k)
        result = result + curr_result
        current += 50
    print(keys)
    return result

jsn = get_all('user.get')
print(jsn)
#f = open('department.json', 'w')
#json.dump(jsn, f)
#f.close()