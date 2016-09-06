import glob
import os
import scipy.io
import pandas
from highcharts import Highchart
from scipy.signal import resample


def main():
    pwd = str(os.getcwd())
    # data location, relative.
    dir = '/data/train_1/'
    # define test file, layout is from when i wanted to iterate over all files
    # to run over all files change line to '*.mat'
    file_type = '1_78_1.mat'

    file_list = glob.glob(pwd+dir+file_type)
    for f in file_list:
        name = f[:-4]
        # load .mat file
        mat = scipy.io.loadmat(f)
        headers = ['channel0', 'channel1', 'channel2', 'channel3',
                   'channel4', 'channel5', 'channel6', 'channel7',
                   'channel8', 'channel9', 'channel10', 'channel11',
                   'channel12', 'channel13', 'channel14', 'channel15']

        # get actual data from the .mat file
        channels_data = mat['dataStruct'][0][0][0]
        # resample file
        rs_data = resample(channels_data, 3600, axis=0)
        
        df = pandas.DataFrame(rs_data, columns=headers)
        print(df)
        charts = Highchart()
        
        options = {'chart': {'type': 'line'}, 'title': {'text': 'test'},
                   'xAxis': {'type': 'float', 'title': {'enabled': True, 'text': 'time (ms)'}},
                   'yAxis': {'type': 'int', 'title': {'enabled': True, 'text': 'EEG signal'}}}
        charts.set_dict_options(options)
        for i in headers:
            data = df[i].tolist()
            data = [float(j) for j in data]
            charts.add_data_set(data, 'line', i)
        charts.save_file(name)
            
                
if __name__ == '__main__':
    main()
