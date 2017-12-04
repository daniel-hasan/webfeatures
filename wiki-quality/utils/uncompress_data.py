import bz2
import gzip
import zipfile
'''
Created on 28 de nov de 2017
Baseado em: https://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type-and-uncompress
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
'''
class CompressedFile(object):
    magic = None
    file_type = None
    mime_type = None
    proper_extension = None

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
        for cls in (ZIPFile, BZ2File, GZFile):
            if cls.is_magic(start_of_file):
                return cls(file_pointer)
    
        return None

    def open(self):
        return None




class ZIPFile (CompressedFile):
    magic = '\x50\x4b\x03\x04'
    file_type = 'zip'
    mime_type = 'compressed/zip'
    
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
    filename = "/home/hasan/teste.zip"
    with open(filename,"rb") as f:
        objFileZip = CompressedFile.get_compressed_file(f)
        
        for name,size in objFileZip.get_each_file_size():
            print("Name: "+name+" size: "+str(size))
    
    