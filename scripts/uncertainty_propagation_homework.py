import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy
from uncertainties import ufloat, unumpy

def plot(x_graph, y_graph, y_err, x_fit, y_fit, y_fit_lower, y_fit_upper, xlabel, filename, ylabel=r"C [$\mu$F]"):

    # draw x_graph, y_graph with error bars
    plt.errorbar(x_graph, y_graph, y_err, fmt='o', label='Data', color='black')

    # draw the fit function and its uncertainty band
    plt.fill_between(x_fit, y_fit_lower, y_fit_upper, color='red', alpha=0.3)

    # create a legend entry for the fit function and its uncertainty band
    line_with_band = mpl.lines.Line2D([], [], color='red', label='Fit', linestyle='-', linewidth=2)
    band = mpl.patches.Patch(color='red', alpha=0.3, label='Fit uncertainty')

    # get the current legend handles and labels
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles=handles + [(line_with_band, band)], labels=labels + ['Fit'])

    # finally, plot
    plt.plot(x_fit, y_fit, 'r-')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    plt.close()

    return

def const_func(x, a):
    return a

y = unumpy.uarray([41.2, 39.6, 36.3, 33, 26.3, 16.6], 0.5) / 100
m = unumpy.uarray([150, 200, 300, 400, 600, 900], 0) / 1000
y_m0 = ufloat(46.4, 0.5) / 100
y0 = y_m0 - y

t0 = unumpy.uarray([0.28, 0.48, 0.56, 0.48, 0.24, 0.20], 0.04)
tn = unumpy.uarray([9.32, 9.84, 9.44, 14.32, 13.56, 13.12], 0.04)
n  = unumpy.uarray([20, 18, 14, 19, 15, 12], 0)
T = (tn - t0) / n
T2 = T**2
g = 4 * np.pi**2 * y0 / T2

# fit T2 vs y0, resulting in g/(4*pi**2)
popt, pcov = scipy.optimize.curve_fit(lambda x, a: a,
                                      np.linspace(0, 5, 6),
                                      unumpy.nominal_values(g), 
                                      sigma=unumpy.std_devs(g), 
                                      absolute_sigma=True)
print(popt[0], '+-', np.sqrt(pcov[0,0]))

# plot the data and the fit
xfit = np.linspace(0, 5, 100)
# create numpy array with 100 identical values of popt[0]
yfit = np.full(100, popt[0])
yfit_lower = np.full(100, popt[0] - np.sqrt(pcov[0,0]))
yfit_upper = np.full(100, popt[0] + np.sqrt(pcov[0,0]))
plot(np.linspace(0, 5, 6), unumpy.nominal_values(g), unumpy.std_devs(g), 
    xfit, yfit, yfit_lower, yfit_upper, "measurement number", "uncertainty_propagation/homework.png", ylabel=r"$g$ [m/s$^2$]")
