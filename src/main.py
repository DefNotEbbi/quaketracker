import typer
from readWrite import *
from obspy import read
from detectionAlgorithms import *
from plot import *
import os

app = typer.Typer()

@app.command()
def staLtaApprox(data_directory : str, output_results : bool = False, output_name : str = "results.csv", short_window : int = 155, long_window : int = 1470, on_factor : float = 0.3, plot : bool = False):
    filenames = None
    isDir = False
    if os.path.exists(data_directory) == False:
        print(f"Warning: Invalid or Missing Path, {data_directory} does not exist.")
        exit()

    if os.path.isdir(data_directory):
        filenames = listFiles(data_directory)
        isDir = True
    elif os.path.isfile(data_directory):
        filenames = [data_directory]

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = None

        if isDir:
            st = read(f"{data_directory}/{filename}")
        else:
            st = read(f"{data_directory}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime, staLta, onThresh = recursiveStaLtaMax(tr_times, tr_data, tr_sampling_rate, short_window, long_window, on_factor)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if plot:
            plot_staLta(tr_times, tr_data, predictedTime, staLta, onThresh, filename)

    if output_results:
        writeCatalog(f"{os.path.dirname(data_directory)}/{output_name}", data)

@app.command()
def zDetection(data_directory : str, output_results : bool = False, output_name : str = "results.csv", short_window : int = 260, onFactor : float = 0.3, plot : bool = False):
    filenames = None
    isDir = False
    if os.path.exists(data_directory) == False:
        print(f"Warning: Invalid or Missing Path, {data_directory} does not exist.")
        exit()

    if os.path.isdir(data_directory):
        filenames = listFiles(data_directory)
        isDir = True
    elif os.path.isfile(data_directory):
        filenames = [data_directory]

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = None

        if isDir:
            st = read(f"{data_directory}/{filename}")
        else:
            st = read(f"{data_directory}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime, staLta, onThresh = zDetect(tr_times, tr_data, tr_sampling_rate, short_window, onFactor)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if plot:
            plot_staLta(tr_times, tr_data, predictedTime, staLta, onThresh, filename)

    if output_results:
        writeCatalog(f"{os.path.dirname(data_directory)}/{output_name}", data)

@app.command()
def staLtaAccurate(data_directory : str, output_results : bool = False, output_name : str = "results.csv", short_window : int = 155, long_window : int = 1470, on_factor : float = 0.3, plot : bool = False):
    filenames = None
    isDir = False
    if os.path.exists(data_directory) == False:
        print(f"Warning: Invalid or Missing Path, {data_directory} does not exist.")
        exit()

    if os.path.isdir(data_directory):
        filenames = listFiles(data_directory)
        isDir = True
    elif os.path.isfile(data_directory):
        filenames = [data_directory]

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = None

        if isDir:
            st = read(f"{data_directory}/{filename}")
        else:
            st = read(f"{data_directory}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime, staLta, onThresh = classicStaLtaMax(tr_times, tr_data, tr_sampling_rate, short_window, long_window, on_factor)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if plot:
            plot_staLta(tr_times, tr_data, predictedTime, staLta, onThresh, filename)

    if output_results:
        writeCatalog(f"{os.path.dirname(data_directory)}/{output_name}", data)

@app.command()
def simpleMax(data_directory : str, output_results : bool = False, output_name : str = "results.csv", plot : bool = False):
    filenames = None
    isDir = False
    if os.path.exists(data_directory) == False:
        print(f"Warning: Invalid or Missing Path, {data_directory} does not exist.")
        exit()

    if os.path.isdir(data_directory):
        filenames = listFiles(data_directory)
        isDir = True
    elif os.path.isfile(data_directory):
        filenames = [data_directory]

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = None

        if isDir:
            st = read(f"{data_directory}/{filename}")
        else:
            st = read(f"{data_directory}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data

        predictedTime = simpleMaxAlgo(tr_times, tr_data)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if plot:
            plot_trace(tr_times, tr_data, predictedTime, filename)

    if output_results:
        writeCatalog(f"{os.path.dirname(data_directory)}/{output_name}", data)

@app.command()
def curveFitDetection(data_directory : str, output_results : bool = False, output_name : str = "results.csv", degree : int = 5, plot : bool = False):
    filenames = None
    isDir = False
    if os.path.exists(data_directory) == False:
        print(f"Warning: Invalid or Missing Path, {data_directory} does not exist.")
        exit()

    if os.path.isdir(data_directory):
        filenames = listFiles(data_directory)
        isDir = True
    elif os.path.isfile(data_directory):
        filenames = [data_directory]

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = None

        if isDir:
            st = read(f"{data_directory}/{filename}")
        else:
            st = read(f"{data_directory}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data

        predictedTime, curve = maxLineMap(tr_times, tr_data, degree)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if plot:
            plot_staLta(tr_times, tr_data, predictedTime, curve, min(curve), filename)

    if output_results:
        writeCatalog(f"{os.path.dirname(data_directory)}/{output_name}", data)

@app.command()
def backflip(data_directory : str, output_results : bool = False, output_name : str = "results.csv", jump_window : int = 290, plot : bool = False):
    filenames = None
    isDir = False
    if os.path.exists(data_directory) == False:
        print(f"Warning: Invalid or Missing Path, {data_directory} does not exist.")
        exit()

    if os.path.isdir(data_directory):
        filenames = listFiles(data_directory)
        isDir = True
    elif os.path.isfile(data_directory):
        filenames = [data_directory]

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = None

        if isDir:
            st = read(f"{data_directory}/{filename}")
        else:
            st = read(f"{data_directory}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data

        predictedTime = maxDetect(tr_times, tr_data, jump_window)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if plot:
            plot_trace(tr_times, tr_data, predictedTime, filename)

    if output_results:
        writeCatalog(f"{os.path.dirname(data_directory)}/{output_name}", data)

if __name__ == '__main__':
    app()
