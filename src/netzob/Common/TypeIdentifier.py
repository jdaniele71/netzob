#!/usr/bin/python
# coding: utf8


#+---------------------------------------------- 
#| Global Imports
#+----------------------------------------------
import base64
import logging

#+---------------------------------------------- 
#| Local Imports
#+----------------------------------------------
from ..Common import ConfigurationParser


#+---------------------------------------------- 
#| Configuration of the logger
#+----------------------------------------------
loggingFilePath = ConfigurationParser.ConfigurationParser().get("logging", "path")
logging.config.fileConfig(loggingFilePath)

class TypeIdentifier():
    

    def __init__(self):
        # create logger with the given configuration
        self.log = logging.getLogger('netzob.Common.TypeIdentifier.py')
    
    
    #+---------------------------------------------- 
    #| Identify a possible type from a hexa string
    #+----------------------------------------------
    def getType(self, stringsTable):
        entireString = "".join(stringsTable)
        
        self.log.debug("Identify type of strings "+entireString)
        
        setSpace = set()
        for i in range(0, len(entireString), 2):
            setSpace.add(int(entireString[i:i + 2], 16))
        sorted(setSpace)

        aggregatedValues = ""
        for i in setSpace:
            aggregatedValues += chr(i)

        typesList = ""
        if aggregatedValues == "":
            return typesList
        if aggregatedValues.isdigit():
            typesList += "num,"
        if aggregatedValues.isalpha():
            typesList += "alpha,"
        if aggregatedValues.isalnum():
            typesList += "alphanum,"
        if self.isAscii(aggregatedValues):
            typesList += "ascii,"
        if self.isBase64(stringsTable):
            typesList += "base64,"
        typesList += "binary"
        
        self.log.debug("identified type is "+typesList)
        return typesList
    
    
    
    
    #+---------------------------------------------- 
    #| Return True if the string parameter is ASCII
    #+----------------------------------------------
    def isAscii(self, string):
        try:
            string.decode('ascii')
            return True
        except UnicodeDecodeError:
            return False    
    #+---------------------------------------------- 
    #| Return True if the string parameter is base64
    #|  encoded
    #+----------------------------------------------
    def isBase64(self, stringsTable):
        res = True
        try:
            for s in stringsTable:
                tmp = base64.b64decode(s)
                if tmp == "":
                    res = False
        except TypeError:
            res = False

        return res    
       
         