from pymongo import MongoClient
import parser, feature, encoder, sys, json
from ml_models import Model
from bid_optimizer import BidOptimizer

json_payload = '{"id" : "572fa35095e8b6c30b1aa871e52b2d", "imp" : [ { "id" : "1", "banner" : { "w" : 336, "h" : 280, "wmax" : null, "hmax" : null, "wmin" : null, "hmin" : null, "id" : null, "pos" : 0, "btype" : [ ], "battr" : [ 9, 1, 2, 14018, 14014, 3, 5, 14, 13, 14005, 10, 14015, 8, 14019 ], "mimes" : [ ], "topframe" : 0, "expdir" : [ ], "api" : [ ], "ext" : {  } }, "video" : null, "displaymanager" : null, "displaymanagerver" : null, "instl" : 0, "tagid" : "70821", "bidfloor" : 0, "bidfloorcur" : "USD", "secure" : 0, "iframebuster" : [ ], "pmp" : null, "ext" : {  } } ], "site" : { "id" : "15756", "name" : "Zoopla", "domain" : "trqRTJjrXqf7FmMs", "cat" : [ "IAB21" ], "sectioncat" : [ ], "pagecat" : [ ], "page" : "23510110004d0dcb593e2e3c1fc46e28", "privacypolicy" : 0, "ref" : null, "search" : null, "publisher" : { "id" : "9208", "name" : null, "cat" : [ ], "domain" : null, "ext" : {  } }, "keywords" : null, "ext" : {  } }, "app" : null, "device" : { "dnt" : 0, "ua" : "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.12 (KHTML, like Gecko) Maxthon/3.0 Chrome/18.0.966.0 Safari/535.12", "ip" : "120.40.95.*", "geo" : { "lat" : null, "lon" : null, "country" : "CN", "region" : "124", "regionfips104" : null, "metro" : null, "city" : "125", "zip" : null, "type" : null, "ext" : {  } }, "didsha1" : null, "didmd5" : null, "dpidsha1" : null, "dpidmd5" : null, "macsha1" : null, "macmd5" : null, "ipv6" : null, "carrier" : null, "language" : "en", "make" : null, "model" : null, "os" : null, "osv" : null, "js" : 1, "connectiontype" : 0, "devicetype" : 2, "flashver" : null, "ifa" : null, "ext" : {  } }, "user" : { "id" : "64c017a3d756e2566596cc1499294d1b602c88a3", "buyeruid" : "7be2ed3d-a245-4045-af05-f15c9771a73e", "yob" : null, "gender" : null, "keywords" : null, "customdata" : null, "geo" : null, "data" : [ ], "ext" : { "sessiondepth" : 5 } }, "at" : 2, "tmax" : 129, "wseat" : [ ], "allimps" : null, "cur" : [ ], "bcat" : [ ], "badv" : [ ], "regs" : null, "ext" : { "format" : "1", "tags" : "10031,13042,10110", "ts" : "20130606000105075", "pp" : 87, "conv" : 0, "clk" : 0, "visibility" : "0", "adexchangeid" : "1", "bp" : 300 }, "pmp" : null }'

def build_model():
    #get data from mongo
    client = MongoClient('localhost', 27017)
    db = client.rtb
    bid_requests = db.bid_requests
    cnt = 0
    features = []
    enc = encoder.Encoder()
    #exctact features
    for req in bid_requests.find():
        data = parser.parse(req)
        #print data
        fets = feature.extract_features(data)
        #print fets
        features.append(fets)
        cnt += 1
        #if cnt > 10:
        #    break
    #create training data
    X, Y = feature.generate_training_data(features, "train.csv", enc)
    print len(X)
    print len(Y)
    #build/serialize model
    model = Model()
    model.build_lr_model(X, Y)   #train lr model
    #save model
    model.save_model()
    #test bid optimizer as api call flow
    payload = json.loads(json_payload)
    res = model.predict(payload)
    print res
    opt = BidOptimizer()
    print "const=", opt.const_bidder()
    print "rand=", opt.rand_bidder()
    print "mcpc=", opt.mcpc_bidder(payload)
    print "lin=", opt.lin_bidder(payload)

if __name__ == "__main__":
    build_model()
