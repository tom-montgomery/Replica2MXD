"""Adds all feature classes contained in a specific replica to an already created mxd file."""
import os
import xml.etree.ElementTree as ET


import arcpy
arcpy.env.overwriteOutput = True


def replica2mxd(gdb, mxd, replica):
    """Adds feature classes to an already created MXD for the replica or enterprise geodatabase specified. Temporarily
    Creates a XML file in the target mxd directory.
        gdb(Text):
         full path to the geodatabase connection file containing the replica of interest

        mxd(Text):
         full path to already created mxd to add replica feature classes to. Should have same name as replica.

        replica(Text):
         full name including schema of replica of interest. Example: 'SDE.ReplicaName' """
    replica_objs = arcpy.da.ListReplicas(gdb)
    feature_classes, replicas = [], []
    xml = os.path.dirname(mxd)+'\\replica.xml'

    for r in replica_objs:
        replicas.append(r.name)
    if replica in replicas:
        arcpy.ExportReplicaSchema_management(gdb, xml, replica)
        tree = ET.parse(xml)
        for elem in tree.iter():
            if elem.tag == "DatasetName":
                feature_classes.append(elem.text)
    else:
        print "Replica '{0}' not found in {1}".format(replica, gdb)

    mxdo = arcpy.mapping.MapDocument(mxd)
    df = mxdo.activeDataFrame
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
    mxdo.save()
    os.remove(xml)

# replica2mxd()