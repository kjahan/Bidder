import numpy as np

class Encoder:
    def __init__(self):
        inx = 0
        dows = ["0", "1", "2", "3", "4", "5", "6"]  #date object: Monday is 0 and Sunday is 6
        hours = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        oss = ["android","ios","linux","mac","other","windows","wphone"]
        browsers = ["chrome","firefox","ie","maxthon","opera","other","qq","safari","sogou"]
        regions = ["0","1","106","124","134","146","15","164","183","2","201","216","238","253","27","275","276","298","3","308","325","333","344","359","368","374","393","394","395","40","55","65","79","80","94"]
        slot_sizes = ["1000*90","120*600","160*600","200*200","250*250","300*250","300*300","336*280","360*300","468*60","728*90","910*90","950*90","960*90"]
        user_tags = ["10006","10024","10031","10048","10052","10057","10059","10063","10067","10074","10075","10076","10077","10079","10083","10093","10102","10684","11092","11278","11379","11423","11512","11576","11632","11680","11724","11944","13042","13403","13496","13678","13776","13800","13866","13874","14273","16593","16617","16661","16706","16751","10110","10111"]
        #generate a map for dow
        self.dows_map = dict(zip(dows, xrange(inx, inx + len(dows))))
        inx += len(dows)
        #generate a map for hours
        self.hours_map = dict(zip(hours, xrange(inx, inx + len(hours))))
        inx += len(hours)
        #generate a map for oss
        self.oss_map = dict(zip(oss, xrange(inx, inx + len(oss))))
        inx += len(oss)
        #generate a map for browsers
        self.browsers_map = dict(zip(browsers, xrange(inx, inx + len(browsers))))
        inx += len(browsers)
        #generate a map for regions
        self.regions_map = dict(zip(regions, xrange(inx, inx + len(regions))))
        inx += len(regions)
        #generate a map for slot size
        self.slot_size_map = dict(zip(slot_sizes, xrange(inx, inx + len(slot_sizes))))
        inx += len(slot_sizes)
        #generate a map for uaser tags
        self.user_tag_map = dict(zip(user_tags, xrange(inx, inx + len(user_tags))))
        inx += len(user_tags)
        self.tot_dim = inx

    def encode(self, fet):
        #dow: 7, hour:24, os: 7, browser: 9, region: 35, slot_size: 14 --> total dimension=96      --> considering traing and test data for round 2 adv id=1458!!!
        dow_inx = self.dows_map[fet["dow"]]
        hour_inx = self.hours_map[fet["hour"]]
        os_inx = self.oss_map[fet["osfamily"]]
        browser_inx = self.browsers_map[fet["uafamily"]]
        region_inx = self.regions_map[fet["region"]]
        slot_size_inx = self.slot_size_map[fet["slotsize"]]
        user_tag_inxs = []
        if fet["tags"] and "null" not in fet["tags"]:  #now in mongo we write null literally if no tag exists
            #print fet["tags"]
            #let's split tags and store them as a list
            tags = fet["tags"].split(",")
            for tag in tags:
                tag_inx = self.user_tag_map[tag]
                user_tag_inxs.append(tag_inx)        #add all tag index to this list
            #else:
            #    print fet["tags"]
            #    print fet["id"]
        array = self.tot_dim*[0]
        x = np.zeros(self.tot_dim)
        array[dow_inx] = 1   #dow
        x[dow_inx] = 1   #dow
        array[hour_inx] = 1   #hour
        x[hour_inx] = 1   #hour
        array[os_inx] = 1    #os
        x[os_inx] = 1    #os
        array[browser_inx] = 1  #browser
        x[browser_inx] = 1  #browser
        array[region_inx] = 1        #region
        x[region_inx] = 1        #region
        array[slot_size_inx] = 1     #slot size
        x[slot_size_inx] = 1     #slot size
        #let's set all tag id indexes
        for tag_inx in user_tag_inxs:
            array[tag_inx] = 1   #user tag
            x[tag_inx] = 1
        array = map(str, array)
        return array, x
