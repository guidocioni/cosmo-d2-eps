import numpy as np
import matplotlib.pyplot as plt
from reader import read_coordinates, read_dates, read_variable, read_variable_xr
from config import folder_images, get_projection

# Get coordinates 
lats, lons = read_coordinates()
time=read_dates()

# Read variables from files and time, this is common to all the script
clct=read_variable_xr(variable='clct').TCDC_P1_L1_GRLL0


fig = plt.figure(figsize=(8,10))
m = get_projection("germany", regions=True)
x, y = m(lons,lats)

first = True 
threshold=50.
probabilities = (np.sum(clct[:,:,:,:] < threshold, axis=1)/20.)*100.

for i, date in enumerate(time):
    cs = m.contourf(x, y, probabilities[i,:,:], np.linspace(0,100,10), cmap=plt.cm.gist_stern_r, extend='both')

    plt.title('Probability cloud cover<'+str(int(threshold))+' %| '+date.strftime('%d %b %Y at %H UTC'))
    if first: # Apparently it only needs to be added once...
        plt.colorbar(cs, orientation='horizontal', label='Probability [%]',fraction=0.046, pad=0.04)
    plt.savefig(folder_images+'prob_clct_%s_%s.png' % (int(threshold), date.strftime('%Y%m%d%H')),
                dpi=150, bbox_inches='tight')
    first=False

plt.close('all')
