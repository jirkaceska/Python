n = ['3','3','8','8']
s = ['+', '-', '*', '/', '(', ')']

def search(n, s, r):
    try:
        if eval(r) == 24 and len(n) == 0:
            print(r)
    except:
        pass
    for i in range(len(n)):
        tmp = r
        tmp += n[i]
        res = search(n[:i] + n[(i+1):], s, tmp)
#        if (eval(res) == 24):
#            return res
    for j in range(len(s)):
        tmp = r
        tmp += s[j]
        res = search(n, s[:j] + s[(j+1):], tmp)
#        if (eval(res) == 24):
#            return res

#print(eval('//**'))
print(search(n, s, ''))
    
