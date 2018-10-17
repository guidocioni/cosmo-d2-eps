import numpy as np
import matplotlib.pyplot as plt
from reader import read_coordinates, read_dates, read_variable, read_variable_xr
from config import folder_images, get_projection, dpi_resolution, annotation_run, annotation
import pandas as pd

# Get coordinates 
lats, lons = read_coordinates()
time=read_dates()
cum_hour=np.array((time-time[0]) / pd.Timedelta('1 hour')).astype("int")

# Read variables from files and time, this is common to all the script
h_snow=read_variable_xr(variable='h_snow').SNOD_P1_L1_GRLL0
h_snow=h_snow*100.

# Probabilites plot 
thresholds = [10., 50., 100.]

# Germany plots
fig = plt.figure(figsize=(8,10))
m = get_projection("germany", regions=True)
x, y = m(lons,lats)

first = True 
for threshold in thresholds:
    probabilities = (np.sum(h_snow[:,:,:,:] > threshold, axis=1)/20.)*100.
    
    for i, date in enumerate(time):
        cs = m.contourf(x, y, probabilities[i,:,:], np.linspace(0,100,10), cmap=plt.cm.gist_stern_r, extend='both')

        plt.title('Probability height snow>'+str(int(threshold))+' cm | '+date.strftime('%d %b %Y at %H UTC'))
        annotation_run(plt.gca(), time)
        annotation(plt.gca(), text='COSMO-D2-EPS', loc='upper left')
        if first: # Apparently it only needs to be added once...
            plt.colorbar(cs, orientation='horizontal', label='Probability [%]',fraction=0.046, pad=0.04)
        plt.savefig(folder_images+'prob_snow_%s_%s.png' % (int(threshold), cum_hour[i]),
                    dpi=dpi_resolution, bbox_inches='tight')
        first=False

plt.close('all')

# Italy plots

fig = plt.figure(figsize=(10,7))
m = get_projection("italy", regions=True)
x, y = m(lons,lats)

first = True 
for threshold in thresholds:
    probabilities = (np.sum(h_snow[:,:,:,:] > threshold, axis=1)/20.)*100.
    
    for i, date in enumerate(time):
        cs = m.contourf(x, y, probabilities[i,:,:], np.linspace(0,100,10), cmap=plt.cm.gist_stern_r, extend='both')

        plt.title('Probability height snow>'+str(int(threshold))+' cm | '+date.strftime('%d %b %Y at %H UTC'))
        annotation_run(plt.gca(), time)
        annotation(plt.gca(), text='COSMO-D2-EPS', loc='upper left')
        if first: # Apparently it only needs to be added once...
            plt.colorbar(cs, orientation='horizontal', label='Probability [%]',fraction=0.046, pad=0.04)
        plt.savefig(folder_images+'it/prob_snow_%s_%s.png' % (int(threshold), i),
                    dpi=dpi_resolution, bbox_inches='tight')
        first=False

plt.close('all')


# To be added plot of the average and standard deviation