import subprocess
from Logger import *
class CongestionManager(object):
    def __init__(self, logger):
        self.logger = logger
    def getBackLog(self):
        byte_result = subprocess.check_output("tc -s qdisc", shell=True)
        result = str(byte_result).encode('utf-8')
        result_array = [s for s in result.splitlines()]
        # list of list, hashmap is {}
        interface_details = []
        for i in range(0, len(result_array),3):
            # dictionary 0: interface, 1: backlog bytes, 2: backlog packet
            tmp = []
            interface = result_array[i].split()[4]
            # insert take 2 arguments, to make retrieving value more sense when calculate rate, we use insert(index, value) 
            tmp.insert(0,interface)
            backlog = result_array[i+2].split()
            tmp.insert(1,backlog[1])
            tmp.insert(2,backlog[2])
            if tmp[0] != "lo":
                interface_details.append(tmp)
        return interface_details

if __name__ == "__main__":
    logger = Logger()
    cng_mngr = CongestionManager(logger)
    interface_details = cng_mngr.getBackLog()
    for interface_detail in interface_details:
            print (interface_detail[0] + ", " + interface_detail[1] + ", " + interface_detail[2])

     
