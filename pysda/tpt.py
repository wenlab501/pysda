# -*- encoding: utf-8 -*-
import os

#import tapitas
from tapitas.subclusters_progress import Point_Diffusion
from . import tpt_make_fig as tmf ## NEW 1016 ##
from .util import check_dir, zip_shp


class Tapitas(object):
    def __init__(self, pysdaData):
        self.dateIndex = pysdaData.dateIndex
        self.point_df = pysdaData.gdf
        # default parameters
        self.params = dict(
                    T1=12,
                    T2=27,
                    SR=500,
                    resample=99,
                    confidence=0.80,
                    critical=None
        )
        self.col_setting = {'time':'intTime'}
        self.PG = None
        self.res_obj = None
        self.results = None


    def setParams(self, T1=None, T2=None, SR=None, resample=None,
            confidence=None, critical=None):

        sparam_key = ['T1', 'T2', 'SR', 'resample', 'confidence', 'critical']
        nparam = [T1, T2, SR, resample, confidence, critical]

        for s,n in zip(sparam_key, nparam):
            if not(n is None):
                self.params[s] = n

    def run(self):
        if not((self.point_df is None) and (self.col_setting is None)):
            T1 = self.params['T1']
            T2 = self.params['T2']
            s_radius = self.params['SR']
            resample_time = self.params['resample']
            confidence_level = self.params['confidence']
            critical_value = self.params['critical']
            self.PG = Point_Diffusion(self.point_df,
                pts_setting=self.col_setting,
                s_radius=s_radius, T1=T1, T2=T2,
                resample_time=resample_time,
                confidence_level=confidence_level,
                critical_value=critical_value
            )
            print("calculation done")
            print("prepare results table")
            self.res_obj = self.PG.results

            summary = self.res_obj.get_summary_df()
            summary = summary.rename(index=dict(clusterno='sub-cluster'))
            results = dict(
                summary =  summary,
                nodes = self.res_obj.get_node_df(),
                slinks = self.res_obj.get_final_slinks_df(),
                npairs = self.res_obj.get_final_nlinks_df(),
                subclusters = self.res_obj.get_cluster_df(),
                prog_links = self.res_obj.get_progress_df(),
            )
            resultsGDF = dict(
                nodes = self.res_obj.get_node_gdf(),
                slinks = self.res_obj.get_final_slinks_gdf(),
                npairs = self.res_obj.get_final_nlinks_gdf(),
                subclusters = self.res_obj.get_cluster_gdf(),
                prog_links = self.res_obj.get_progress_gdf(),
            )
            self.results = {}
            for tab in results.keys():
                if not(tab=='summary'):
                    self.results[tab] = self.__convert_time(tab, results[tab])
                else:
                    self.results[tab] = summary
            self.resultsGDF = {}
            for tab in resultsGDF.keys():
                self.resultsGDF[tab] = self.__convert_time(tab, resultsGDF[tab])

            print("prepare result done")
            self.summary = summary

    def getDF(self, tab):
        if tab in self.resultsGDF:
            return self.results[tab]
        else:
            print('no table name {}'.format(tab))

    def getGDF(self, tab, vno=16, dev_scale=1.5):
        if tab in self.resultsGDF:
            return self.resultsGDF[tab]
        else:
            print('no table name {}'.format(tab))

    def getAll(self, mode='gdf'):
        if mode=='gdf':
            return self.resultsGDF
        elif mode=='df':
            return self.results

    def saveAll(self, dirpath='.', prefix='tpt_', to_csv=False, to_shp=True, zip_it=False):
        if to_csv:
            self.output_csv(dirpath=dirpath, prefix=prefix)
        if to_shp:
            self.output_shp(dirpath=dirpath, prefix=prefix, zip_it=zip_it)

    def output_csv(self, dirpath='.', prefix='tpt_'):
        tables=['summary', 'nodes', 'slinks', 'npairs', 'subclusters', 'prog_links']
        for tab in tables:
            fn = prefix+tab+'.csv'
            fp = os.path.join(dirpath, fn)
            check_dir(fp)
            #print(results[tab].head())
            #table = self.__convert_time(tab, self.results[tab])
            table = self.results[tab]
            table.to_csv(fp, index_label='ind')

    def output_shp(self, dirpath='.', prefix='tpt_', vno=16, dev_scale=1.5, zip_it=False):
        tables=['nodes', 'slinks', 'npairs', 'subclusters', 'prog_links']
        for tab in tables:
            fn = prefix+tab+'.shp'
            fp = os.path.join(dirpath, fn)
            check_dir(fp)
            #print(resultsGDF[tab].head())
            #table = self.__convert_time(tab, self.resultsGDF[tab])
            table = self.resultsGDF[tab]
            table.to_file(filename=fp, driver='ESRI Shapefile')
            if zip_it:
                fn = prefix+tab+'.zip'
                fp = os.path.join(dirpath, fn)
                zip_shp(fp)

    ## NEW 1016 ##
    def saveFigure(self, dirpath='.', prefix='tpt_', bg_polys=[], bbox=None, vno=16, dev_scale=1.5):
        return tmf.saveFigure(self.resultsGDF, dirpath=dirpath, prefix=prefix, bg_polys=bg_polys, bbox=bbox, vno=vno, dev_scale=dev_scale)


    def __convert_time(self, tab, gdf):
        time_col = {
            'summary': [],
            'nodes': ['time'],
            'slinks': ['otime', 'dtime'],
            'npairs': ['n1t','n2t'],
            'subclusters': ['time_median','time_start','time_stop','time_mdian'],
            'prog_links': ['t0','t1'],
        }
        for co in time_col[tab]:
            if co in gdf.columns:
                intdate = gdf[co].tolist()
                fulldate = [ self.dateIndex[str(int(i))] for i in intdate ]
                gdf[co] = fulldate
        return gdf
