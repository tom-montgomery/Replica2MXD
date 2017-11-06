# Replica2MXD
Creates MXD files from enterprise geodatabase replicas containing all feature classes and tables. Use when re-creating
replicas or for quickly checking replica contents.

After having created numerous MXDs to define which feature classes are included in a replica, I decided to automate it.
Use a list of fully qualified replica names for the replica_list variable or use the keyword "ALL" to create MXD files for 
all replicas in the enterprise geodatabase of interest.
