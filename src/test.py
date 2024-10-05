# Author: Ebrahim Muneer
# Rough testing playground

from obspy import read, UTCDateTime
from plot import *
from detectionAlgorithms import *
from readWrite import *
#from crossCorrelate import *
import os
from geneticAlgorithm import *

def geneticTuning():
    currentDir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'data', 'S12_GradeA')
    filenames = listFiles(data_directory)
    catalogDir = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'catalogs', 'apollo12_catalog_GradeA_final.csv')
    catalog = readCatalog(catalogDir)

    generticAlgorithm = GeneticAlgorithm(10, 0.95, 200, filenames, catalog, data_directory)
    generticAlgorithm.run()


def tuning():
    currentDir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'data', 'S12_GradeA')
    filenames = listFiles(data_directory)
    catalogDir = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'catalogs', 'apollo12_catalog_GradeA_final.csv')
    catalog = readCatalog(catalogDir)

    bestOnFactor = 0.0
    attempts = 0
    onFactor = 0.0
    lowestError = 2.74

    while attempts < 100:

        attempts += 1

        onFactor += 0.01
        
        error_list = []


        for filename in filenames:
            st = read(f"{data_directory}/{filename}")
            st.filter('bandpass', freqmin=0.90, freqmax=0.91)

            tr = st[0]
            tr_times = tr.times()
            tr_data = tr.data
            tr_samplingRate = tr.stats.sampling_rate

            catalogArrival = getCatalogTimes(catalog, filename.replace('.mseed', ''))
            predictedArrival, sta_lta, on_threshold = recursiveStaLtaMax(tr_times, tr_data, tr_samplingRate, on_factor=onFactor)

            if catalogArrival is not None and predictedArrival is not None:
                error = (abs(catalogArrival - predictedArrival) / np.max(tr_times)) * 100
                error_list.append(error)

        avgError = np.mean(error_list)
        print(f"Attempt {attempts} - On Factor {onFactor} - Error {avgError}")
        if avgError < lowestError:
            lowestError = avgError
            bestOnFactor = onFactor
            print(f"Best on factor {bestOnFactor} - Attempt {attempts} - Error: {avgError}")
            with open("bestOnFactor.txt", "w") as f:
                f.write(str(bestOnFactor))

def test():

    currentDir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'mars', 'training', 'data')
    filenames = listFiles(data_directory)
    catalogDir = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'mars', 'training', 'catalogs', 'Mars_InSight_training_catalog_final.csv')
    catalog = readCatalog(catalogDir)
    error_list = []
    plot = False
    
    st = read(f"{data_directory}/{filenames[1]}")
    st.filter('bandpass', freqmin=0.99, freqmax=1.0)

    print(st)

    tr = st[0]
    tr_times = tr.times()
    tr_data = tr.data
    tr_samplingRate = tr.stats.sampling_rate

    catalogArrival = getCatalogTimes(catalog, filenames[0].replace('.mseed', ''))

    start = tr.stats.starttime + float(catalogArrival)
    end = start + 4000
    tr.trim(start, end)
    
    ref_event = tr.data

    for filename in filenames:

        st = read(f"{data_directory}/{filename}")
        
        disp_data = st[0].data
        disp_time = st[0].times()

        st_filt = st.copy()

        st_filt.filter('bandpass', freqmin=0.90, freqmax=0.91)

        tr = st_filt[0]
        tr_times = tr.times()
        tr_data = tr.data
        sampling_rate = tr.stats.sampling_rate

        #predictedArrival, sta_lta, on_threshold = recursiveStaLtaMaxCrossCorrelation(tr_times, tr_data, sampling_rate, ref_event)
        predictedArrival, sta_lta, on_threshold = maxDetect(tr_times, tr_data, 290)
        catalogArrival = getCatalogTimes(catalog, filename.replace('.mseed', ''))

        if predictedArrival is not None and catalogArrival is not None:
            error = (abs(catalogArrival - predictedArrival) / np.max(tr_times)) * 100
            error_list.append(error)
            print(f"{filename} - Seismic event detected at {predictedArrival:.2f} seconds - Error: {error:.2f}%")
            
            if plot and error >= 1:
                plot_staLta(disp_time, tr_data, predictedArrival, catalogArrival, sta_lta, on_threshold, filename)
                

        else:
            print(f"{filename} - No Seismic event detected")
            error_list.append(100)


    print(f"Average error: {np.mean(error_list):.2f}%")


def mainTest(debug = False, plot = False):

    # The data directory below is temporary and needs to be changed when switching over
    currentDir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'data', 'S12_GradeA')
    filenames = listFiles(data_directory)
    catalogDir = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'catalogs', 'apollo12_catalog_GradeA_final.csv')
    catalog = readCatalog(catalogDir)
    error_list = []
    bad_files = ['xa.s12.00.mhz.1971-10-31HR00_evid00045', 'xa.s12.00.mhz.1970-03-26HR00_evid00004', 'xa.s12.00.mhz.1974-06-25HR00_evid00149', 'xa.s12.00.mhz.1972-07-17HR00_evid00067', 'xa.s12.00.mhz.1970-07-20HR00_evid00011', 'xa.s12.00.mhz.1972-07-17HR00_evid00068', 'xa.s12.00.mhz.1974-04-27HR00_evid00145', 'xa.s12.00.mhz.1970-04-25HR00_evid00006', 'xa.s12.00.mhz.1970-10-24HR00_evid00014', 'xa.s12.00.mhz.1973-07-04HR00_evid00114', 'xa.s12.00.mhz.1974-07-17HR00_evid00153', 'xa.s12.00.mhz.1971-06-12HR00_evid00035', 'xa.s12.00.mhz.1973-06-05HR00_evid00107', 'xa.s12.00.mhz.1974-07-06HR00_evid00151', 'xa.s12.00.mhz.1971-02-09HR00_evid00026', 'xa.s12.00.mhz.1970-07-20HR00_evid00010', 'xa.s12.00.mhz.1971-05-12HR00_evid00031', 'xa.s12.00.mhz.1970-11-12HR00_evid00015', 'xa.s12.00.mhz.1971-04-13HR02_evid00029']
    
    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:

        st = read(f"{data_directory}/{filename}")
        
        disp_data = st[0].data
        disp_time = st[0].times()

        st_filt = st.copy()

        st_filt.filter('bandpass', freqmin=0.90, freqmax=0.91)

        tr = st_filt[0]
        tr_times = tr.times()
        tr_data = tr.data
        sampling_rate = tr.stats.sampling_rate

        predictedArrival, sta_lta, on_threshold = recursiveStaLtaMax(tr_times, tr_data, sampling_rate)
        catalogArrival = getCatalogTimes(catalog, filename.replace('.mseed', ''))

        if predictedArrival is not None and catalogArrival is not None:
            error = (abs(catalogArrival - predictedArrival) / np.max(tr_times)) * 100
            error_list.append(error)
            print(f"{filename} - Seismic event detected at {predictedArrival:.2f} seconds - Error: {error:.2f}%")
            
            if plot and error >= 1:
                plot_staLta(disp_time, tr_data, predictedArrival, catalogArrival, sta_lta, on_threshold, filename)
                

        else:
            print(f"{filename} - No Seismic event detected")
            error_list.append(100)

        data['filename'].append(filename.replace('.mseed',''))
        data['time_rel(sec)'].append(predictedArrival)


        if debug:
            break

    writeCatalog(os.path.join(data_directory, 'output.csv'), data)
    print(f"Average error: {np.mean(error_list):.2f}%")

if __name__ == "__main__":
    test()