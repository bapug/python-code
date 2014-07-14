import sys
import os.path

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import re

class BasicStorage(object):
    """
    Class for manipulating an Amazon S3 Storage area
    """

    def __init__(self,bucket):
        self._bucketName = bucket
        self._re_bucket = bucket
        self._conn = None
        self._bconn = None

        self._projFiles = []

    def connect(self):
        """
        Connect to the S3 service using boto and then connect to the
        specified bucket.
        """

        # Access key and secret key stored in users ~/.boto
        #conn = S3Connection()
        self._conn = boto.connect_s3()

        self._bconn= self._conn.get_bucket(self._bucketName)

    def setBucket(self,bucket):
        """
        Set the new bucket name and connect to the bucket.
        """
        if self._bconn:
            self._bconn.close()
            self._bconn = None
        self._bucketName = bucket

    def getBucket(self):
        return self._bucketName

    def getBucketList(self):
        """
        Call the boto list function on the bucket connection.
        """
        if self._bconn:
            return self._bconn.list()
        return None

    def setSearchBucket(self,bucket):
        """
        If we are moving files, or we think the bucket in the path is wrong,
        we can specify a new re search bucket.
        """

        b = self._re_bucket
        if not bucket:
            self._re_bucket = self._bucketName
        else:
            self._re_bucket = bucket

        return b # return previous value

    def buildPath(self,path,file):
        """
        The bucket is stored in the paths, so we need to remove it..
        """

        path = os.path.join(path,file)
        m = re.match('^%s/(.*)$' % self._re_bucket,path)
        if m:
            path = m.group(1) # remove the leading bucket!

        return path

    def getFile(self,path,file,localfile):
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        k.name = self.buildPath(path,file)
        if k.exists():
            print ("Key name:%s" % k.name)
            k.get_contents_to_file(localfile)

    def exists(self,path,file):
        """
        Check if a file exists on the S3 server.
        """
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        k.key = self.buildPath(path,file)
        return k.exists()

    def getFileData(self,path,file):
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        k.key = self.buildPath(path,file)
        fileData = None
        try:
            if k.exists():
                fileData = k.get_contents_as_string()
            else:
                return None
        except boto.exception.S3ResponseError as e:
            pass

        return fileData

    def storeFileData(self,path,file,data):
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        k.key = self.buildPath(path,file)
        print ("Key name:%s" % k.name)
        try:
            fileData = k.set_contents_from_string(data)
        except boto.exception.S3ResponseError as e:
            pass

    def storeFile(self,localfile,path,file):
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        k.name = os.path.join(path,file)
        print ("Key name:%s" % k.name)
        k.set_contents_from_filename(localfile,replace=True)

    def removeFile(self,path,file):
        if self._conn == None:
            raise Exception("Must connect first.")

        pass

    def getProject(self,ver,uid,pid,destdir):
        """
        Retrieve the files for a project

        Pass in the version, uid, pid and destination dir.
        The files will be read from s3 and stored with the same
        name in the destdir.
        """
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        path = os.path.join('model-%s' % ver, 'uid-%d' % uid, 'pid-%d' % pid)

        for file in self._projFiles:
            name = os.path.join(path,file)
            k.name = name
            dest = os.path.join(destdir,file)
            k.get_contents_to_filename(dest)

    def saveProject(self,ver,uid,pid,srcdir):
        """
        Save the project files from the given source dir.

        Load the project files from 'srcdir' and save them
        """
        if self._conn == None:
            raise Exception("Must connect first.")

        k = Key(self._bconn)
        path = os.path.join("/",'model-%s' % ver, 'uid-%d' % uid, 'pid-%d' % pid)

        for file in self._projFiles:
            src = os.path.join(destidr,name)
            if os.path.exists(src):
                name = os.path.join(path,file)
                k.name = name
                k.set_contents_from_filename(src)


def main():
    ps = BasicStorage("partsim_eddev_projects")
    ps.connect()
    ps.setProjectFiles(['model.xml.gz','probes.json.gz','simdata.json.gz','simparams.json.gz'])

    #ps.storeFile(__file__,'/model-v1.0/uid-1/pid-xx',"apythonfile.py")


    ps.getProject('v1.0',1,21,'.')
    #mfile = ps.getFile('model-v1.0/uid-1/pid-21','model.xml.gz')
    #pfile = ps.getFile('model-v1.0/uid-1/pid-21','probes.json.gz')

if __name__ == '__main__':
    main()


