import redis

#part of bidding model is stored in Redis - connect to redis db
redis_db = redis.Redis(host='localhost', port=6379, db=0)

DEBUG = False
#this method periodically goes through resid all submitted bids
#and cleanup those bids we haven't receeived any win notice
#it updates totalspend and freqs for users accordingly
def update_total_spend_periodically():
    r = redis.StrictRedis()
    pubsub = r.pubsub()
    pubsub.psubscribe('__keyevent@0__:expired')
    for msg in pubsub.listen():
        try:
            if DEBUG:
                print msg
            shadow_key = msg['data']
            items = shadow_key.split(':')
            user_id = "user" + ":" + items[1]  #get user id
            bid_id = items[2]   #get bid id
            #let's check if bid_id is in redis --> if not, this means that we have received win before shadow key expires
            bid_val = r.get(bid_id) #get bid we submited for this bid id from redis
            if bid_val is not None:
                #if we come here it means that we haven't received won signal for this shadow key
                adj = -1.0*float(bid_val) #get bid val
                if DEBUG:
                    print bid_id, adj
                if adj < 0:
                    r.incrbyfloat("totalspend", adj)    #key is expired so return bid val to total budget
                r.delete(bid_id)    #delete bid id
                r.decr(user_id) #we didnt win so decrease freq for this user st we can bid later for her/him
        except:
            pass

#this method is called by win end point for adjusting totalspend
def adjust_total_spend(bid_id, bid_val):
    try:
        redis_db.incr("wins")   #inrease wins st at the end of test we know how many wins we had
        paid = float(bid_val)/1000.0    #cpm pricing model
        adj = -1.0*(float(redis_db.get(bid_id)) - paid)
        if DEBUG:
            print "adjust bid for ", bid_id, " by ", adj
        if adj < 0:
            redis_db.incrbyfloat("totalspend", adj)    #adjust total spend based on how much exchange charged us
        redis_db.delete(bid_id)    #delete bid id
    except:
        pass

if __name__ == '__main__':
    update_total_spend_periodically()
