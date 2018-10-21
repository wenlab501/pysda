import os
import numpy as np
import imageio
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches

from .util import check_dir, zip_shp
from mstdbscan import MSTdbscanResult

class MSTresult(MSTdbscanResult):
    def __init__(self, timeBar, dateIndex, pointGDF, points, allClusters, noiseOverTime):

        super().__init__(timeBar, pointGDF, points, allClusters, noiseOverTime)

        self.__dateIndex = dateIndex
        self.__timeBar = timeBar
        self.__clusterGDF = self._MSTdbscanResult__clusterGDF
        self.__pointResultGDF = self._MSTdbscanResult__pointResultGDF

        self.__clusterGDF["mstDate"] = self.__clusterGDF["mstTime"].apply(lambda x: self.__dateIndex[str(x)])
        self.__pointResultGDF["mstDate"] = self.__pointResultGDF["mstTime"].apply(lambda x: self.__dateIndex[str(x)])


    def setPolygons(self, polygonGDF):
        super().setPolygons(polygonGDF)
        self.__polygonResultGDF = self._MSTdbscanResult__polygonResultGDF
        self.__polygonResultGDF.rename(columns=self.__dateIndex, inplace=True)


    def getAll(self):
        if self.__polygonResultGDF is None:
            raise AttributeError("Please set the polygons first.")

        resultDict = {}
        resultDict["clusters"] = self.__clusterGDF
        resultDict["points"] = self.__pointResultGDF
        resultDict["polygons"] = self.__polygonResultGDF
        return resultDict

    def saveAll(self, dirpath=".", prefix="mst_"):
        if self.__polygonResultGDF is None:
            raise AttributeError("Please set the polygons first.")

        clusterFilename = prefix+"dynamicClusters.shp"
        clusterPath = os.path.join(dirpath, clusterFilename)
        check_dir(clusterPath)
        #clusterGDF = self.__getClusters()
        self.__clusterGDF.to_file(clusterPath, encoding="utf-8")

        pointFilename = prefix+"dynamicPoints.shp"
        pointPath = os.path.join(dirpath, pointFilename)
        check_dir(pointPath)
        #pointResultGDF = self.__getPoints()
        self.__pointResultGDF.to_file(pointPath, encoding='utf-8')

        polygonFilename = prefix+"polygonResults.shp"
        polygonPath = os.path.join(dirpath, polygonFilename)
        check_dir(polygonPath)
        #polygonResultGDF = self.__getPolygons()
        self.__polygonResultGDF.to_file(polygonPath, encoding='utf-8')


    def saveAnimation(self, figsize=(8,8), dirpath=".", prefix="mst_"):
        if self.__polygonResultGDF is None:
            raise AttributeError("Please set the polygons first.")

        gifFilename = prefix+"polygon.gif"
        gifPath = os.path.join(dirpath, gifFilename)
        check_dir(gifPath)
        #polygonResultGDF = self.__getPolygons()


        timeList = list(self.__dateIndex.values())
        timeList.sort()

        kwargs_write = {'fps':1.0, 'quantizer':'nq'}
        imageio.mimsave(gifPath, [self.__plotOneImage(self.__polygonResultGDF, t, figsize) for t in timeList], fps=1)


    def __plotOneImage(self, polygonResultGDF, time, figsize):
        # Data for plotting
        groupedGDF = polygonResultGDF.groupby(time)

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_aspect("equal")
        ax.set_title(time)
        ax.set_xticks([])
        ax.set_yticks([])

        increase_patch = mpatches.Patch(color="red", label='Increase')
        keep_patch = mpatches.Patch(color="blue", label='Keep')
        decrease_patch = mpatches.Patch(color="green", label='Decrease')
        non_patch = mpatches.Patch(color="gray", label='No cluster')

        ax.legend(handles=[increase_patch, keep_patch, decrease_patch, non_patch])

        #polygonGDF.plot(ax=ax, column=time, categorical=True)
        for name, group in groupedGDF:
            if name == "increase":
                group.plot(ax=ax, color="red")
            elif name == "keep":
                group.plot(ax=ax, color="blue")
            elif name == "decrease":
                group.plot(ax=ax, color="green")
            else:
                group.plot(ax=ax, color="gray")

        # Used to return the plot as an image rray
        #fig.canvas.draw()       # draw the canvas, cache the renderer
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        return image
