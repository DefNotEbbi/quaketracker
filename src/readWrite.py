# Author: Ebrahim Muneer
# Common read/write/list functions

import os
import pandas as pd

# Returns the list of all the .mseed files in a given directory
def listFiles(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.mseed')]

# Returns the catalog as a pandas dataframe
def readCatalog(path):
    return pd.read_csv(path)

# Returns the time of a given filename in the catalog
def getCatalogTimes(catalog, filename):
    f = catalog[catalog['filename'] == filename]
    if f.empty:
        print(f"Warning: Filename {filename} not found in catalog.")
        return None
    return f['time_rel(sec)'].iloc[0]

# Initializes common directories (for testing)
def initCommonDir():
    currentDir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'data', 'S12_GradeA')
    filenames = listFiles(data_directory)
    catalogDir = os.path.join(currentDir, '..', 'space_apps_2024_seismic_detection', 'data', 'lunar', 'training', 'catalogs', 'apollo12_catalog_GradeA_final.csv')
    catalog = readCatalog(catalogDir)
    
    return data_directory, filenames, catalog

# Writes the resulting data to a .csv file
def writeCatalog(directory, data):
    if os.path.exists(directory):
        folder_name = os.path.basename(os.path.dirname(directory))
        outputCatalog = pd.DataFrame(data)
        outputCatalog.to_csv(f"../results/{folder_name}.csv", index=False)
    else:
        print(f"Warning: Invalid or Missing Path, {directory} does not exist.")

if __name__ == "__main__":
    pass