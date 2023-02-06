#!/usr/bin/env python3
import sys
import os
from dbs.apis.dbsClient import DbsApi
from optparse import OptionParser
from dataclasses import dataclass, field
import os

@dataclass
class DatasetInfo:
    datasetname:list
    verbose:bool
    instance:str = "phys03"
    dataset_fileinfo:dict[str] = field( default_factory=dict)
    def getFileListFromDBS3(self):
        if(self.datasetname[0] == "#"): return []
        if(self.verbose): 
            print('getFileListFromDBS3')
            print(f"DataSetName at DatasetInfo : {self.datasetname}")
        dbs = DbsApi(f'https://cmsweb.cern.ch/dbs/prod/{self.instance}/DBSReader')
        self.dataset_fileinfo[self.datasetname] = dbs.listFiles(dataset = self.datasetname, detail=1)
        return(self.dataset_fileinfo)
    def getFileList(self):
        return(self.dataset_fileinfo)
    def printFiles(self,dataset=None):
        if dataset is None:
            print(self.dataset_fileinfo)
        else :
            if (dataset in self.dataset_fileinfo):
                print(self.dataset_fileinfo[dataset])
            else:
                print(f"Error! {dataset} is not existed.")
    def getFileListWithFormat(self,want_dataset=None):
        if(self.verbose): print('getFileListWithFormat')
        fileinfo_format =[]
        for dataset in self.dataset_fileinfo.keys():
            if ( want_dataset is not None and dataset != want_dataset): continue
            for fileinfo in self.dataset_fileinfo[dataset]:
                fileinfo_format.append({ "logical_file_name": fileinfo["logical_file_name"],
                                         "file_size": fileinfo["file_size"],
                                         "adler32": fileinfo["adler32"] })
        return(fileinfo_format)

if __name__ == "__main__":
    usage=f"Usage: {sys.argv[0]} [options] [dataset1] [dataset2] ..."
    parser = OptionParser(usage)
    parser.add_option("-f", "--datasetfile", dest="dataset", help="Dataset list file. If this option is set, arguments is ignored.")
    parser.add_option("-i", "--instance", dest="instance",default="phys03", help="Instance Name [global or phys03(default)]")
    parser.add_option("-v", "--verbose", dest="verbose",action="store_true", help="Verbose mode")
    (options, args) = parser.parse_args()
    if ( options.dataset is not None):
        datasetname = open(options.dataset).readlines()
    else:
        datasetname = args
    ds = DatasetInfo(datasetname=datasetname, verbose=options.verbose, instance=options.instance)
    ds.getFileListFromDBS3()
    filesinfo = ds.getFileListWithFormat()
    for fileinfo in filesinfo:
        print(f'LFN : {fileinfo["logical_file_name"]} / Size: {fileinfo["file_size"]} / Adler32: {fileinfo["adler32"]}\n')

