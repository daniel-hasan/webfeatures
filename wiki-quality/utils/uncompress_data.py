'''
Created on 28 de nov de 2017
Baseado em: https://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type-and-uncompress
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
'''

import bz2
import gzip
import os
import zipfile


class CompressedFile(object):
    magic = None
    file_type = None
    mime_type = None
    proper_extension = None
    extension_ready = False
    
    @classmethod
    def get_known_compress_classes(self):
        arrStrNames = [SubClassCompressedFile for SubClassCompressedFile in CompressedFile.__subclasses__() if SubClassCompressedFile.extension_ready]
        return arrStrNames
    @classmethod
    def get_known_compress_extensions(self):
        arrStrNames = [SubClassCompressedFile.file_type for SubClassCompressedFile in CompressedFile.get_known_compress_classes()]
        return arrStrNames
    
    def __init__(self, file_pointer):
        # f is an open file or file like object
        self.file_pointer = file_pointer

    @classmethod
    def is_magic(self, data):
        return data.startswith(self.magic.encode())
    
    @classmethod
    def get_compressed_file(self,file_pointer):
        start_of_file = file_pointer.read(1024)
        file_pointer.seek(0)
        for cls in CompressedFile.get_known_compress_classes():
            if cls.is_magic(start_of_file):
                return cls(file_pointer)
        
        raise UncompatibleTypeError(file_pointer)
    
    def descomprime_files(self,strDirPrefix):
        for name,strFileTxt in self.read_each_file():
            #cria o diretorio dentro do tmp
            arrPastasEArq = name.split("/")
            strDir = strDirPrefix+"/".join(arrPastasEArq[:len(arrPastasEArq)-1])
            os.makedirs(strDir)
            #grava o arquivo
            with open(strDir+arrPastasEArq[len(arrPastasEArq)-1]) as file:
                file.write(strFileTxt)
                
    def open(self):
        return None

class UncompressError(Exception):
    """Basic exception for errors raised by comprression"""
    def __init__(self, file, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "Erro ao compactar/descompactar o arquivo %s" % file.name
        super(UncompressError, self).__init__(msg)
        self.file = file

class UncompatibleTypeError(Exception):
    """Basic exception for errors raised by comprression"""
    def __init__(self, file, msg=None):
        if msg is None:
            # Set some default useful error message
            arrCompFormats = CompressedFile.get_known_compress_extensions()
            msg = "O arquivo '%s' não é um tipo de arquivo válido. É possível descompactar o(s) seguinte(s) formato(s): %s " %(file.name,", ".join(arrCompFormats))
        super(UncompatibleTypeError, self).__init__(msg)
        self.file = file
class ZIPFile (CompressedFile):
    magic = '\x50\x4b\x03\x04'
    file_type = 'zip'
    mime_type = 'compressed/zip'
    extension_ready = True
    
    def __init__(self,file_pointer):
        super().__init__(file_pointer)
        self.zip_file_obj = zipfile.ZipFile(self.file_pointer) 
        
    def read_each_file(self):
        for name in self.zip_file_obj.namelist():
            yield (name,self.zip_file_obj.read(name))
            
    def get_each_file_size(self):
        return [(name,self.zip_file_obj.getinfo(name).file_size) for name in self.zip_file_obj.namelist()]
        
class BZ2File (CompressedFile):
    magic = '\x42\x5a\x68'
    file_type = 'bz2'
    mime_type = 'compressed/bz2'

    def __init__(self,file_pointer):
        super().__init__(file_pointer)
        self.bz_file_obj = zipfile.ZipFile(self.file_pointer) 


class GZFile (CompressedFile):
    magic = '\x1f\x8b\x08'
    file_type = 'gz'
    mime_type = 'compressed/gz'

    def __init__(self,file_pointer):
        super().__init__(file_pointer)
        self.bz_file_obj = zipfile.ZipFile(self.file_pointer)



if __name__ == '__main__':
    #filename = "/home/profhasan/test_compress.zip"
    filename = "/home/profhasan/doc_station.pdf"
    with open(filename,"rb") as f:
        objFileZip = CompressedFile.get_compressed_file(f)
        
        #navega buscando o tamanho de cada arquivo
        for name,size in objFileZip.get_each_file_size():
            print("Name: "+name+" size: "+str(size))
            
        for name,strFileTxt in objFileZip.read_each_file():
            print("")
            print("-------------------------------------")
            print("Conteudo do arquivo '%s': "+name)
            print(strFileTxt)
            print("-------------------------------------")
            
        