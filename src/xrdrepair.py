#!/usr/bin/env python3
from XRootD import client
from XRootD.client.flags import DirListFlags, OpenFlags, MkDirFlags, QueryCode
from optparse import OptionParser
from configparser import ConfigParser
from datasetinfo import DatasetInfo 

#from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass, field

import logging

import os, sys
import gettext
t = gettext.translation('messages','locale',fallback=True)
_ = t.gettext

class MyCopyProgressHandler(client.utils.CopyProgressHandler):
  def begin(self, jobId, total, source, target):
    print (f"id: {jobId}, total: {total}")
    print (f"source: {source}")
    print (f"target: {target}")

  def end(self, jobId, result):
    print (f"end status: {jobId}, {result}")

  def update(self, jobId, processed, total):
    print (f"jobId: {jobId}, processed: {processed}, total: {total}\n")

  def should_cancel( jobId ):
    return False

#@dataclass(frozen=True)
@dataclass
class XrdRepair:
    dataset: str 
    step: int
    configFile: str 
    dryrun: bool
    autorecover: bool
    output: str
    local: bool
    verbose: bool


    def __post_init__(self):
        # Parse Option and Config                                                                                                                             
        self.config = ConfigParser()
        self.config.read(self.configFile)
        if ( "LocalPrefix" in self.config['SiteInfo']) :
            self.local_path = self.config['SiteInfo']['LocalPrefix']
        else: 
            self.local_path = os.getcwd()
        self.XrdHost   = self.config['SiteInfo']['XrdHost']
        self.XrdPrefix = self.config['SiteInfo']['XrdPrefix']
        self.downloader = client.CopyProcess()
    def printParams(self):
        print(type(self.config),self.config['SiteInfo']['LocalPrefix'])
    def getFilelist(self):
        logging.info("getFileList")
        self.filelist =[]
        datasets = open(self.dataset).readlines()
        for dataset in datasets:
            dataset = dataset.strip()
            datasettype = dataset.split("/")[-1]
            if(datasettype == "USER"):
                instance = "phys03"
            else:
                instance = "global"
            ds = DatasetInfo(datasetname=dataset, verbose=self.verbose, instance="global")
            ds.getFileListFromDBS3()
            self.filelist.extend(ds.getFileListWithFormat())
    def checkingfile(self):
        logging.info(self.XrdHost, self.XrdPrefix)
        self.total_files = len(self.filelist)
        count = {'normal file':0,'duplicated file':0,'missing file':0,'broken file':0}
        check_filelist = {'duplicated file':{}, 'missing file':{}, 'broken file':{} }
        for idx,fileinfo in enumerate(self.filelist):
            filename = fileinfo['logical_file_name']
            size = fileinfo['file_size']
            checksum = fileinfo['adler32']
            if (idx % int(self.step)==0) : 
                print(f"{idx+1}/{self.total_files} : {filename}")
            myclient = client.FileSystem(f"{self.XrdHost}")
            xrd_filepath = f"{self.XrdPrefix}{filename}"
            logging.info(f"xrd_filepath : {xrd_filepath}")
            ## missing 여부 판단,
            status, stat = myclient.stat(xrd_filepath)
            if (status.ok):
                status, deeplocate = myclient.deeplocate(xrd_filepath,OpenFlags.READ)
                if ( len(deeplocate.locations) ==1 ):
                    if int(stat.size)==int(size):
                        count['normal file'] = count['normal file']+1
                    else:
                        count['broken file'] = count['broken file'] + 1
                        if self.autorecover:
                            self.addDownloadFile(filename)
                        else:
                            check_filelist['broken file'][filename]=("Failed",stat.size)
                elif (len(deeplocate.locations)>=2):
                    count['duplicated file'] = count['duplicated file'] + 1
                    check_filelist['duplicated file'][filename] = []
                    for location in deeplocate.locations:
                        myclient2 = client.FileSystem(f"{location.address}")
                        status, stat_in_server = myclient2.stat(xrd_filepath)
                        logging.info(stat_in_server)
                        if int(stat_in_server.size)==int(size):
                            check_filelist['duplicated file'][filename].append((location.address,"OK",stat.size))
                        else:
                            if self.autorecover:
                                ## Try to remove duplicated file
                                remove_status = self.removeXrdFile(xrd_filepath)
                                if (remove_status): 
                                    check_filelist['duplicated file'][filename].append((location.address,"Removed",stat.size))
                                else:
                                    check_filelist['duplicated file'][filename].append((location.address,"Failed to remove",stat.size))
                            else:
                                check_filelist['duplicated file'][filename].append((location.address,"Failed",stat.size))
                else: 
                    print(_("Unknown error!"))
                    print(f"{deeplocate}")
                    print(f"{status}")
            else:
                logging.info(_("The file is missing"))
                count['missing file'] = count['missing file'] + 1
                if self.autorecover:
                    logging.info(_("The file is transferring."))
                    self.addDownloadFile(filename)
        self.count = count
        self.checklist = check_filelist
    def removeXrdFile(self, filename):
        status, stat = myclient2.rm(f"{filename}")
        return status.ok

    def addDownloadFile(self, filename):
        xrd_filepath = f"{self.XrdPrefix}{filename}"
        cmsaaa = self.config['SiteInfo']['CMSAAA']
        src  = f"{cmsaaa}/{filename}"
        if self.local:
           if ( self.config['SiteInfo']['LocalPrefix'] is not None) :
               local_path = self.config['SiteInfo']['LocalPrefix']
               dest = f"{local_path}/{xrd_filepath}"
           else: 
               print("No configure for local prefix")
               return -1
        else: 
           dest = f"{self.XrdHost}/{xrd_filepath}"
        logging.info(f"Register transferring from {src} to {dest}.")
        self.downloader.add_job(src,dest,sourcelimit=4,force=True)

    def fileDownload(self):
        if ( self.dryrun): return 0
        self.downloader.prepare()
        handler = MyCopyProgressHandler()
        status, response = self.downloader.run(handler=handler)
        if ( response[0]["status"].ok ):
            print(response)
            return 0
        else:
            print(status, response)
            return -1

    def report(self):
        if self.verbose:
            print(self.count)
            print(self.checklist)

        with open(self.output,'w') as mdfile:
            mdfile.write(_("# File Scan Report on the XRootD System\n"))
            mdfile.write(_("## Scan configuration\n"))
            mdfile.write(_(f"* Repair mode : {self.autorecover}\n"))
            mdfile.write(f"## Total Number of files: {self.total_files}\n")
            mdfile.write(f"* Number of Normal files: {self.count['normal file']}\n")
            mdfile.write(f"* Number of Duplicated files: {self.count['duplicated file']}\n")
            for duplicated_file in self.checklist['duplicated file'].keys():
                mdfile.write(f"   * {duplicated_file}\n")
                for (address, status, size) in self.checklist['duplicated file'][duplicated_file]:
                    mdfile.write(f"      * ```{address}```\n")
                    mdfile.write(f"         * Status is {status}\n")
                    mdfile.write(f"         * Size is {size}\n")
            mdfile.write(f"* Number of Missing files: {self.count['missing file']}\n")
            for missing_file in self.checklist['missing file'].keys():
                mdfile.write(f"   * {missing_file}\n")
                (status) = self.checklist['missing file'][missing_file]
                mdfile.write(f"         * Status is {status}\n")
            mdfile.write(f"* Number of broken files: {self.count['broken file']}\n")
            for broken_file in self.checklist['broken file'].keys():
                mdfile.write(f"   * {broken_file}\n")
                (status, size) = self.checklist['broken file'][broken_file]
                mdfile.write(f"         * Status is {status}\n")
                mdfile.write(f"         * Size is {size}\n")


if __name__ == "__main__":
    usage=f"Usage: {sys.argv[0]} [options] \n(ex) {sys.argv[0]} -i datasetlist.txt -v "
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--input", dest='dataset',default="datasetlist.txt",help=_('Input dataset list file to check'))  
    parser.add_option("-s", "--step", dest='step',default=1,help=_('Number of step to display'))
    parser.add_option("-c", "--config", dest='configFile',default="config.ini",help=_('Config file')) 
    parser.add_option("-d", "--dryrun", dest='dryrun',action='store_true',help=_('Dry run mode')) 
    parser.add_option("-a", "--autorecover", dest='auto',action="store_true",default=False,help=_('Auto recovery using DBS')) 
    parser.add_option("-o", "--output", dest='output',default="output.md",help=_('Set a filename for report output')) 
    parser.add_option("-l", "--local", dest='local',action='store_true',help=_('Download file to local directory (For production site)')) 
    parser.add_option("-v", "--verbose", dest='verbose',action='store_true',help=_('Verbose mode'))                                                       
    (options, args) = parser.parse_args()
    if options.verbose:
        logging.basicConfig(level=logging.INFO)
    xr = XrdRepair( 
                    dataset = options.dataset,
                    step = options.step,
                    configFile = options.configFile,
                    dryrun = options.dryrun,
                    autorecover = options.auto,
                    output = options.output,
                    local = options.local,
                    verbose = options.verbose,
                    )
    #xr.printParams()
    xr.getFilelist()
    xr.checkingfile()
    xr.fileDownload()
    xr.report()

