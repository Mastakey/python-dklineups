class DKSalary(object):
    def __init__(self, csvfile):
        self.csvfile = csvfile

    def getDkdata(self):
        #returns a list of dict of:
        #[{player, salary, position}]
        f = open(self.csvfile,  'r')
        dk_lines = f.readlines()
        count = 0
        dkdata = []
        #print len(salary_lines)
        for line in dk_lines:
            #ignore header line
            if count > 0:
                mydict = {}
                mycsvlist = line.split(',')
                mydict['position'] = mycsvlist[0].replace("\"", "")
                mydict['player']  = mycsvlist[1].replace("\"", "")
                mydict['salary']  = mycsvlist[2].replace("\"", "")
                #print position
                dkdata.append(mydict)
            count += 1
        return dkdata
