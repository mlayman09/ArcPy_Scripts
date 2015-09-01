import arcpy
arcpy.env.workspace = "C:/Users/Matt Layman/Downloads/activities"
arcpy.env.overwriteOutput = True

list = arcpy.ListFiles()
print list

for f in list:
    arcpy.GPXtoFeatures_conversion(f,f + ".shp")
    print arcpy.GetMessages()

newlist = arcpy.ListFiles("*.shp")
arcpy.Merge_management(newlist,"merge_shp")
arcpy.MakeFeatureLayer_management("merge_shp.shp","merge_lyr")
arcpy.LayerToKML_conversion("merge_lyr","activities.kmz")

