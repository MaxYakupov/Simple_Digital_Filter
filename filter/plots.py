from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from math import pi, sin
from scipy.signal import butter, filtfilt


class UnfilteredSignalPlot(FigureCanvasQTAgg):
    """Sum of Sinusoidal Input Signals y = y1 + y2.

    Parameters
    ----------
    `parent` : master widget
        Represents a widget to act as the parent of the current object
    """

    def __init__(self, parent=None, width=5, height=2, dpi=70):
        # create the Figure
        fig = Figure(figsize=(width, height), dpi=dpi)   # figsize - in inch
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)
        # create the axes
        self.axes = fig.add_subplot(111)
        self.configureAxes()
        self.draw()

    def plot(self, Am1 = 1, Fs1 = 1, Am2 = 1, Fs2 = 1, samples = 48000, section=4800):
        """Draw unfiltered signal.
        Return y"""
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        # create empty array
        y = [0] * samples
        # fill array with xxxHz signal
        for i in range(samples):
            y[i] = Am1 * sin(2 * pi * Fs1 * i/samples) + Am2 * sin(2 * pi * Fs2 * i/samples)
        # set range
        self.axes.set_xlim(0, section)
        self.axes.set_ylim(min(y) - 1, max(y) + 1)
        # create a plot
        self.axes.plot(y)
        self.draw()

        return y

    def configureAxes(self):
        self.axes.set_title("Generated Signal", size=13)
        self.axes.set_ylabel("Magnitude")
        self.axes.set_xlabel("Samples")
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(-1, 1)
        self.axes.grid(True)

    def cleanAxes(self):
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        self.draw()


class FilteredSignalPlot(FigureCanvasQTAgg):
    """

    Parameters
    ----------
    `parent` : master widget
        Represents a widget to act as the parent of the current object
    """

    def __init__(self, parent=None, width=5, height=2, dpi=70):
        # create the Figure
        fig = Figure(figsize=(width, height), dpi=dpi)   # figsize - in inch
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        self.axes = fig.add_subplot(111)
        self.configureAxes()
        self.axes.plot([1, 2, 3], [1, 2, 3])
        self.draw()

    def plot(self, order=10, lowcut=0.05, highcut=10, filtrType="highpass", samplingRate=1000, section=1000, unfilteredSig=None):
        """Draw filtered signal."""
        # clear current plot
        self.axes.clear()
        self.configureAxes()


        if filtrType == "highpass":
            filtered_sine = self.butter_highpass_filter(data=unfilteredSig, cutoff=highcut, fs=samplingRate)
            # butterArray = butter(order, highcut, btype=filtrType, fs=samplingRate, output='sos', analog = False)
        # elif filtrType == "lowpass":
        #     butterArray = butter(order, lowcut, btype=filtrType, fs=samplingRate, output='sos', analog = False)
        # elif filtrType == "bandpass":
        #     butterArray = butter(order, [lowcut, highcut], btype=filtrType, fs=samplingRate, output='sos', analog = False)
        # elif filtrType == "bandstop":
        #     butterArray = butter(order, [lowcut, highcut], btype=filtrType, fs=samplingRate, output='sos', analog = False)
        

        # # set range
        self.axes.set_xlim(0, section)
        self.axes.set_ylim(min(filtered_sine) - 1, max(filtered_sine) + 1)

        # create a plot
        self.axes.plot(range(len(filtered_sine)), filtered_sine)
        self.draw()

    def butter_highpass(self, cutoff, fs, order=5):
        # Nyquist frequency | f = f / (fs/2) 
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y

    def configureAxes(self):
        self.axes.set_title("Filtered Signal", size=13)
        self.axes.set_ylabel("Magnitude")
        self.axes.set_xlabel("Samples")
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(-1, 1)
        self.axes.grid(True)

    def cleanAxes(self):
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        self.draw()
