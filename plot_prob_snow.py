# Plots the probability of snow vs. rain

import numpy as np
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reader import *
from config import *
import pandas as pd

# Read variables from files and time, this is common to all the script
ds = read_variable_xr(variable='prs_gsp')
ds1 = read_variable_xr(variable='tot_prec')

lats, lons = ds.latitude.data, ds.longitude.data
time= pd.to_datetime(ds.valid_time.data)
cum_hour=np.array((time-time[0]) / pd.Timedelta('1 hour')).astype("int")

snow = ds.lssrwe*3600.

# We have to load the array into memory since there are problems with the indexing in Dask...
tot_prec = ds1['tp'].load()*0.
for i in range(1, len(time)):
    tot_prec[i,:,:,:] = ds1.tp[i,:,:,:]-ds1.tp[i-1,:,:,:]
tot_prec_mean = tot_prec.mean(axis=1)

threshold = 0.01 # this should be in mm/h of equivalent snow height

# Truncate colormap
cmap = plt.get_cmap('gist_stern_r')
new_cmap = truncate_colormap(cmap, 0, 0.9)

# Germany plots
fig = plt.figure(figsize=(8,10))
m = get_projection("germany", regions=True)
x, y = m(lons,lats)

first = True 

probabilities = (np.sum(snow > threshold, axis=1)/20.)*100.

for i, date in enumerate(time):
    cs = m.contourf(x, y, probabilities[i,:,:], np.linspace(10,100,10),
                     cmap=new_cmap, alpha=0.85)
    cr = m.contourf(x, y, tot_prec_mean[i,:,:], levels=(0.1, 1.),
                    colors='none', hatches=['...','...'], extend='max')

    plt.title('Probability snowfall & tot. prec > 0.1 mm h$^{-1}$ | '+date.strftime('%d %b %Y at %H UTC'))
    annotation_run(plt.gca(), time)
    annotation(plt.gca(), text='COSMO-D2-EPS', loc='upper left')
    if first: # Apparently it only needs to be added once...
        plt.colorbar(cs, orientation='horizontal', label='Probability [%]',fraction=0.04, pad=0.04)
    plt.savefig(folder_images+'prob_snow_prec_%s.png' %  cum_hour[i],
                dpi=dpi_resolution, bbox_inches='tight')
    for coll in cs.collections: 
        coll.remove()
    for coll in cr.collections: 
        coll.remove()
    first=False

plt.close('all')

# Italy plots
fig = plt.figure(figsize=(10,7))
m = get_projection("italy", regions=True)
x, y = m(lons,lats)

first = True 

probabilities = (np.sum(snow > threshold, axis=1)/20.)*100.

for i, date in enumerate(time):
    cs = m.contourf(x, y, probabilities[i,:,:], np.linspace(10,100,10),
                     cmap=new_cmap, alpha=0.85)
    cr = m.contourf(x, y, tot_prec_mean[i,:,:], levels=(0.1, 1.),
                    colors='none', hatches=['...','...'], extend='max')

    plt.title('Probability snowfall & tot. prec > 0.1 mm h$^{-1}$ | '+date.strftime('%d %b %Y at %H UTC'))
    annotation_run(plt.gca(), time)
    annotation(plt.gca(), text='COSMO-D2-EPS', loc='upper left')
    if first: # Apparently it only needs to be added once...
        plt.colorbar(cs, orientation='horizontal', label='Probability [%]',fraction=0.04, pad=0.04)
    plt.savefig(folder_images+'it/prob_snow_prec_%s.png' %  cum_hour[i],
                dpi=dpi_resolution, bbox_inches='tight')
    for coll in cs.collections: 
        coll.remove()
    for coll in cr.collections: 
        coll.remove()
    first=False

plt.close('all')