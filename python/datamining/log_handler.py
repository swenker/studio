__author__ = 'sunwj'


class LogParser():


    def parse_raw_log(self,log_file_path):
        "parse log to extract uid,itemid, magazineid "
        print "hello"
        outfile=file("uid_mid_weight.txt","w")

        ummap={}
        try:
            with open(log_file_path) as f:
                for line in f:
                    if line.count("downloadReport"):
                        #2014-06-01 10:31:40 downloadReport 357630053387836 4038b64c t8cdktvble 3.0.0.10 1 4.3 SM-N900S 366 77 1
                        line = line.strip()
                        fields = line.split()
                        uid = fields[5]
                        if uid == '-':
                            continue

                        #itemid=fields[10]
                        mid = fields[11]

                        if ummap.has_key(uid):
                            midmap = ummap[uid]
                            if midmap.has_key(mid):
                                midmap[mid] += 1
                            else:
                                midmap = {mid:1}

                            ummap[uid] = midmap

                        else:
                            if mid:
                                ummap[uid] = {mid:1}


                for key in ummap.keys():
                    tmap=ummap[key]

                    ulines=[]
                    for mid in tmap.keys():
                        oline = "%s,%s,%d \n" %(key,mid,tmap[mid])
                        ulines.append(oline)

                    outfile.writelines(ulines)
        except IOError:
            print IOError.message
            outfile.close()

        return ummap




class UserDownloadModel():
    pass
