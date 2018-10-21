# -*- encoding: utf-8 -*-
import os
from .util import check_dir, zip_shp

import pandas as pd
import geopandas as gpd

from mstdbscan import MSTdbscan
from . import mstResult



class MSTDBSCAN(MSTdbscan):
    def __init__(self, pysdaData):
        self.dateIndex = pysdaData.dateIndex
        super().__init__(pysdaData.gdf)


    def _MSTdbscan__storeResult(self, MSTDBSCAN_Result):
        self._MSTdbscan__result = mstResult.MSTresult(self._MSTdbscan__timeBar, self.dateIndex,\
        self._MSTdbscan__pointGDF, self._MSTdbscan__points,\
        MSTDBSCAN_Result["allClusters"], MSTDBSCAN_Result["noiseOverTime"])



    ###########################################################################
