import typer
from readWrite import *
from obspy import read
from detectionAlgorithms import *
import matplotlib.pyplot as plt

app = typer.Typer()

@app.command()
def staLtaMax(data_directory : str, output_results : bool = True, short_window : int = 155, long_window : int = 1470, on_factor : float = 0.3):
    filenames = listFiles(data_directory)

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = read(f"{data_directory}/{filename}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        
        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime, staLta, onThresh = recursiveStaLtaMax(tr_times, tr_data, tr_sampling_rate, short_window, long_window, on_factor)
        
        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

    if output_results:
        writeCatalog(data_directory, data)

@app.command()
def simpleMax(data_directory : str, output_name: str = "results.csv", output_results : bool = True):
    filenames = listFiles(data_directory)

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = read(f"{data_directory}/{filename}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime = simpleMaxAlgo(tr_times, tr_data, tr_sampling_rate)

        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

    if output_results:
        writeCatalog(f"{data_directory}/{output_name}", data)

@app.command()
def curveFitDetection(data_directory : str,output_name: str = "results.csv", output_results : bool = True, degree : int = 5, curvePlot : bool = False):
    filenames = listFiles(data_directory)

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = read(f"{data_directory}/{filename}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime, curve = maxLineMap(tr_times, tr_data, degree)

        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

        if curvePlot:
            curvePlot = False
            plt.plot(tr_times, tr_data)
            plt.show()
            plt.plot(curve)
            plt.show()

    if output_results:
        writeCatalog(f"{data_directory}/{output_name}", data)

@app.command()
def backflip(data_directory : str, output_name: str = "results.csv", output_results : bool = True, jump_window : int = 290):
    filenames = listFiles(data_directory)

    data = {
        "filename" : [],
        "time_rel(sec)" : []
    }

    for filename in filenames:
        st = read(f"{data_directory}/{filename}")

        st.filter('bandpass', freqmin = 0.9, freqmax = 0.91)

        tr = st[0]
        tr_times = tr.times()
        tr_data = tr.data
        tr_sampling_rate = tr.stats.sampling_rate

        predictedTime = maxDetect(tr_times, tr_data, jump_window)

        print(f"{filename} - {predictedTime:.2f}s")

        data["filename"].append(filename.replace('.mseed', ''))
        data["time_rel(sec)"].append(predictedTime)

    if output_results:
        writeCatalog(f"{data_directory}/{output_name}", data)


if __name__ == '__main__':
    app()