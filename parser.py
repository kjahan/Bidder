#grab json and extract all low level signals
def parse(bid_req):
    data = {}
    data["id"] = bid_req["id"]  #bid id
    data["ua"] = bid_req["device"]["ua"]    #ua
    data["ip"] = bid_req["device"]["ip"]
    data["country"] = bid_req["device"]["geo"]["country"]#country
    data["region"] = bid_req["device"]["geo"]["region"] #region
    data["city"] = bid_req["device"]["geo"]["city"] #city
    data["domain"] = bid_req["site"]["domain"] #domain
    data["page"] = bid_req["site"]["page"] #url
    data["w"] = bid_req["imp"][0]["banner"]["w"] #ad slot width
    data["h"] = bid_req["imp"][0]["banner"]["h"] #ad slot height
    data["bidfloor"] = bid_req["imp"][0]["bidfloor"] #bid floor price
    data["ts"] = bid_req["ext"]["ts"]
    data["adexchangeid"] = bid_req["ext"]["adexchangeid"]
    data["visibility"] = bid_req["ext"]["visibility"]
    data["format"] = bid_req["ext"]["format"]
    data["pp"] = bid_req["ext"]["pp"]
    data["bp"] = bid_req["ext"]["bp"]
    data["tags"] = bid_req["ext"]["tags"]
    data["clk"] = bid_req["ext"]["clk"]
    data["conv"] = bid_req["ext"]["conv"]
    return data
