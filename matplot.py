
import pylab
import numpy as Math
import random


def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    discardHeader = dataFile.readline()
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (distances, masses)

# ------------------------------------------------------
# ----------------Figure 1: lines and numpy-------------
# ------------------------------------------------------

# Create figure 1
# pylab.figure(1)
# t = Math.arange(0., 5., 0.1)
# line1, line2, line3 = pylab.plot(t, t, t, t**2, t, t**3)
# pylab.axis([0, 2, 0, 2])
#
# pylab.setp(line1, color='r', linewidth=1.0, linestyle='--',antialiased=True)
# pylab.setp(line2, color='g', linewidth=1.0, linestyle='--',antialiased=True)
# pylab.setp(line3, color='b', linewidth=1.0, linestyle='--',antialiased=True)

# -------------------------------------------------
# ----------------Figure 2: sub plot---------------
# -------------------------------------------------

# def f(t):
#     """
#     t: a numpy array instance
#     """
#     return Math.exp(-t) * Math.cos(2*Math.pi*t)
#
# def fexp(t):
#     """
#     t: a numpy array instance
#     """
#     return Math.exp(t) * Math.cos(2*Math.pi*t)
#
# t1 = Math.arange(0.0, 5.0, 0.1)
# t2 = Math.arange(0.0, 5.0, 0.02)
#
# # Create figure 2
# pylab.figure(2)
#
# # Create sub plot in figure 2, 211 means: 2 row, 1 colum, 1th position
# pylab.subplot(311)
# pylab.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
#
# pylab.subplot(312)
# pylab.plot(t1, fexp(t1), 'go', t2, fexp(t2), 'k')
#
# # Create sub plot
# pylab.subplot(313)
# pylab.plot(t2, Math.cos(2*Math.pi*t2), 'r--')

# -----------------------------------------------------------------
# ------------------Figure 3: text and histogram-------------------
# -----------------------------------------------------------------

# mu, sigma = 100, 15
# x = mu + sigma * Math.random.randn(10000)
#
# # The histogram of the data
# pylab.figure(3)
# n, bins, patches = pylab.hist(x, 100, normed=1, facecolor='g', alpha=0.75)
# pylab.xlabel('Smarts')
# pylab.ylabel('Probability')
# pylab.title('Histogram of IQ')
# # pylab.text(x, y, ...) x,y is position of the text
# pylab.text(60, .025, r'$\mu=100, \ \sigma=15$')
# pylab.axis([40, 160, 0, 0.03])
# pylab.grid(True)
# ----------------------------------------------------------------
# ---------------------Figure 4: Annotations ---------------------
# ----------------------------------------------------------------

# ax = pylab.subplot(111)
# t = Math.arange(0.0, 5.0, 0.01)
# s = Math.cos(2*Math.pi*t)
# line, = pylab.plot(t, s, lw=2)
#
# # xy is the arrow tip, xytext is the text location
# pylab.annotate('Local max', xy=(2,1), xytext=(3, 1.5),
#            arrowprops=dict(facecolor='black', shrink=0.05),)
# pylab.ylim(-2, 2)

# -------------------------------------------------------------------------
# ---------------Figure 5: Logarithmic and other nonlinear axis------------
# -------------------------------------------------------------------------

# Make up some data in the interval [0, 1]
# y = Math.random.normal(loc=0.8, scale=0.4, size=1000)
# y = y[(y > 0) & (y < 1)]
# y.sort()
# x = Math.arange(len(y))
#
# pylab.figure(5)
#
# # linear
# pylab.subplot(221)
# pylab.plot(x,y)
# pylab.yscale('linear')
# pylab.title('Linear')
# pylab.grid(True)
#
# # log
# pylab.subplot(222)
# pylab.plot(x,y)
# pylab.yscale('log')
# pylab.title('Log')
# pylab.grid(True)
#
# # symmetirc log
# pylab.subplot(223)
# pylab.plot(x, y - y.mean())
# pylab.yscale('symlog', linthreshy=0.05)
# pylab.title('symlog')
# pylab.grid(True)
#
# # logit
# pylab.subplot(224)
# pylab.plot(x, y)
# pylab.yscale('logit')
# pylab.title('Logit')
# pylab.grid(True)

# ----------------------------------------------
# ---------------Figure 6: Legend---------------
# ----------------------------------------------

def fitData(fileName):
    yVals, xVals = getData(fileName)
    xVals = Math.array(xVals)
    yVals = Math.array(yVals)
    xVals = xVals * 9.81
    pylab.plot(xVals, yVals, 'ro', label = 'Measured displacements')
    pylab.title('Measured displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')
    a, b, c = pylab.polyfit(xVals, yVals, 2)
    estYVals = a * xVals **2 + b * xVals + c
    k = 1/a
    pylab.plot(xVals, estYVals, label = 'Linear fit, k=' + str(round(k, 5)))
    pylab.legend(loc = 'best')

# fitData('springData.txt')

# ----------------------------------------------------------
# ----------------Figure 7: Axis limitation-----------------
# ----------------------------------------------------------
def stdDev(X):
    """
    standard deviation: square root of the sum of the (x - mean)^2
    :param X: a list of numerical values
    :return: a float which is the standard deviation
    """
    mean = sum(X) / float(len(X))
    total = 0.0
    for x in X:
        total += (x - mean)**2
    return (total/len(X)) ** 0.5

def flip(numflips):
    heads = 0.0
    for i in range(numflips):
        if random.random() < 0.5:
            heads += 1.0
    return heads / numflips


def flipSim(numflipPerTrial, numTrials):
    fracOHeads = []
    for i in range(numTrials):
        fracOHeads.append(flip(numflipPerTrial))
    return fracOHeads


def labelPlot(nf, nt, mean, sd):
    pylab.title(str(nt) + ' trials of' + str(nf) + ' flips each')
    pylab.xlabel('Fraction of Heads')
    pylab.ylabel('Number of Trials')
    xmin, xmax = pylab.xlim()
    ymin, ymax = pylab.ylim()
    pylab.text(xmin + (xmax - xmin) * 0.02, (ymax - ymin)/2,
               'Mean = ' + str(round(mean, 6))
               + '\nSD = ' + str(sd))

def makePlots(nf1, nf2, nt):
    """
    :param nf1: number of flips 1st experiment
    :param nf2:  number of flips 2st experiment
    :param nt: number of trials per experiment
    :return: None
    """
    fracHeads = flipSim(nf1, nt)
    mean1 = sum(fracHeads)/float(len(fracHeads))
    sd1 = stdDev(fracHeads)
    pylab.hist(fracHeads, 20)
    xmin, xmax = pylab.xlim()
    ymin, ymax = pylab.ylim()
    labelPlot(nf1, nt, mean1, sd1)

    pylab.figure()
    fracHeads2 = flipSim(nf2, nt)
    mean2 = sum(fracHeads2) / float(len(fracHeads2))
    sd2 = stdDev(fracHeads2)
    pylab.hist(fracHeads2, 20)
    pylab.xlim(xmin, xmax)
    labelPlot(nf2, nt, mean2, sd2)

makePlots(100, 1000, 10000)

pylab.show()
