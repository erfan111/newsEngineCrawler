def normalize(string):
    r = string
    s = r.find('<')
    while s != -1:
        f = r.find('>', s + 1)
        r = r[:s] + ' ' + r[f + 1:]
        s = r.find('<', f + 1)

    return r
