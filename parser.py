#grab json and extract all low level mopub signals
def parse(bid_req):
    data = {}
    #top level attributes
    try:
        data["id"] = bid_req["id"]  #bid id
    except:
        data["id"] = None
    try:
        data["at"] = bid_req["at"]
    except:
        data["at"] = None
    try:
        data["badv"] = bid_req["badv"]
    except:
        data["badv"] = None
    try:
        data["bcat"] = bid_req["bcat"]
    except:
        data["bcat"] = None
    #device attributes
    try:
        data["carrier"] = bid_req["device"]["carrier"]   #carrier name
    except:
        data["carrier"] = None
    try:
        data["connectiontype"] = bid_req["device"]["connectiontype"]    #conntype
    except:
        data["connectiontype"] = None
    try:
        data["devicetype"] = bid_req["device"]["devicetype"]    #dev type
    except:
        data["devicetype"] = None
    try:
        data["dnt"] = bid_req["device"]["dnt"]
    except:
        data["dnt"] = None
    try:
        data["dpidmd5"] = bid_req["device"]["dpidmd5"]
    except:
        data["dpidmd5"] = None
    try:
        data["dpidsha1"] = bid_req["device"]["dpidsha1"]
    except:
        data["dpidsha1"] = None
    try:
        data["lat"] = bid_req["device"]["geo"]["lat"]
    except:
        data["lat"] = None
    try:
        data["lon"] = bid_req["device"]["geo"]["lon"]
    except:
        data["lon"] = None
    try:
        data["city"] = bid_req["device"]["geo"]["city"] #city
    except:
        data["city"] = None
    try:
        data["country"] = bid_req["device"]["geo"]["country"]#country
    except:
        data["country"] = none
    try:
        data["region"] = bid_req["device"]["geo"]["region"] #region
    except:
        data["region"] = None
    try:
        data["zip"] = bid_req["device"]["geo"]["zip"]
    except:
        data["zip"] = None
    try:
        data["geotype"] = bid_req["device"]["geo"]["type"]
    except:
        data["geotype"] = None
    try:
        data["ip"] = bid_req["device"]["ip"]
    except:
        data["ip"] = None
    try:
        data["js"] = bid_req["device"]["js"]
    except:
        data["js"] = None
    try:
        data["language"] = bid_req["device"]["language"]
    except:
        data["language"] = None
    try:
        data["make"] = bid_req["device"]["make"]
    except:
        data["make"] = None
    try:
        data["model"] = bid_req["device"]["model"]
    except:
        data["model"] = None
    try:
        data["os"] = bid_req["device"]["os"]
    except:
        data["os"] = None
    try:
        data["osv"] = bid_req["device"]["osv"]
    except:
        data["osv"] = None
    try:
        data["ua"] = bid_req["device"]["ua"]    #user agent
    except:
        data["ua"] = None
    try:
        data["idfa"] = bid_req["device"]["ext"]["idfa"]
    except:
        data["idfa"] = None
    #app features
    try:
        data["appbundle"] = bid_req["app"]["bundle"]
    except:
        data["appbundle"] = None
    try:
        data["appcat"] = bid_req["app"]["cat"]
    except:
        data["appcat"] =None
    try:
        data["appid"] = bid_req["app"]["id"]
    except:
        data["appid"] = None
    try:
        data["appname"] = bid_req["app"]["name"]
    except:
        data["appname"] = None
    try:
        data["apppubid"] = bid_req["app"]["publisher"]["id"]
    except:
        data["apppubid"] = None
    try:
        data["apppubname"] = bid_req["app"]["publisher"]["name"]
    except:
        data["apppubname"] = None
    try:
        data["appstoreurl"] = bid_req["app"]["storeurl"]
    except:
        data["appstoreurl"] = None
    try:
        data["appver"] = bid_req["app"]["ver"]
    except:
        data["appver"] = None
    #impression features
    try:
        data["bannerapi"] = bid_req["imp"][0]["banner"]["api"]
    except:
        data["bannerapi"] = None
    try:
        data["battr"] = bid_req["imp"][0]["banner"]["battr"]
    except:
        data["battr"] = None
    try:
        data["btype"] = bid_req["imp"][0]["banner"]["btype"]
    except:
        data["btype"] = None
    try:
        data["w"] = bid_req["imp"][0]["banner"]["w"] #ad slot width
    except:
        data["w"] = None
    try:
        data["h"] = bid_req["imp"][0]["banner"]["h"] #ad slot height
    except:
        data["h"] = None
    try:
        data["pos"] = bid_req["imp"][0]["banner"]["pos"]
    except:
        data["pos"] = None
    try:
        data["bidfloor"] = float(bid_req["imp"][0]["bidfloor"]) #bid floor price
    except:
        data["bidfloor"] = 0.01
    try:
        data["displaymanager"] = bid_req["imp"][0]["displaymanager"]
    except:
        data["displaymanager"] = None
    try:
        data["displaymanagerver"] = bid_req["imp"][0]["displaymanagerver"]
    except:
        data["displaymanagerver"] = None
    try:
        data["impid"] = bid_req["imp"][0]["id"]
    except:
        data["impid"] = None
    try:
        data["instl"] = bid_req["imp"][0]["instl"]
    except:
        data["instl"] = None
    try:
        data["tagid"] = bid_req["imp"][0]["tagid"]
    except:
        data["tagid"] = None
    #user features
    try:
        data["user"] = bid_req["user"]
    except:
        data["user"] = None
    return data
