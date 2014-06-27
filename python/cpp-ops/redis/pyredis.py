__author__ = 'samsung'

import redis

r = redis.StrictRedis(host='cache01.stsvc.mscc.cn', port=6379, db=0)
r.set('akey','avalue')



