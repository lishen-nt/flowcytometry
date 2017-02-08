import os
import fcsparser
import FlowCal
import numpy as np

fcs_directory = '/home/hduser/FlowCAP-II/Data/AML/FCS/'
csv_directory = '/home/hduser/FlowCAP-II/Data/AML/CSV/'
header = 'FS Lin, SS Log, FL1 Log, FL2 Log,FL3 Log, FL4 Log, FL5 Log'

files = (s for s in os.listdir(fcs_directory))
file_names = []
for s in files:
    file_names.append(s)
    file_names.sort()

# extracts raw data of the 7 channels from the FCS and save as CSV with the same file name
for s in file_names:
    fcs_path = fcs_directory + s
    data = np.array(FlowCal.io.FCSData(fcs_path))
    np.savetxt(csv_directory + s[:-3]+'CSV', data, delimiter=',', fmt='%.1d', header = header, comments='')
