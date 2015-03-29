from ml_models import Model
import random as rand
import parser

class BidOptimizer:
    def __init__(self, load_ml_model):
        self.load_campaign_parameters()
        self.ml_model = None
        if load_ml_model:
            #load ml model once for predicting ctr
            self.ml_model = Model()
            self.ml_model.load_lr_model()

    def load_campaign_parameters(self):
        self.total_budget = 5000.0  #campaign total budget in USD
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
        
    #const bidder
    def const_bidder(self, payload):
        data = parser.parse(payload) #parse payload
        self.const_bid_val = data["bidfloor"] + 0.01   #bid 1 cents above bid floor
        if self.const_bid_val < data["bidfloor"]:
            return None #Do Not bid
        return self.const_bid_val
    
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
