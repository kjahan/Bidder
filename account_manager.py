import redis

#part of bidding model is stored in Redis - connect to redis db
redis_db = redis.Redis(host='localhost', port=6379, db=0)

DEBUG = False
#thus method periodically goes through resid all submitted bids
#and cleanup those bids we haven't receeived any win notice
#it updates totalspend accordingly
def update_total_spend_periodically():
    r = redis.StrictRedis()
    pubsub = r.pubsub()
    pubsub.psubscribe("__keyevent@0__:expired")
    for msg in pubsub.listen():
        try:
            if DEBUG:
                print msg
            shadow_key = msg['data']
            bid_id = shadow_key.split(':')[1]   #get bid id
            adj = -1.0*float(r.get(bid_id)) #get bid val
            if DEBUG:
                print bid_id, adj
            if adj < 0:
                r.incrbyfloat("totalspend", adj)    #key is expired so return bid val to total budget
            r.delete(bid_id)    #delete bid id
        except:
            pass

#this method is call by win end point for adjusting totalspend
def adjust_total_spend(bid_id, bid_val):
    try:
        paid = float(bid_val)/1000.0    #cpm pricing model
        adj = -1.0*(float(redis_db.get(bid_id)) - paid)
        if DEBUG:
            print "adjust bid for ", bid_id, " by ", adj
        if adj < 0:
            redis_db.incrbyfloat("totalspend", adj)    #key is expired so return bid val to total budget
        redis_db.delete(bid_id)    #delete bid id
    except:
        pass

if __name__ == '__main__':
    update_total_spend_periodically()
