import simplejson
qs = 'page=1'

page = simplejson.loads(qs.encode())
print(page)