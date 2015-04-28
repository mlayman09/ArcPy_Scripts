###Script developed by Matt Layman###
###Deviation survey conversion to 3D features###
###MS Project, Spring 2015###

###This script takes a deviation survey CSV file, and converts it into a 3D feature class
###that can be viewed in ArcScene. A deviation survey is a collection of points measured
###in oil and gas wells with depth values, coordinates, etc. Using these points, one can
###map the exact location of a wellbore below the surface.

##import the arcpy module, set the workspace to a user-defined geodatabase, and allow overwriting of data

import arcpy
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

######################################################################################################################################################################

##The following lines of code are the input variables, description of each will be written in a comment the right of each one

inputCSV = arcpy.GetParameterAsText(1)   ##the input deviation survey CSV file
xField = arcpy.GetParameterAsText(2)     ##the field in that CSV that contains X coordinate values
yField = arcpy.GetParameterAsText(3)     ##the field in that CSV that contains Y coordiate values
prj = arcpy.GetParameterAsText(4)        ##the projection file used to project the CSV points, this should be the projection you want the end features to be in
inputDEM = arcpy.GetParameterAsText(5)   ##the input DEM for the area in which the CSV points fall
UWI = arcpy.GetParameterAsText(6)        ##the unique well identifier field in the deviation survey CSV
output = arcpy.GetParameterAsText(7)     ##the name for the output (3d line features) of the script

######################################################################################################################################################################

##The following lines of code execute the necessary geoprocessing tools

##Plot the points from the CSV file
arcpy.MakeXYEventLayer_management(inputCSV,xField,yField,"layer",prj)
print arcpy.GetMessages()

##Copy those features to a new file
arcpy.CopyFeatures_management("layer","points")
print arcpy.GetMessages()

##For each point, get the elevation value from the DEM and add it to a field
arcpy.sa.ExtractValuesToPoints("points",inputDEM,"points_elev")
print arcpy.GetMessages()

##Add a field ("New_Depth") to hold the values for the actual elevation of each point
arcpy.AddField_management("points_elev","New_Depth","DOUBLE")
print arcpy.GetMessages()

##Calculate that field with the expression as seen in the code. Convert the rastervalu field to feet from meters, and subtract the true vertical depth
arcpy.CalculateField_management("points_elev","New_Depth",'(!RASTERVALU!*3.28084) - !TVD!', "PYTHON")
print arcpy.GetMessages()

##Make the "points_elev" file 3D by the "New_Depth" field
arcpy.FeatureTo3DByAttribute_3d("points_elev","points_converted","New_Depth")
print arcpy.GetMessages()

##Convert the 3D points created in the tool above to 3D lines
arcpy.PointsToLine_management("points_converted",output,UWI)
print arcpy.GetMessages()









