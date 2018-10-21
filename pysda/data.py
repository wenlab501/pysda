# -*- encoding: utf-8 -*-
import datetime
from dateutil.parser import parse

import shapely.geometry as sg
import pandas as pd
import geopandas as gpd

#from pysda import tapitas


def __checkColName(pointDF, t, x=None, y=None):
    check = True
    col_key = [x, y, t]
    for k in col_key:
        if k is None:
            continue
        else:
            if k in pointDF.columns:
                pass
            else:
                raise AttributeError('The given column names are not in the data.')

def readCSV(csvpath, xtitle="xcoor", ytitle="ycoor", ttitle="time", crs=None, tunit="day"):
    pointDF = pd.read_csv(csvpath)
    return readDF(pointDF, xtitle, ytitle, ttitle, crs, tunit)


def readDF(pointDF, xtitle="xcoor", ytitle="ycoor", ttitle="time", crs=None, tunit="day"):
    __checkColName(pointDF, ttitle, xtitle, ytitle)

    # create geometry
    geometry = []
    for index, row in pointDF.iterrows():
        coord = sg.Point(float(row[xtitle]), float(row[ytitle]))
        geometry.append(coord)

    pointGDF = gpd.GeoDataFrame(pointDF, geometry=geometry)
    pointGDF.crs = crs

    d = PysdaData(pointGDF, ttitle, tunit)
    return d


def readSHP(shppath, ttitle="time", tunit="day"):
    pointGDF = gpd.read_file(shppath)
    return readGDF(pointGDF, ttitle, tunit)


def readGDF(pointGDF, ttitle="time", tunit="day"):
    __checkColName(pointGDF, ttitle)

    d = PysdaData(pointGDF, ttitle, tunit)
    return d



###############################################################################
class PysdaData():
    def __init__(self, gdf, ttitle, tunit):
        self.tunit = self.__transformTimeUnit(tunit)
        if self.tunit == "int":
            gdf["intTime"] = gdf[ttitle]

            intDates = gdf[ttitle].tolist()
            intDates = list(set(intDates))
            intDates.sort()

            timeDict = {}
            for i in intDates:
                timeDict[i] = i

        else:
            # deal with time unit
            strDates = gdf[ttitle]
            dates = [parse(i) for i in strDates]
            intDates = [None]*len(dates)

            start = min(dates)
            end = max(dates)
            dateRange = [i.to_pydatetime() for i in pd.date_range(start, end, freq=self.tunit)]

            for i in range(len(dates)):
                for j in range(len(dateRange)-1,-1,-1):
                    if dates[i] >= dateRange[j]:
                        intDates[i] = j
                        break

            gdf["intTime"] = intDates

            timeDict = {}
            for i in range(len(dateRange)):
                timeDict[str(i)] = dateRange[i].strftime("%Y/%m/%d-%H:%M:%S")

        self.gdf = gdf
        self.dateIndex = timeDict

    def __transformTimeUnit(self, tunit):
        if tunit == "int":
            pass
        elif tunit == "hour":
            tunit = "1h"
        elif tunit == "day":
            tunit = "1D"
        elif tunit == "week":
            tunit = "7D"
        elif tunit == "month":
            tunit = "30D"
        elif tunit == "year":
            tunit = "365D"
        else:
            pass

        return tunit
