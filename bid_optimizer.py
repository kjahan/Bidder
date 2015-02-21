from ml_models import Model
import random as rand

class BidOptimizer:
    def __init__(self, load_model):
        #we have computed the following numbers based on training data for 1458
        #we need to do the same thing for future campaigns
        avg_cpm = 69.0 #average cpm computed from history data --> this can be updated with new data
        max_bid = 300#4*cpm #we should study pp distribution and look at bounds
        three_day_volume = 600000.  #no of impressions that we can potentially buy at max_bid price
        three_days_budget = three_day_volume*avg_cpm/1000.0
        budgets = [45165.243/2.0, 45165.243/8.0, 45165.243/32.0]
        budg_denoms = ["1/2", "1/8", "1/32"]
        budget = budgets[1]
        train_cost = 212400.    #total cost for adv 1458 from history data
        train_clks = 2454.      #total clks for adv 1458 from history data
        max_eCPC = train_cost/train_clks
        avg_CTR = 0.08*0.01 #computed from history data --> this can be updated over time
        base_bid = max_bid*avg_CTR
        bid_val = avg_cpm + budget*(max_bid - avg_cpm)/(three_days_budget)  #dynamic bid value computed for conts and rand algs
        const_bid = bid_val
        self.budget = budget
        self.const_bid_val = const_bid  #const bidder parameter
        self.max_bid_val = max_bid      #random bidder parameter
        self.max_eCPC = max_eCPC        #Mcpc bidder parameter
        self.base_bid = base_bid 
        self.avg_CTR = avg_CTR
        self.model = None
        if load_model:
            #load ml model once for predicting ctr
            self.model = Model()
            self.model.load_model()

    #const bidder
    def const_bidder(self):
        return self.const_bid_val
    
    #random bidder
    def rand_bidder(self):
        #random bid strategy
        return rand.randint(1, self.max_bid_val)

    #Mcpc bid strategy
    def mcpc_bidder(self, payload):
        #res = {"y": y, "prob": prob[0][1], "y_pred": y_pred, "pp": pp} #store label and pr(y=1)
        res = self.model.predict(payload)   #let's compute pCTR
        #y_pred= res["y_pred"]
        #p_ctr = res["prob"] #probability of click
        #Mcpc bid strategy
        return res["prob"]*self.max_eCPC    #bid value is multiplication of pCTR and max of expected eCPC from training data

    #Lin bid strategy
    def lin_bidder(self, payload):
        #res = {"y": y, "prob": prob[0][1], "y_pred": y_pred, "pp": pp} #store label and pr(y=1)
        res = self.model.predict(payload)   #let's compute pCTR
        #y_pred= res["y_pred"]
        #p_ctr = res["prob"] #probability of click
        #Lin bid strategy
        return self.base_bid*(res["prob"]/self.avg_CTR)    #our bid is pCTR/avgCTR multiplied by base_bid
