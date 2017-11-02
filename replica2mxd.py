"""Adds all feature classes contained in a specific replica to an already created mxd file."""
import os
import xml.etree.ElementTree as ET


import arcpy


def replica2mxd(gdb, mxd, replica):
    """Adds feature classes to an already created MXD for the replica or enterprise geodatabase specified.
        gdb(Text):
         full path to the geodatabase connection file containing the replica of interest

        mxd(Text):
         full path to already created mxd to add replica feature classes to. Should have same name as replica.

        replica(Text):
         full name including schema of replica of interest. Example: 'PCGDO.ZipcodeNP1' """
    replica_objs = arcpy.da.ListReplicas(gdb)
    feature_classes, replicas = [], []
    xml = os.path.dirname(mxd)+'\\replica.xml'

    for r in replica_objs:
        replicas.append(r.name)
    if replica in replicas:
        arcpy.da.ExportReplicaSchema_management(gdb, xml, replica)
        tree = ET.parse(xml)
        root = tree.getroot()
        for dataset in root[0][4][12][3]:
            feature_classes.append(dataset.find('DatasetName').text)
    else:
        print "Replica '{0}' not found in {1}".format(replica, gdb)

    mxd = arcpy.mapping.MapDocument(mxd)
    df = mxd.activeDataFrame
    for fc in feature_classes:
        layer = arcpy.mapping.Layer("{0}\\{1}".format(gdb,fc))
        arcpy.mapping.AddLayer(df, layer, "TOP")

    os.remove(xml)
