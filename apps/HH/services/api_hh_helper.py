import requests
import stringdist


def suggest_func_reverse(inputstr):
    url = 'https://api.hh.ru/areas/%s' % int(inputstr)
    res = requests.get(url)
    area = res.json()['name']
    return area


def suggest_func(inputstr):
    if len(inputstr) > 2:
        url = 'https://api.hh.ru/suggests/areas/?text=%s'%inputstr
        res = requests.get(url)
        res = res.json()
        if len(res['items']) > 0:
            c = 0
            ccc = 1
            cindex = 0
            for i in res['items']:
                cc = stringdist.levenshtein_norm(i['text'].lower(), inputstr.lower())
                if cc < ccc:
                    ccc = cc
                    cindex = c
                c += 1

            return res['items'][cindex]['id']
        else:
            return '0'
    else:
        return '0'