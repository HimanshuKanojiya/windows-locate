"""
Created on 12/10/2020
Author: Himanshu Kanojiya
Script Version 1.0
Descripton: To find query match files and folders
"""


import os
import argparse
import json
import shelve
import time
import difflib
import re


class file_loads(object):
    """
    This class is to handle file related operations.
    """
    def __init__(self, configs = None):
        self._configs = configs #private variable
    
    @property
    def configs(self):
        """
        This function is to see script configurations.
        """
        return self._configs
    
    @configs.setter
    def configs(self, path=None):
        """
        This Function is to load json configuration file.
        """
        if path == None:
            with open("config.json") as fp:
                config = json.load(fp)
            self._configs = config
        else:
            with open(os.path.abspath(path)) as fp:
                config = json.load(fp)
            self._configs = config
            
    @staticmethod
    def _local_db_writer(db_name, indextype, db=dict()):
        """
        This Function is to write in local database
        Usage > pass data in dictionary format
        
        Note: 
        1. For files, use 'File Indexes' as key
        2. For folders, use 'Folder Indexes' as key
        3. For values, pass in list format
        """
        
        if len(db) == None:
            return -1 # -1 for empty passing dictionaries
        else:
            try:
                lc_db = shelve.open(db_name)
                for key, data in db.items():
                    #We can not add nested dictionary in shelve
                    #directly, that'why we assign the dict in temp
                    #first then store elements in that var
                    #after that store that var in shelve
                    temp = lc_db[indextype]
                    temp[key] = data
                    lc_db[indextype] = temp

                lc_db.close()
            except:
                raise ValueError("No Configuration Loaded")
                
    @staticmethod
    def _create_db(db_name):
        """
        This function should be called first, before calling 'local_db_writer' function
        Usage > pass db_name, use db_name which is mentioned in config.json file
        """
        if str(db_name + ".dir") not in os.listdir("."):
            lc_db = shelve.open(db_name)
            lc_db["Folder Indexes"] = {}
            lc_db["File Indexes"] = {}
            lc_db.close()
            return 1
        else:
            return
    
    @staticmethod
    def _create_db_json(db_name):
        if str(db_name + ".json") not in os.listdir("."):
            with open(str(db_name+".json"), "a") as jpointer:
                json.dump({"Folder Indexes": {},
                          "File Indexes": {}}, jpointer)
    
    
    @staticmethod
    def _error_logs(error = None):
        if error == None:
            return 
        else:
            time_of_error = time.asctime(time.localtime(time.time()))
            reason_of_error = error
            error_format = f"Time of Error: {time_of_error}, Reason of Error: {reason_of_error}"
            with open("errors_log.txt","a") as pointer:
                pointer.write(error_format)
                pointer.write("\n")
                
    
class indexer(file_loads):
    
    def __init__(self):
        file_op = file_loads()
        file_op.configs = None
        self._drive = file_op.configs["drive_paths"]
        self._disallow_paths = file_op.configs["disallow_paths"]
        self._allowed_paths = file_op.configs["allowed_paths"]
        self._allowed_extension = file_op.configs["allowed_extensions"]
        self._disallow_extension = file_op.configs["disallow_extensions"]
        self._db_name = file_op.configs["db_name"]
        
    def _indexer_recursive_bot(self, path):
        for i in os.listdir(path):
            prep = path
            path_2 = os.path.join(os.path.abspath(prep), i)
            
            #if anything available in disallow path list then it will
            #check each seeing paths with disallow list
            
            if self._isdisallowed_path_available():
                
                #if path_2 found/present in disallow list
                #then indexer bot will ignore them &
                #will not save db   
                if path_2 in [os.path.abspath(i) for i in self._isdisallowed_path_available()]:
                    continue
                
                
                #if path_2 not found then extension check will
                # be consider
                else:
                    try:
                        #this condition is to check path_2 is file or not
                        if os.path.isfile(path_2):
                            #if allowed extension present then index
                            #will check extensions otherwise consider
                            #all files
                            if self._isallowed_extensions_available():
                                #extension check
                                if os.path.splitext(path_2)[-1][1:] in self._isallowed_extensions_available():
                                    file_loads._local_db_writer(self._db_name, "File Indexes",{i: path_2})
                                    
                            
                            elif self._isdisallow_extensions_available():
                                #disallow extension check
                                if os.path.splitext(path_2)[-1][1:] not in self._isdisallow_extensions_available():
                                    file_loads._local_db_writer(self._db_name, "File Indexes",{i: path_2})
                            else:
                                file_loads._local_db_writer(self._db_name, "File Indexes",{i: path_2})
                        
                        #this condition is to check path_2 is folder
                        #it will not check extensions
                        elif os.path.isdir(path_2):
                            file_loads._local_db_writer(self._db_name, "Folder Indexes",{i: path_2})
                            self._indexer_recursive_bot(path_2)

                    except Exception as Error:
                        file_loads._error_logs(Error)
                        continue
            
            #if nothing available in disallow list then it will
            #see and consider all path within available paths
            else:
                try:
                    #this condition is to check path_2 is file or not
                    if os.path.isfile(path_2):
                    #if allowed extension present then index
                    #will check extensions otherwise consider
                    #all files
                        if self._isallowed_extensions_available():
                        #extension check
                            if os.path.splitext(path_2)[-1][1:] in self._isallowed_extensions_available():
                                file_loads._local_db_writer(self._db_name, "File Indexes",{i: path_2})
                            
                        elif self._isdisallow_extensions_available():
                        #disallow extension check
                            if os.path.splitext(path_2)[-1][1:] not in self._isdisallow_extensions_available():
                                file_loads._local_db_writer(self._db_name, "File Indexes",{i: path_2})
                        
                        else:
                            file_loads._local_db_writer(self._db_name, "File Indexes",{i: path_2})
                        
                        #this condition is to check path_2 is folder
                        #it will not check extensions
                    elif os.path.isdir(path_2):
                        file_loads._local_db_writer(self._db_name, "Folder Indexes",{i: path_2})
                        self._indexer_recursive_bot(path_2)
                
                except Exception as Error:
                    file_loads._error_logs(Error)
                    continue
                
    def indexer_recursive_decision_primary(self):
        #This method is check and validate the drive path
        #and allowed_paths, if drive_path available then it will ignore
        #allowed paths otherwise consider them to use
        
        if self._isdrive_path_available():
            if self._isallowed_path_available():
                for drive in self._isdrive_path_available():
                    for paths in self._isallowed_path_available():
                        if drive in paths:
                            self._indexer_recursive_bot(paths)
            else:
                for drive in self._isdrive_path_available():
                    self._indexer_recursive_bot(drive)
            
        elif self._isdrive_path_available() == False or self._isallowed_path_available():
            for path in self._isallowed_path_available():
                self._indexer_recursive_bot(path)
                
    def _isallowed_path_available(self):
        #return false if not available, othwerwise return allowed
        return False if(len(self._allowed_paths) == 0) else self._allowed_paths
    
    def _isdisallowed_path_available(self):
        #return false if not available, otherwise return disallowed paths
        return False if(len(self._disallow_paths) == 0) else self._disallow_paths
    
    def _isdrive_path_available(self):
        #return False if not available otherwise return path
        #If this is not available then indexer will look for
        #allowed path, if both not available then indexer will
        #not work
        return False if(len(self._drive) == 0) else self._drive
    
    def _isallowed_extensions_available(self):
        #return False if not available otherwise return extensions
        #if you specify this in configuration file then
        #indexer will only look for allowed extensions but folders
        #will be indexed by default
        return False if(len(self._allowed_extension) == 0) else self._allowed_extension
    
    def _isdisallow_extensions_available(self):
        #return False if not available otherwise return disallowed extensions
        #if you specify this then indexer will only ignore specified extensions
        #and indexer all
        return False if(len(self._disallow_extension) == 0) else self._disallow_extension
    
    def start_db(self):
        file_loads._create_db(self._db_name)
        
        
class indexSearch:
    def __init__(self, db_name):
        self._db_name = db_name
        self._isDbOpen = False
        self._db_pointer = None
        
    def _db_open(self):
        if self._isDbOpen == True:
            raise ValueError("Database is already opened")
            
        else:
            self._db_pointer = shelve.open(self._db_name)
            self._isDbOpen = True
            
    def _db_close(self):
        if self._isDbOpen == False:
            #if no db open then it will return -1
            return -1
        else:
            self._db_pointer.close()
            self._isDbOpen = False
            self._db_pointer = None
            
    def _db_key_close_matches_files(self, query, cutoff):
        if self._isDbOpen == False:
            #if no db open then return -1
            return -1
        else:
            #if zero searches found then it will return empty list
            keys = difflib.get_close_matches(query,self._db_pointer["File Indexes"].keys(),100, cutoff)
            print(keys)
            return [] if(len(keys) == 0) else keys
        
    def _db_key_close_matches_folders(self, query, cutoff):
        if self._isDbOpen == False:
            return -1
        else:
            keys = difflib.get_close_matches(query, self._db_pointer["Folder Indexes"].keys(),100,cutoff)
            print(keys)
            return [] if(len(keys) == 0) else keys
    
    def _iterFoundResults(self, files, folders):
        #input should be list or -1 for no results
        if files == -1 and folders == -1:
            return "NO MATCH FOUND"
        
        if files != -1:
            for show in files:
                print(self._db_pointer["File Indexes"][show])
        
        if folders != -1:
            for show in folders:
                print(self._db_pointer["Folder Indexes"][show])
                
    def _querySender(self, query):
        #producing wrong results, need to improve this
        if self._isDbOpen == False:
            self._db_open()
        
        isFile = False
        cutoff = 0.5
        while not isFile:
            files = []
            
            if cutoff <= 0.1:
                isFile = True
                break
                
            if len(files) == 0:
                files = self._db_key_close_matches_files(query, cutoff)
                
            if len(files) > 0:
                isFile = True  
                break
            
            cutoff-=0.1
            
        isFolder = False
        cutoff = 0.5
        
        while not isFolder:
            folder = []
            if cutoff <= 0.1:
                isFolder = True
                break
            if len(folder) == 0:
                folder = self._db_key_close_matches_folders(query, cutoff)
            
            if len(folder) > 0:
                isFolder = True
                break
            cutoff-=0.1
        
        self._iterFoundResults(self._queryMatcherAfterGetCloseMatch(query,files), self._queryMatcherAfterGetCloseMatch(query, folder))
        self._db_close()
        
    def _queryMatcherAfterGetCloseMatch(self, query, db):
        #supporting method for _querySender
        if len(db) == 0:
            return -1
        else:
            new_db = []
            for i in db:
                if re.findall(query, i, re.IGNORECASE):
                    new_db.append(i)
            return new_db
        
    def querySenderWithRe(self, query):
        #This method will use re.findall function to find pattern
        if self._isDbOpen == False:
            self._db_open()
        
        files = []      
        for i in self._db_pointer["File Indexes"].keys():
            if re.findall(query, i, re.IGNORECASE):
                files.append(i)
                
        folders = []
        for i in self._db_pointer["Folder Indexes"].keys():
            if re.findall(query, i, re.IGNORECASE):
                folders.append(i)
                
        files = -1 if(len(files) == 0) else files
        folders = -1 if(len(folders) == 0) else folders
        self._iterFoundResults(files, folders)
        self._db_close()


if __name__ == "__main__":

    if "config.json" in os.listdir("."):

        parser = argparse.ArgumentParser(description = "Give Query to find related files/folders")
        parser.add_argument("-search", help = "Query to Search")
        parser.add_argument("-createdb", help="Enter 'y' Create Database, Make sure you have checked the config.json file")
        args = vars(parser.parse_args())

        if args["search"] != None or args["createdb"] != None:
            core = indexer()
            search = indexSearch(core._db_name)
            print("[+] Windows Locate Configuration Found")

        if args["search"]!= None and "local-db.dir" in os.listdir("."):
            print("[+] Searching in Database")
            search.querySenderWithRe(args["search"])

        elif args["createdb"] == "y":
            print("[+] Creating the database")
            core.start_db()
            core.indexer_recursive_decision_primary()
            print("[+] Database created")
            
        elif "local-db.dir" not in os.listdir("."):
            print("[+] Database is not created yet")
    else:
        print("[+] Windows Locate Configuration Not Found!")

