import os
# to avoid memory leak in Windows
if os.name == 'nt':
	os.environ["OMP_NUM_THREADS"] = '1'
import math
import numpy as np
import matplotlib.pyplot as plt
from vispy.scene import SceneCanvas, visuals, AxisWidget
from qtpy.QtWidgets import QDialog, QMessageBox, QWidget, QHBoxLayout
from qtpy.QtCore import Signal, Slot
from plugin.kMeansClustersDialog_ui import Ui_kMeansClustersDialog
from processing.processing import ProcessingBase
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold


class kMeansClustering(QDialog, ProcessingBase):
	def __init__(self, nwbFile, bento):
		QDialog.__init__(self)
		ProcessingBase.__init__(self, nwbFile, bento)
		self.bento = bento
		self.checkData()
		if not self.neuralExists:
			msgBox = QMessageBox(QMessageBox.Warning, 
			"Required Data not found", 
			"Neural data \
			must exist for this plugin to work")
			msgBox.exec()
			raise RuntimeError("Neural Data does not exist for this plugin to work.")

		self.getNeuralData()
		self.invokeUI()

	def invokeUI(self):
		#setting up UI
		self.ui = Ui_kMeansClustersDialog()
		self.ui.setupUi(self)
	
	def getType(self):
		return "kMeansClustering"
	
	def setNeural(self, neural):
		self.neuralFrame = neural
	
	def preprocessing(self, data):
		scaler = StandardScaler()
		self.scaledData = scaler.fit_transform(data)

	def calculateBIC(self, data, labels):
		nPoints = len(labels)
		nClusters = len(set(labels))
		nDimensions = data.shape[1]

		nParameters = (nClusters - 1) + (nDimensions * nClusters) + 1

		loglikelihood = 0
		for labelName in set(labels):
			dataCluster = data[labels == labelName]
			nPointsCluster = len(dataCluster)
			if nPointsCluster==1:
				loglikelihood += -(nPointsCluster * np.log(nPoints))
			else:
				centroid = np.mean(dataCluster, axis=0)
				variance = np.mean((dataCluster - centroid) ** 2)
				loglikelihood += \
					nPointsCluster * np.log(nPointsCluster) \
					- nPointsCluster * np.log(nPoints) \
					- nPointsCluster * nDimensions / 2 * np.log(2 * math.pi * variance) \
					- (nPointsCluster - 1) / 2

		bic = loglikelihood - (nParameters / 2) * np.log(nPoints)

		return bic

	def computeCrossValidation(self, data):
		# get values from UI
		self.clusterStart = int(self.ui.clusterRangeBox1.text())
		self.clusterStop = int(self.ui.clusterRangeBox2.text())
		self.numFolds = int(self.ui.crossValidationFoldsBox.text())
		self.preprocessing(data)
		kMeansKwargs = {
        "init": "k-means++",
        "n_init": 10,
        "max_iter": 300
    	}
		# cross validation 
		kf = KFold(n_splits=self.numFolds, shuffle=True)
		self.avgBicValues = []
		for k in range(self.clusterStart, self.clusterStop):
			bic_values = []
			for trainInd, valInd in kf.split(self.scaledData):
				scaledDataTrain, scaledDataVal = self.scaledData[trainInd], self.scaledData[valInd]
				kmeans = KMeans(n_clusters=k, **kMeansKwargs)
				kmeans.fit(scaledDataTrain)
				valLabels = kmeans.predict(scaledDataVal)
				# Calculate bic
				bic = self.calculateBIC(scaledDataVal, valLabels)
				bic_values.append(bic)
			self.avgBicValues.append(np.mean(bic_values))
		

	def plotBicValues(self):	
		self.bicCanvas = SceneCanvas(size=(600,600))
		self.bicGrid = self.bicCanvas.central_widget.add_grid()
		self.bicXaxis = AxisWidget(orientation='bottom',
								axis_label='Number of Clusters',
								axis_color='black',
								tick_color='black',
								text_color='black',
								axis_font_size=12,
								font_size= 8,
								axis_label_margin=20,
								tick_label_margin=14)
		self.bicXaxis.height_max = 50
		self.bicXaxis.bgcolor = 'white'
		self.bicGrid.add_widget(self.bicXaxis, row=1, col=1)
	
		self.bicYaxis = AxisWidget(orientation='left',
							 	axis_label='BIC Values',
								axis_color='black',
								tick_color='black',
								text_color='black',
								axis_font_size=12,
								font_size= 8,
								axis_label_margin=70,
								tick_label_margin=8)
		self.bicYaxis.width_max = 100
		self.bicYaxis.bgcolor = 'white'
		self.bicGrid.add_widget(self.bicYaxis, row=0, col=0)
	

		self.bicView = self.bicGrid.add_view(0, 1, bgcolor='white')
		self.bicPlot = visuals.Line(
            np.column_stack((np.arange(self.clusterStart, self.clusterStop), self.avgBicValues)),
            parent=self.bicView.scene,
            color='black'
        )
		self.bicView.camera = "panzoom"
		self.bicView.interactive = False
		self.bicView.camera.set_range(x=(self.clusterStart, self.clusterStop), 
										y=(min(self.avgBicValues), max(self.avgBicValues)))
		self.bicXaxis.link_view(self.bicView)
		self.bicYaxis.link_view(self.bicView)
		
		# show plot on a widget
		self.plotWidget = QWidget()
		self.plotLayout = QHBoxLayout()
		self.plotLayout.addWidget(self.bicCanvas.native)
		self.plotWidget.setWindowTitle("Bayesion Information Criterion Values vs # of Clusters")
		self.plotWidget.setLayout(self.plotLayout)
		self.plotWidget.show()

	
	def kMeansClustering(self, data):
		kMeansKwargs = {
		"init": "k-means++",
		"n_init": 10,
		"max_iter": 300
		}
		self.numOfClusters = int(self.ui.numOfClustersBox.text())
		self.preprocessing(data)
		self.kmeans = KMeans(n_clusters=self.numOfClusters, **kMeansKwargs)
		self.kmeans.fit(self.scaledData)
	
	def getNewOrderAfterClusterting(self):
		newOrder = np.array([], dtype=int)
		endOfLabel = np.array([], dtype=int)
		labels = self.kmeans.labels_
		for c in range(self.numOfClusters):
			indices = np.where(labels==c)[0]
			if c<1:
				endOfLabel = np.concatenate((endOfLabel, [indices.shape[0]]), axis=0, dtype=int)
			else:
				endOfLabel = np.concatenate((endOfLabel, [endOfLabel[-1] + indices.shape[0]]), axis=0, dtype=int)
			newOrder = np.concatenate((newOrder, indices), axis=0, dtype=int)
		self.neuralFrame.neuralScene.reorderTracesAndHeatmap(newOrder, endOfLabel)
			
	@Slot()
	def accept(self):
		if self.ui.gofRadioButton.isChecked():
			self.computeCrossValidation(self.neuralData)
			self.plotBicValues()
		else:
			self.kMeansClustering(self.neuralData)
			self.getNewOrderAfterClusterting()
			
		super().accept()

	@Slot()
	def reject(self):
		super().reject()

def register(registry, nwbFile=None, bento=None):
    kMeansClusteringPlugin = kMeansClustering(nwbFile, bento)
    registry.register(kMeansClusteringPlugin.getType(), kMeansClusteringPlugin)