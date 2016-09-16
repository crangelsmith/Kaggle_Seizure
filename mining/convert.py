import glob
import scipy.io
import pandas as pd
from highcharts import Highchart
from scipy.signal import resample
import config

## Couple of functions to analise the data from the Kaggle competition for seizure prediction (https://www.kaggle.com/c/melbourne-university-seizure-prediction)
## data input are Matlab type files that consist of a group of time series measurements from EEG signals
## This functions read the files in python, resample them, plot them and builds a new data frame with sumary statistics for each measurement

def convert_mat(f,resample_size):
    """ This function reads a file , resample the data to ms and returns a dataframe"""

    # load .mat file
    mat = scipy.io.loadmat(f)
    headers = ['channel0', 'channel1', 'channel2', 'channel3',
               'channel4', 'channel5', 'channel6', 'channel7',
               'channel8', 'channel9', 'channel10', 'channel11',
               'channel12', 'channel13', 'channel14', 'channel15']

    # get actual data from the .mat file
    channels_data = mat['dataStruct'][0][0][0]
    # resample file
    rs_data = resample(channels_data, resample_size, axis=0)

    df = pd.DataFrame(rs_data, columns=headers)

    return df


def main():
    """ main function read all files , make plots and process them """

    ## data location, relative
    dir = config.training_dir

    ## run over all files with '*.mat'
    file_type = '*.mat'

    # plotting setup
    charts = Highchart()
    options = {'chart': {'type': 'line'}, 'title': {'text': 'test'},
               'xAxis': {'type': 'float', 'title': {'enabled': True, 'text': 'time (ms)'}},
               'yAxis': {'type': 'int', 'title': {'enabled': True, 'text': 'EEG signal'}}}

    charts.set_dict_options(options)

    list_dict = []
    target_list = []

    # get a list of all files to be processed
    file_list = glob.glob(dir + file_type)

    for f in file_list:

        name = f[-9:-4]

        df = convert_mat(f,config.resample_size)

        # create lables that will eventually use in the clasification algorithm
        if "1.mat" in f:
            target = 1
        else:
            target = 0

        values_dict ={}
        # get summary statistics of each channel in the EGG, save them to a list of dictionaries
        for i in df.columns:

            values_dict[i+'_mean']=df[i].mean
            values_dict[i + '_median'] = df[i].median
            values_dict[i + '_std'] = df[i].std
            values_dict[i + '_min'] = df[i].min
            values_dict[i + '_max'] = df[i].max
            values_dict[i + '_kurt'] = df[i].kurt
            values_dict[i + '_kurtosis'] = df[i].kurtosis
            values_dict[i + '_skew'] = df[i].skew
            values_dict[i + '_var'] = df[i].var

            # plot each channel
            data = df[i].tolist()
            data = [float(j) for j in data]
            charts.add_data_set(data, 'line', i)

        # append summary of each measurement
        list_dict.append(values_dict)
        target_list.append(target)
        charts.save_file(config.out_dir+name)

    # get final data frame
    summary_df = pd.DataFrame.from_records(list_dict)
    summary_df['target']= pd.Series(target_list)
    summary_df.to_csv(config.out_dir+'Summary_Stats_df_Training1.csv')



if __name__ == '__main__':
    main()



