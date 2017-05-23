import TecUtil
import TecVals

def TP_extract_polyline():

	PolylineXPts_Array = [-2.5e-4, -2.5e-4]
 	PolylineYPts_Array = [0.0, 0.0]
	PolylineZPts_Array = [1.8e-2, 2.6e-2]
	NumPtsInPolyline = 2
	ExtractThroughVolume = True
	ExtractOnlyPointsOnPolyline = False
	IncludeDistanceVariable = False
	NumPtsToExtractAlongPolyline = 20
	ExtractToFile = True
	ExtractFName = 'tec_polyline_extract.dat'
	
	Results = TecUtil.ExtractFromPolyline(
			PolylineXPts_Array,
			PolylineYPts_Array,
			PolylineZPts_Array,
			NumPtsInPolyline,
			ExtractThroughVolume,
			ExtractOnlyPointsOnPolyline,
			IncludeDistanceVariable,
			NumPtsToExtractAlongPolyline,
			ExtractToFile,
			ExtractFName)
	
	TecUtil.DialogMessageBox("Results: %i" % Results, TecVals.MessageBox_Information)

