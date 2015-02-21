import sys
from flask import Flask, request, Response
import ujson as json	#we are using ujson instead of json for performance reasons --> import json
from bid_optimizer import BidOptimizer

load_model = True #for const we don't load ctr prediction model
app = Flask(__name__)
opt = BidOptimizer(load_model)

@app.route('/bidders/const', methods=['POST'])
def const_bidder():
    #if request.headers['Content-Type'] == 'application/json':	#redundant process --> removed for optimization reason
    data = {
        'bid'  : opt.const_bidder()
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

@app.route('/bidders/rand', methods=['POST'])
def rand_bidder():
    data = {
        'bid'  : opt.rand_bidder()
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

@app.route('/bidders/mcpc', methods=['POST'])
def mcpc_bidder():
    data = {
        'bid'  : opt.mcpc_bidder(json.loads(request.data))#(request.json)
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

@app.route('/bidders/lin', methods=['POST'])
def lin_bidder():
    #print request.json
    data = {
        'bid'  : opt.lin_bidder(json.loads(request.data))#(request.json)	#flask seems using standard json for decoding --> for performance reason we use ujson
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)	#set debug flag to False
