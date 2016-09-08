import glob
import os
import scipy.io
import pandas
from highcharts import Highchart
from scipy.signal import resample
import numpy as np


def rolling_mean(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return cumsum[n:] - cumsum[:-n] / n


def main():
    pwd = str(os.getcwd())
    home = os.path.abspath(os.path.join(pwd, os.pardir))
    # data location, relative.
    dir = '/data/train_1/'
    # define test file, layout is from when i wanted to iterate over all files
    # to run over all files change line to '*.mat'
    file_type = '1_920_0.mat'

    file_list = glob.glob(home+dir+file_type)
    for f in file_list:

        name = f[:-4]
        name = name.split('/')
        name = name[len(name)-1]

        # load .mat file
        mat = scipy.io.loadmat(f)
        headers = ['channel0', 'channel1', 'channel2', 'channel3',
                   'channel4', 'channel5', 'channel6', 'channel7',
                   'channel8', 'channel9', 'channel10', 'channel11',
                   'channel12', 'channel13', 'channel14', 'channel15']

        # get actual data from the .mat file
        channels_data = mat['dataStruct'][0][0][0]
        # resample file
        rs_data = resample(channels_data, 3000, axis=0)
        
        df = pandas.DataFrame(rs_data, columns=headers)

        charts = Highchart()
        
        options = {'chart': {'type': 'line', 'zoomType': 'x'}, 'title': {'text': 'test'},
                   'xAxis': {'type': 'float', 'title': {'enabled': True, 'text': 'time (ms)'}},
                   'yAxis': [{'type': 'int', 'title': {'enabled': True, 'text': 'EEG signal'}, 'opposite': False},
                             {'type': 'int', 'title': {'enabled': True, 'text': 'variance'}, 'opposite': True}]}
        charts.set_dict_options(options)

        for i in headers:
            data = df[i].tolist()
            mean = df[i].rolling(window=2).mean()
            d_var = df[i].rolling(window=2).var()
            d_var = d_var.dropna()
            mean = mean.dropna()
            data = [float(j) for j in data]
            disp = []
            d_var = [float(j) for j in d_var]
            mean = [float(j) for j in mean]
            for k in range(len(mean)):
                disp.append(d_var[k]/mean[k])
            charts.add_data_set(data, 'line', i)
            name = str(i)+'_disp'
            charts.add_data_set(disp, 'line', name, yAxis=1)

        charts.save_file(name)
            
                
if __name__ == '__main__':
    main()
