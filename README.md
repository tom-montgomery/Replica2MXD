# Replica2MXD
Creates MXD files from enterprise geodatabase replicas containing all feature classes and tables. Use when re-creating
replicas or for quickly checking replica contents.

After having created numerous MXDs to define which feature classes are included in a replica, I decided to automate it.
Use a list of fully qualified replica names for the replica_list variable or use the keyword "ALL" to create MXD files for 
all replicas in the enterprise geodatabase of interest.


# Installation and Usage:
Download and extract Zip file then copy replica2mxd.py to your Python Lib folder.(C:\Python27\ArcGISx6410.3\Lib)
Use in python by importing:

```import replica2mxd as r2m```

Call function and use by passing the geodatabase connection, MXD output folder, and replica name(s) as parameters:
Use 'ALL' keyword for replicas parameter to create MXD files for all replicas in geodatabase:
  
```r2m.replica2mxd('Database Connections\\example-gis-server@gisDatabase@sde.sde', 'C:\\Replicas\\MXDs', 'ALL')```

Or use a list of replica names to create MXD files for only those replicas. Must include replica owner in replica names:
  
```r2m.replica2mxd('Database Connections\\example-gis-server@gisDatabase@sde.sde', 'C:\\Replicas\\MXDs', ['SDE.Replica1', 'SDE.Replica2', ...])```
