"""Creates MXD files from enterprise geodatabase replicas containing all feature classes and tables. Use when re-creating
replicas or for quickly checking replica contents."""
import os
import xml.etree.ElementTree as ET
import shutil


import arcpy


def replica2mxd(gdb, mxd_dir, replica_list):
    """Adds replica feature classes and tables to a copy of a template MXD for the replica or enterprise geodatabase
    specified. Temporarily creates a XML file in the target mxd directory.

        gdb(Text):
         Full path to the geodatabase connection file containing the replica of interest

        mxd_dir(Text):
         Full path to an existing directory where the replica MXD files will be created.

        replica_list(List OR Text):
         List containing fully qualified replica name(s) of interest. Example: 'SDE.ReplicaName'.
         Use the value 'ALL' to create MXD files for all replicas in geodatabase."""
    arcpy.env.overwriteOutput = True
    replica_objects = arcpy.da.ListReplicas(gdb)
    replicas = []
    # Convert replica objects to list of replica names.
    for r in replica_objects:
        replicas.append(r.name)

    # If ALL keyword used created MXDs for all replicas in geodatabase.
        if replica_list == 'ALL':
            for replica in replicas:
                convert2mxd(replica, replicas, mxd_dir, gdb)
        else:
            for replica in replica_list:
                if replica in replicas:
                    convert2mxd(replica, replicas, mxd_dir, gdb)


def convert2mxd(replica, replicas, mxd_dir, gdb):
    """Copies template MXD and renames to replica name then converts replica in replica list to xml and parses datasets.
    Cleans up target directory.

        replica(Text):
         Fully qualified replica name.

        replicas(List):
         List of fully qualified replica names as text.

        mxd_dir(Text):
         Full path to directory where MXD files will be saved.

        gdb(Text):
         Database connection file which contains the replicas of interest."""
    arcpy.env.overwriteOutput = True

    feature_classes = []
    mxd = '{0}\\{1}.mxd'.format(mxd_dir, replica.split('.')[-1])
    install_dir = arcpy.GetInstallInfo()['InstallDir']

    # Make copy of the template MXD and give replica's name
    shutil.copy(
        '{0}MapTemplates\\Standard Page Sizes\\ISO (A) Page Sizes\\ISO A0 Portrait.mxd'.format(install_dir),
        mxd)

    # If the replica can be found in the geodatabase, export it's schema as xml and parse dataset names.
    if replica in replicas:
        xml = os.path.dirname(mxd_dir) + '\\{0}.xml'.format(replica)
        arcpy.ExportReplicaSchema_management(gdb, xml, replica)
        tree = ET.parse(xml)

        for elem in tree.iter():
            if elem.tag == "DatasetName":
                feature_classes.append(elem.text)
        mxdobj = arcpy.mapping.MapDocument(mxd)
        df = mxdobj.activeDataFrame

        # Add datasets to the copied MXD file.
        for fc in feature_classes:
            desc = arcpy.Describe("{0}\\{1}".format(gdb, fc))
            if desc.dataType == u'Table':
                tbl = arcpy.mapping.TableView("{0}\\{1}".format(gdb, fc))
                arcpy.mapping.AddTableView(df, tbl)
            elif desc.dataType == u'FeatureClass':
                layer = arcpy.mapping.Layer("{0}\\{1}".format(gdb, fc))
                arcpy.mapping.AddLayer(df, layer, "TOP")
            else:
                pass

        mxdobj.save()
        os.remove(xml)

    else:
        print "Replica '{0}' not found in {1}".format(replica, gdb)
