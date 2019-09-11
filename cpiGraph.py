import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

# Equation to extrapolate theoretical data
def func(x,a,b):
	return a*x**b

# Get data into pandas Data Frame
def getData():
	BAE = pd.read_csv("BAE.csv")
	interComparison = pd.read_csv("intercomparison.csv")
	dropSondes = pd.read_csv("dropsonde.csv")
	theoretical = pd.read_csv("theoretical.csv").sort_values(by="MACH")
	return(BAE, interComparison, dropSondes,theoretical)

# Make event markers
def eventMarkers(interComparison):
	altitudes = [0,1500,4000,10000] #m
	flightLevel = [40,100,150] #1000ft
	comparisonMarkerX = []
	comparisonMarkerY = []
	comparisonMarkerError = []
	for i in range(len(altitudes)-1):
		FL = interComparison[(interComparison["ALT_GIN"] > altitudes[i]) & (interComparison["ALT_GIN"] < altitudes[i+1])]
		comparisonMarkerX.append(np.average(FL["MACH"]))
		comparisonMarkerY.append(np.average(FL["CPI"]))
		comparisonMarkerError.append(np.std(FL["CPI"]))
	return(comparisonMarkerX, comparisonMarkerY, comparisonMarkerError)

# plot data
def plotData(baeCorrec, intercomparisonCorrec, dropsondeCorrec, theoreticalCorrec, comparisonMarkerX,comparisonMarkerY,comparisonMarkerError,params):
	plt.scatter(baeCorrec["mach"],baeCorrec["CPI"], c="green", label = "-903 Correction Law", zorder=12, alpha = 0.5)
	plt.scatter(dropsondeCorrec["mach"],dropsondeCorrec["CPI"], c="red", label="Drop Sonde extrapolation", zorder=11, alpha = 0.5)
	# Plot dummy data point for legend
	plt.scatter(0,0, c= "black", alpha = 1, label= "Intercomparison")
	for i in range(len(comparisonMarkerX)):
		plt.scatter(comparisonMarkerX[i], comparisonMarkerY[i], c = "black", zorder=10)
		plt.errorbar(comparisonMarkerX[i], comparisonMarkerY[i], yerr = comparisonMarkerError[i], c = "black", capsize=6, elinewidth=1, markeredgewidth=1)
	# Plot theoretical with +0.01 fudge factor to get more accurate fit
	plt.plot(theoreticalCorrec["MACH"], func(theoreticalCorrec["MACH"], params[0], params[1]) + 0.01,
         label='Theoretical curve', c= "black")
	# Graph paramaters
	plt.title("Empirical correction to static pressure in the S2 port of the ARA")
	plt.xlabel("Mach number []")
	plt.ylabel("CPI []")
	plt.legend(loc = "upper left")
	plt.minorticks_on()
	plt.grid(which="major", linestyle="-", linewidth="0.5", color="cyan")
	plt.grid(which="minor", linestyle="--", linewidth="0.4", color="cyan")
	plt.xlim(0.2,0.9)
	plt.show()

# Get data
baeCorrec, intercomparisonCorrec, dropsondeCorrec, theoreticalCorrec = getData()
# Average data into event markers for comparison
comparisonMarkerX, comparisonMarkerY, comparisonMarkerError = eventMarkers(intercomparisonCorrec)
# Optimize best fit equation for theoretical curve
params, params_covariance = optimize.curve_fit(func, theoreticalCorrec["MACH"], theoreticalCorrec["CPI"])
# Plot data
plotData(baeCorrec, intercomparisonCorrec, dropsondeCorrec, theoreticalCorrec, comparisonMarkerX,comparisonMarkerY,comparisonMarkerError,params)




