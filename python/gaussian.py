from scipy import signal
from scipy.fftpack import fft, fftshift
from scipy.interpolate import spline
import matplotlib.pyplot as plt 
import numpy as np
# window = signal.gaussian(62, std=7, sym=True)
# plt.plot(window)
# plt.title(r"Gaussian window ($\sigma$=7)")
# plt.ylabel("Amplitude")
# plt.xlabel("Sample")
# plt.show()

plt.close('all')
plt.figure()
mu, sigma, c, bin = 13, 3, 1e4, 99 # mean and standard deviation
s = np.random.normal(mu, sigma, c)
count, bins, ignored = plt.hist(s, bin, normed=True)
f = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) )
plt.plot(bins, f, linewidth=2, color='b')
plt.show()


mu, sigma = 26, 7 # mean and standard deviation
s = np.random.normal(mu, sigma, c)
count, bins, ignored = plt.hist(s, bin, normed=True)
g = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) )
plt.plot(bins, g, linewidth=2, color='r')
plt.show()


mu, sigma = 62, 13 # mean and standard deviation
s = np.random.normal(mu, sigma, c)
count, bins, ignored = plt.hist(s, bin, normed=True)
h = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) )
plt.plot(bins, h, linewidth=2, color='k')
plt.show()

plt.figure()
b100 = np.linspace( 0, 100, 101 )
mu = [ 13, 26, 62 ]
sigma = [ 3, 7, 13 ]
pr = 1/(sigma[0] * np.sqrt(2 * np.pi)) * np.exp( - (b100 - mu[0])**2 / (2 * sigma[0]**2) )
gd = 1/(sigma[1] * np.sqrt(2 * np.pi)) * np.exp( - (b100 - mu[1])**2 / (2 * sigma[1]**2) )
ce = 1/(sigma[2] * np.sqrt(2 * np.pi)) * np.exp( - (b100 - mu[2])**2 / (2 * sigma[2]**2) )
plt.plot(b100, pr, linewidth=2, color='r')
plt.plot(b100, gd, linewidth=2, color='b')
plt.plot(b100, ce, linewidth=2, color='k')

# print( np.shape( f ), np.shape( g ), np.shape( h ) )
# dist_hist_bins = np.linspace( 0, 100, 21 )
# dist_hist = []
# 
for index, bin in np.ndenumerate(b100):
    for i in 
    print(bin,pr[index])

normal_hist_bins = np.linspace( 0, 95, 20 )
normal_hist_pr, normal_hist_gd, normal_hist_ce = [], [], []
for i in normal_hist_bins:
    # print( i, i+5, np.sum(pr[i:i+5]) )
    global normal_hist_pr, normal_hist_gd, normal_hist_ce
    normal_hist_pr.append( np.sum(pr[i:i+5]) )
    normal_hist_gd.append( np.sum(gd[i:i+5]) )
    normal_hist_ce.append( np.sum(ce[i:i+5]) )

plt.figure()
normal_hist_x=np.linspace(0,19,20)
plt.plot( normal_hist_bins, normal_hist_pr )
plt.plot( normal_hist_bins, normal_hist_gd )
plt.plot( normal_hist_bins, normal_hist_ce )
plt.bar( normal_hist_bins, normal_hist_pr, color='b' )
plt.bar( normal_hist_bins, normal_hist_gd, color='green' )
plt.bar( normal_hist_bins, normal_hist_ce, color='r' )
    # global dist_hist
    # if channel >= dist_hist_bins[0] and channel < dist_hist_bins[1]:
    #     dist_hist[0] = h[ind]