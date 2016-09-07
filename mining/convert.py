import glob
import os
import scipy.io
import pandas
from highcharts import Highchart
from scipy.signal import resample


def convert_mat(f):

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

        print df.describe()

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

        return df

            
                
if __name__ == "__main__":

    pwd = str(os.getcwd())
    # data location, relative.
    dir = '/../data/train_1/'
    # define test file, layout is from when i wanted to iterate over all files
    # to run over all files change line to '*.mat'
    file_type = '*.mat'


    list_dict = []

    target_list = []

    file_list = glob.glob(pwd + dir + file_type)
    for f in file_list:
        df = convert_mat(f)

        if "1.mat" in f:
            target = 1
        else:
            target = 0

        values_dict ={}
        for i in df.columns:

            values_dict[i+'_mean']=df[i].mean
            values_dict[i + '_median'] = df[i].median
            values_dict[i + '_std'] = df[i].std
            values_dict[i + '_min'] = df[i].min
            values_dict[i + '_max'] = df[i].max
            values_dict[i + '_kurt'] = df[i].kurt
            values_dict[i + '_kurtosis'] = df[i].kurtosis
            values_dict[i + '_skew'] = df[i].skew
            values_dict[i + '_cummax'] = df[i].cummax
            values_dict[i + '_cummin'] = df[i].cummin
            values_dict[i + '_cumprod'] = df[i].cumprod
            values_dict[i + '_cumsum'] = df[i].cumsum
            values_dict[i + '_var'] = df[i].var
            #values_dict[i + '_disp'] = values_dict[i+'_mean']/values_dict[i+'_var']

        list_dict.append(values_dict)
        target_list.append(target)


    summary_df = pandas.DataFrame(list_dict)

    summary_df.to_csv(pwd+"/../out/summary_df_Training1.csv")

    print summary_df.shape







