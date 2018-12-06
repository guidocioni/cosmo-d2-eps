# Suite of interfaces to read the grib2 data of ICON-EPS
#
import pygrib # import pygrib interface to grib_api
import numpy as np 
from glob import glob
import pandas as pd
import xarray as xr #also requires pyNio to read grib files 

# Default values for reader 
main_folder='/scratch/local1/m300382/cosmo_d2_eps/'
file_prefix='cosmo-d2-eps_germany_rotated-lat-lon'
level_type='single-level'
run=''
variable='vmax_10m'

number_ensembles=20
nlat=716
nlon=651

file_coordinates='/home/mpim/m300382/cosmo_d2_eps/coord.grib2'

# This is necessary to loop through the grib messages and extract the variables
variables_names={
    't_2m'  : 'Temperature',
    'u_10m' : 'u-component of wind',
    'v_10m' : 'v-component of wind',
    'tot_prec' : 'Total precipitation rate',
    'cape_ml'  : 'Convective available potential energy',
    'vmax_10m'  : 'Wind speed'
}
variables_levels={
    't_2m'  : 2,
    'u_10m' : 10,
    'v_10m' : 10,
    'tot_prec' : 0,
    'cape_ml' : 0,
    'vmax_10m'  : 10
}

def read_coordinates(file=file_coordinates):
    "Read lat/lon coordinates from the specified file"
    grbs_coord = pygrib.open(file)
    lats = []
    lons = []
    for grb in grbs_coord:
        if grb.parameterName == 'Geographical latitude':
            lats.append(grb.values)
        elif grb.parameterName == 'Geographical longitude':
            lons.append(grb.values)
            
    return(np.array(lats)[0,:,:], np.array(lons)[0,:,:])

def read_variable(main_folder=main_folder, file_prefix=file_prefix, run=run, variable=variable, level_type=level_type,
                 date_method=False):
    """Read and concatenate variable from a list of files which is created here,
    if parameters are not provided then the deafults (here up top) will be used.
    Since data every 15 minutes are too much to be processed we first split data
    every 15 minutes with CDO and read data only every hour here. The date_method
    tries to read all the data and split according to dates but takes too much time."""
    
    if date_method:
        files= sorted(glob(main_folder+file_prefix+'_'+level_type+'_'+run+'*'+variable+'.grib2'))
        
        dates=[]
        temps = []
        
        for file in files:
            grbs = pygrib.open(file)
            for grb in grbs:
                dates.append("%d %s" % (grb['forecastTime'], grb.fcstimeunits))
                if grb.parameterName == variables_names[variable] and grb.level == variables_levels[variable]:
                    temps.append(grb.values)
                
        dates=np.array(dates)
        u, ind = np.unique(dates, return_index=True)
        dates_unique=u[np.argsort(ind)]
        time=pd.date_range(start=grb.analDate, freq='15min', periods=dates_unique.shape[0])
        
        var_ens=np.empty(shape=(0, number_ensembles, nlat, nlon), dtype=float)
        for time_ind in dates_unique:
            var_ens=np.append(var_ens, [temps[dates==time_ind]], axis=0)
    else:
        # New method which should be faster, for now uses the one from icon_eps which 
        # assumes one time step per file 
        files= sorted(glob(main_folder+file_prefix+'_'+level_type+'_'+run+'*_00_'+variable+'.grib2'))
        
        for file in files:
            temps = []
            grbs = pygrib.open(file)
            for grb in grbs:
                if grb.parameterName == variables_names[variable] and grb.level == variables_levels[variable]:
                    temps.append(grb.values)
            if file == files[0]: # This is the first file we read, so...
                #...create the variable
                var_ens=np.empty(shape=(0, number_ensembles, nlat, nlon), dtype=float)
            var_ens=np.append(var_ens, [temps], axis=0)
    
    return(var_ens) # This gives back an array with [time, number_ensembles, number_cells]

def read_variable_xr(main_folder=main_folder, file_prefix=file_prefix, run=run, variable=variable, level_type=level_type,
                    full=False):
    """Read and concatenate variable from a list of files which is created here,
    if parameters are not provided then the deafults (here up top) will be used.
    Since data every 15 minutes are too much to be processed we first split data
    every 15 minutes with CDO and read data only every hour here. This version 
    uses xarray to read the grib files. It should be more flexible."""
    
    if full:
        files= sorted(glob(main_folder+file_prefix+'_'+level_type+'_'+run+'*_'+variable+'.grib2'))
    else:
        files= sorted(glob(main_folder+file_prefix+'_'+level_type+'_'+run+'*_00_'+variable+'.grib2'))
    
    datasets = xr.open_mfdataset(files, engine="cfgrib", concat_dim="time")
    
    return(datasets)
    
def read_dates(main_folder=main_folder, file_prefix=file_prefix, run=run, full=False, variable=variable):
    "Read dates from the list of files assuming that these will be the same number"
    
    if full:
        files= sorted(glob(main_folder+file_prefix+'_'+level_type+'_'+run+'*'+variable+'.grib2'))
    else:
        files= sorted(glob(main_folder+file_prefix+'_'+level_type+'_'+run+'*_00_'+variable+'.grib2'))
    dates=[]

    for file in files:
        grbs = pygrib.open(file)
        for grb in grbs:
            dates.append(grb.validDate)          

    return(pd.to_datetime(np.unique(np.array(dates))))
