__author__ = 'Wenju Sun'

#logfile = "d:/u_ex140108.log"
#logfile = "d:/u_in140109.log"
"""date format:u_ex140109
   hour: 0,1,10
   result is csv
"""

DEBUG=True
#http://dl-3m.svc.mcitech.cn/items/58/160/6DEAA08641F8B313A14759F27730E7A4.zip
def loadUrlList():
    urlList = []
    furl = r'D:\work\allurl-20140310.txt'
    f = open(furl, "rb")
    for sline in f:
        newline = sline.strip()
        #urlList.append(newline[len("http://dl-3m.svc.mcitech.cn"):])
        urlList.append(newline)
        if DEBUG:
            for u in urlList:
                print u
    return urlList

#10.159.63.173, -, 1/8/2014, 14:27:04, W3SVC2, 3mdl01-svc-mscc, 10.200.115.148, 531, 437, 2097431, 206, 0, GET, /items/51/195/ee257008-625e-4498-b4d3-02c7bda1fee5.zip, -,
def parseLog(input_file):
    """
    Check the occurence of the elements in url list
    @rtype : dict
    """
    #global zip_request_hour_counter
    zip_request_total_counter = 0
    zip_request_total_counter_unknown = 0

    occurence_map = {}
    urlList = loadUrlList()
    for u in urlList:
        occurence_map[u]=[0]*24

    unknownfile_map={}

    with open(input_file, "r") as fHandle:
        for line in fHandle:
            sline=line.strip()
            if (not sline.startswith("#") and sline.count("GET") > 0 and sline.count("zip") > 0):
                zip_request_total_counter += 1
                log_fields = sline.split(",")

                #ldate = log_fields[2].strip()
                ltime = log_fields[3].strip()
                #request_type = log_fields[12].strip()
                filename = log_fields[13].strip()
                hour=int(ltime.split(":")[0])

                if(urlList.count(filename)==0):

                    zip_request_total_counter_unknown+=1
                    if(unknownfile_map.has_key(filename)):
                        uc = unknownfile_map[filename]
                        unknownfile_map[filename] = uc+1
                    else:
                        unknownfile_map[filename] = 1
                else:
                    for u in urlList:
                        hourly_counters = occurence_map[u]
                        lc = sline.count(u)
                        if (lc > 0):
                            hourly_counters[hour] += lc
                            occurence_map[u] = hourly_counters

    print  zip_request_total_counter,zip_request_total_counter_unknown
    return occurence_map,unknownfile_map


querydate="140309"
logfile = "d:/work/log/u_in"+querydate+".log"
resultfile="d:/work/log/parseresult"+querydate+"1.csv"
unresultfile="d:/work/log/unresult"+querydate+"1.csv"

counter_map,unknownfile_map= parseLog(logfile)

#print len(counter_map)
with open(resultfile,"w") as fresult:
    header="file,"
    for i in range(24):
        header =header + str(i)+","
    header +="total"
    #print header
    fresult.write(header+"\n")

    for k, v in counter_map.items():
        sline=k+","
        perzip_total=0
        for h in v:
            perzip_total +=h
            sline = sline+str(h)+","

        #zip_request_total_counter +=perzip_total
        sline+=str(perzip_total)
        #print sline
        fresult.write(sline+"\n")



unknownfile_counter=0
with open(unresultfile,"w") as f:
    for k,v in unknownfile_map.items():
        sline =k+","+str(v) + "\n"
        #unknownfile_counter +=v

        f.write(sline)

#print unknownfile_counter