# Replica2MXD
Adds all feature classes contained in a specific enterprise geodatabase replica to an already created mxd file.

After having created numerous MXDs to define which feature classes are included in a replica, I decided to automate it.
I could not figure out how to auto create MXD files using arcobjects to really automate the whole process, so for now
this module only supports adding replica feature classes to a single mxd at a time. Hopefully in the future it will be
possible to simply point to a SDE and create MXD files of all the replicas.
