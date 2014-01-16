
def converter(L):
    """Takes picobot code, as a list, and returns a picobot dictionary"""
    picobotDict = {}
    for item in L:
        key = (int(item[0]), str(item[2:6]))
        value = (str(item[10]), int(item[12]))
        picobotDict[key] = value
    return picobotDict
        
L = [
 '0 NExx -> W 2',
 '0 NxWx -> E 2',
 '0 Nxxx -> X 2',
 '0 xExS -> N 4',
 '0 xExx -> S 2',
 '0 xxWS -> X 2',
 '0 xxWx -> X 2',
 '0 xxxS -> N 0',
 '0 xxxx -> S 3',
 '1 NExx -> X 4',
 '1 NxWx -> S 4',
 '1 Nxxx -> W 4',
 '1 xExS -> W 3',
 '1 xExx -> W 0',
 '1 xxWS -> E 0',
 '1 xxWx -> X 0',
 '1 xxxS -> E 1',
 '1 xxxx -> N 0',
 '2 NExx -> S 3',
 '2 NxWx -> S 1',
 '2 Nxxx -> X 3',
 '2 xExS -> W 0',
 '2 xExx -> W 4',
 '2 xxWS -> X 3',
 '2 xxWx -> S 0',
 '2 xxxS -> X 0',
 '2 xxxx -> X 1',
 '3 NExx -> S 3',
 '3 NxWx -> S 2',
 '3 Nxxx -> S 0',
 '3 xExS -> N 2',
 '3 xExx -> N 1',
 '3 xxWS -> E 4',
 '3 xxWx -> S 3',
 '3 xxxS -> N 4',
 '3 xxxx -> S 0',
 '4 NExx -> W 0',
 '4 NxWx -> E 4',
 '4 Nxxx -> W 3',
 '4 xExS -> X 1',
 '4 xExx -> X 1',
 '4 xxWS -> X 2',
 '4 xxWx -> N 0',
 '4 xxxS -> X 1',
 '4 xxxx -> N 4']
