# Configuration file for some common variables to all script 
from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit
import numpy as np
from matplotlib.offsetbox import AnchoredText
import matplotlib.colors as colors
from matplotlib.colors import from_levels_and_colors
import seaborn as sns

# Output folder for images 
folder_images = "/scratch/local1/m300382/cosmo_d2_eps/"
# Resolution of images 
dpi_resolution = 100

def get_projection(projection="germany", countries=True, regions=False, labels=False):
    if projection=="germany":
        m = Basemap(projection='cyl', llcrnrlon=5, llcrnrlat=46,\
               urcrnrlon=16, urcrnrlat=56,  resolution='i')
        m.drawcoastlines()
        if countries:
            m.drawcountries()
        if regions:
            m.readshapefile('/home/mpim/m300382/shapefiles/DEU_adm_shp/DEU_adm1',
                            'DEU_adm1',linewidth=0.2,color='black')
        if labels:
            m.drawparallels(np.arange(-80.,81.,10), linewidth=0.2, labels=[True, False, False, True])
            m.drawmeridians(np.arange(-180.,181.,10), linewidth=0.2, labels=[True, False, False, True])
        img=m.arcgisimage(service='World_Shaded_Relief', xpixels = 1000, verbose= True)
        img.set_alpha(0.8)

    elif projection=="italy":
        m = Basemap(projection='cyl', llcrnrlon=5, llcrnrlat=43.5,\
               urcrnrlon=15, urcrnrlat=48,  resolution='i')
        m.drawcoastlines()
        if countries:
            m.drawcountries()
        if regions:
            m.readshapefile('/home/mpim/m300382/shapefiles/ITA_adm_shp/ITA_adm1',
                            'ITA_adm1',linewidth=0.2,color='black')
        if labels:
            m.drawparallels(np.arange(-80.,81.,10), linewidth=0.2, labels=[True, False, False, True])
            m.drawmeridians(np.arange(-180.,181.,10), linewidth=0.2, labels=[True, False, False, True])
        img=m.arcgisimage(service='World_Shaded_Relief', xpixels = 1000, verbose= True)
        img.set_alpha(0.8)
             
    return(m)

# Annotation run, models 
def annotation_run(ax, time, loc='upper right'):
    at = AnchoredText('Run %s'% time[0].strftime('%Y%m%d %H UTC'), 
                      prop=dict(size=8), frameon=True, loc=loc)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.1")
    ax.add_artist(at)

def annotation(ax, text, loc='upper right'):
    at = AnchoredText('%s'% text, prop=dict(size=8), frameon=True, loc=loc)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.1")
    ax.add_artist(at)
    
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap