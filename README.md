# QuakeTracker

QuakeTracker is a command-line tool designed to accurately detect the start of seismic events from miniSEED files. Built for the [Space Apps 2024](https://www.spaceappschallenge.org/nasa-space-apps-2024/) hackathon under the [Seismic Detection across the Solar System](https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/seismic-detection-across-the-solar-system/) challenge.

## Installation

To get started, simply clone the repository and run the `main.py` script located in the `src` folder.

```
git clone https://github.com/QuakeTracker/QuakeTracker.git
cd QuakeTracker/src
python3 main.py --help
```

## Dependencies

The following Python packages are required:
- `obspy` (for handling seismic data)
- `matplotlib` (for plotting seismic traces and results)
- `numpy` (for numerical operations)
- `pandas` (for handling catalogs and output data)

You can install them via `pip`:

```bash
pip install obspy matplotlib numpy pandas
```

## Usage

The CLI provides flexibility to run different algorithms on seismic data. Use the help command to see available options:

```bash
python3 main.py [ALGORITHM] [ARGUMENTS] [DIRECTORY]
```

For instance, to run the `staltamax` algorithm on a folder containing miniSEED files:

```bash
python3 main.py staltamax ./data
```

To see all the available arguments for any specified algorithm:

```bash
python3 main.py [ALGORITHM] --help
```

For example, to override the default "jump window" value for the `backflip` algorithm:

```bash
python3 main.py backflip ./data --jump-window 50
```

## Algorithms

The following algorithms are available for event detection:

1. **staltamax**: Uses the recursive short-term average / long-term average (STA/LTA) method and `obspy`'s `trigger_onset` function to identify event start times.
(Preferred)

2. **backflip**: Jumps backward in the trace from the peak by a specified window until it finds a larger value.

3. **simplemax**: Returns the index of the maximum value in the seismic trace. Has a surprisingly low error despite its simplicity.

4. **curvefitdetection**: Similar to `backflip`, but first fits a polynomial curve to the trace and then steps back along the curve until it reaches a local minimum or the mean. This needs a high degree of polynomial fitting to work half-decently. 


## Working with the Source Code

The entire codebase is an undocumented mess and a frankenstein monster of different pieces of code snippets from the internet stitched togethher with mine very poorly, as this project had a deadline. I apologize in advance if you plan on working with this code. 

P.S: There's still a couple of other algorithms that are just different varients of the STA-LTA algorithm, for instance, Z-Detect and the Classic STA-LTA.

## Output

By default, all of the predicted times are listed down in CSV file along with their respective filenames. The CSV file is stored in the `results/` folder alongside `src/`.

## Credits

- **ObsPy**: For providing tools to work with miniSEED files and for the STA-LTA functions.
- **Matplotlib**: For generating the visualizations used in debugging and analysis.
- **Numpy** and **Pandas**: For data manipulation.
  
Special thanks to the NASA Space Apps Challenge for hosting the 2024 hackathon.

## License

This project is open-source under the [MIT License](LICENSE).
