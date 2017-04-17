
import numpy as np
import csv

def distanceFrom(pos1,pos2):
    return np.linalg.norm(np.array(pos1)-np.array(pos2))
        
def dumpTableToCsv(filename, table):    
    csv_file = open(filename,"w")
    csv_writer = csv.writer(csv_file)
    header_row = None
    
    for row_name, data in table.items():
        fieldnames = [""]
        fieldnames.extend(sorted(data.keys()))
        
        if header_row is None:
            header_row = fieldnames
            csv_writer.writerow(header_row)
            
        assert (header_row == fieldnames), "Malformed table"
            
        s = map(lambda x: x[1][0], sorted(data.items(), key=lambda x: x[0]))
        row = [row_name]
        row.extend(s)
        csv_writer.writerow(row)
        
    csv_file.close()
    
def configToText(config):
    s = ",".join(map(lambda x: " ".join(map(str,x)),config))
    return s.replace("_"," ")

def dumpTableToLatex(table):
    print
    print "Latex table"    
    headers = [""]
    headers.extend(table.items()[0][1].keys())
    print " & ".join(headers), "\\\\"
       
    for row_name, data in table.items():
        row = []
        row.append(row_name)
        row.extend(data.values())
        row = map(str, row)
        
        print " & ".join(row), "\\\\"
        

def findConfigs(algorithm, purge_common=False):
    configs = set()
    
    for trial in algorithm.listTrials():
        conf = trial.getConfig()
        
        configs.add(frozenset(conf.items()))
        
    
    
    if purge_common:
        common_fields = set(configs.pop())
        for config in configs:
            
            common_fields.intersection_update(set(config))

        new_frozensets = set()
        
        for config in configs:
            new_config = set(config) - common_fields
            
            new_frozensets.add(frozenset(new_config))
        return new_frozensets
        
    else:
        return configs
                    
        
    
    
