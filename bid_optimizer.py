from ml_models import Model
import random as rand, parser, redis

class BidOptimizer:
    def __init__(self, load_ml_model):
        self.load_campaign_parameters()
        self.ml_model = None
        if load_ml_model:
            #load ml model once for predicting ctr
            self.ml_model = Model()
            self.ml_model.load_lr_model()
        #part of bidding model is stored in Redis - connect to redis db
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def load_campaign_parameters(self):
        self.total_budget = 100.0  #campaign total budget in USD --> this should be moved to a config file
        self.nurl_ttl = 1800    #how long keep bidid in redis for account updating --> set 1800 secs (from mopub 10-15mins)
        campaign_length = 30.0
        self.daily_budget = self.total_budget/campaign_length   #daily budget
        self.user_freq_cap = 1  #frequency cap for Impression Per User
        self.app_placement_freq_cap = 10    #Freq Cap per App Placement --> optimize the parameter
        self.placement_cats = []    #whitelist or blacklist apps categories
        self.placements = []    #whitelist or blacklist placements by name
        #we have computed the following numbers based on training data for 1458
        #we need to do the same thing for future campaigns
        avg_cpm = 69.0 #average cpm computed from history data --> this can be updated with new data
        max_bid = 300#4*cpm #we should study pp distribution and look at bounds
        three_day_volume = 600000.  #no of impressions that we can potentially buy at max_bid price
        three_days_budget = three_day_volume*avg_cpm/1000.0
        train_cost = 212400.    #total cost for adv 1458 from history data
        train_clks = 2454.      #total clks for adv 1458 from history data
        max_eCPC = train_cost/train_clks
        avg_CTR = 0.08*0.01 #computed from history data --> this can be updated over time
        base_bid = max_bid*avg_CTR
        bid_val = avg_cpm + self.total_budget*(max_bid - avg_cpm)/(three_days_budget)  #dynamic bid value computed for conts and rand algs
        self.const_bid_val = bid_val  #const bidder parameter
        self.max_bid_val = max_bid      #random bidder parameter
        self.max_eCPC = max_eCPC        #Mcpc bidder parameter
        self.base_bid = base_bid 
        self.avg_CTR = avg_CTR

    #basic const bidder
    def const_bidder(self, payload):
        data = parser.parse(payload)    #parse bid req payload
        bid = data["bidfloor"] + 0.01   #bid 1 cent above the bid floor
        bid_val = bid/1000.0  #cpm pricing model
        currentspend = float(self.redis.get("totalspend"))
        #if bid < data["bidfloor"]:
        #    return None #Do Not bid
        if not data["idfa"]:
            return None #Do Not bid as there is no idfa signal to o user capping
        user_id = "user:" + data["idfa"]    #user key for redis freq capping
        user_freq = 0   #if we haven't served any ad for this user, set user freq to zero by default
        try:
            user_feq = int(self.redis.get(user_id))
        except:
            pass
        if bid_val + currentspend < self.total_budget:
            totalspend = float(self.redis.incrbyfloat("totalspend", bid_val))  #hard cap to be conservative --> we should cast as float because all numbers are calculated as float type!
            #R1: make sure total spend is under total campaign budget
            if totalspend > self.total_budget:
                #we have passed campaign total budget --> rollback & send nobid
                self.redis.decr("totalspend", bid_val)
                return None #Do Not bid
            #we havent passed total budget so add corresponding states to redis for budget management
            #we should store this transaction into redis
            if user_freq < self.user_freq_cap:
                new_freq = int(self.redis.incr(user_id)) #incr freq for the user
                if new_freq > self.user_freq_cap:
                    self.redis.decr(user_id)    #we passed freq capp for this user --> go back
                    return None #no bid
            else:
                #we passed freq capp for this user --> no bid
                return None #Do Not bid for this user
            self.redis.set(data["id"], bid_val)  #let's store bid id along with bid val for later accounting
            shadow_key = "shadow:" + data["idfa"] + ":" + data["id"]    #shadow key is concat of shadow:user_id:bid_id
            self.redis.setex(shadow_key, "", self.nurl_ttl) 
        else:
            #we have passed campaign total budget --> send nobid
            return None #Do Not bid
        return bid
    
    #random bidder
    def rand_bidder(self):
        #random bid strategy
        return rand.randint(1, self.max_bid_val)

    #Mcpc bid strategy
    def mcpc_bidder(self, payload):
        #res = {"y": y, "prob": prob[0][1], "y_pred": y_pred, "pp": pp} #store label and pr(y=1)
        res = self.ml_model.predict(payload)   #let's compute pCTR
        #y_pred= res["y_pred"]
        #p_ctr = res["prob"] #probability of click
        #Mcpc bid strategy
        return res["prob"]*self.max_eCPC    #bid value is multiplication of pCTR and max of expected eCPC from training data

    #Lin bid strategy
    def lin_bidder(self, payload):
        #res = {"y": y, "prob": prob[0][1], "y_pred": y_pred, "pp": pp} #store label and pr(y=1)
        res = self.ml_model.predict(payload)   #let's compute pCTR
        #y_pred= res["y_pred"]
        #p_ctr = res["prob"] #probability of click
        #Lin bid strategy
        return self.base_bid*(res["prob"]/self.avg_CTR)    #our bid is pCTR/avgCTR multiplied by base_bid
