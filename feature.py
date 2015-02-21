import numpy as np
from datetime import datetime
from ua_parser import user_agent_parser

def extract_features(data):
    fet = {}
    #exctarct features we want to use for building model
    fet["id"] = data["id"] #bid id
    date = datetime.strptime(str(data["ts"]), '%Y%m%d%H%M%S%f')
    fet["dow"] = str(date.weekday()) #day of week
    fet["month"] = str(date.month)   #month
    fet["hour"] = str(date.hour) #hour of day
    result_dict = user_agent_parser.Parse(data["ua"])
    fet["osfamily"] = transform_os_fet(result_dict['os']['family'].lower())   #iOS
    fet['uafamily'] = transform_browser_fet(result_dict['user_agent']['family'].lower())   #Mobile Safari
    fet['devfamily'] = result_dict['device']['family'].lower()   #iPhone
    fet["ip"] = data["ip"]
    fet["country"] = data["country"] #country
    fet["region"] = data["region"] #region
    fet["city"] = data["city"] #city
    fet["domain"] = data["domain"] #domain
    fet["page"] = data["page"] #url
    fet["w"] = data["w"] #ad slot width
    fet["h"] = data["h"] #ad slot height
    fet["slotsize"] = str(data["w"]) + "*" + str(data["h"])
    fet["bidfloor"] = int(data["bidfloor"]) #bid floor price
    fet["ts"] = data["ts"] #ts
    fet["adexchangeid"] = data["adexchangeid"]
    fet["visibility"] = data["visibility"]
    fet["format"] = data["format"]
    fet["pp"] = data["pp"]
    fet["bp"] = data["bp"]
    fet["tags"] = data["tags"]
    fet["clk"] = int(data["clk"])
    fet["conv"] = int(data["conv"])
    return fet

def transform_browser_fet(ua_family):
    if ua_family.startswith("opera"):
        #opera browser
        return "opera"
    elif ua_family.startswith("firefox"):
        #firefox browser
        return "firefox"
    elif ua_family.startswith("chrome"):
        #chrome browser
        return "chrome"
    elif ua_family.startswith("sogou"):
        #sogou browser
        return "sogou"
    elif (ua_family.startswith("ie") or ua_family.startswith("myie2")):
        #IE browser
        return "ie"
    elif ua_family.startswith("maxthon"):
        #maxthon browser
        return "maxthon"
    elif (ua_family.startswith("safari") or ua_family.startswith("mobile safari")):
        #safari browser
        return "safari"
    elif ua_family.startswith("qq"):
        #qq browser
        return "qq"
    #other browser
    return "other"

def transform_os_fet(os_family):
    if os_family.startswith("windows phone"):
        return "wphone"
    elif os_family.startswith("ios"):
        return "ios"
    elif os_family.startswith("android"):
        return "android"
    elif os_family.startswith("mac os x"):
        return "mac"
    elif os_family.startswith("windows"):
        return "windows"
    elif (os_family.startswith("ubuntu") or os_family.startswith("suse") or os_family.startswith("fedora") or os_family.startswith("gentoo") or os_family.startswith("debian") or os_family.startswith("linux mint") or os_family.startswith("linux") or os_family.startswith("red hat")):
        return "linux"
    #other
    return "other"

#this method stores an encoded version of features
def generate_training_data(features, file_name, encoder):
    with open(file_name, "w") as fp:
        fp.write("dow,hour,os,browser,region,slotsize,usertags\n")
        dims = [7,24,7,9,35,14,44]  #for now hard coded
        out = ",".join(map(str, dims)) + "\n"
        fp.write(out)
        #dow: 7, hour:24, os: 7, browser: 9, region: 35, slot_size: 14, tags: 44 --> total dimension=140
        tot_dim = sum(dims)
        cnt = 0
        for fet in features:
            array, x = encoder.encode(fet)
            out = ",".join(array) + "," + str(fet["clk"]) + "," + fet["id"] + "\n"
            fp.write(out)
            if cnt > 0:
                X[cnt] = x
                Y = np.append(Y, [fet["clk"]])
            else:
                X = np.zeros((len(features), tot_dim))
                X[cnt] = x
                Y = np.array(fet["clk"])
            cnt += 1
    return X, Y
