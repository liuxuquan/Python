import redis
#r = redis.Redis(host='10.25.174.198',port=6379)
#r.set('name','KillerMan')
#print r.get('name')
pool = redis.ConnectionPool(host='10.25.174.198',port=6379)

r = redis.Redis(connection_pool=pool)

r.set('age', '16')

print(r.get('age'))
