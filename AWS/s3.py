
import os.path

from boto.s3.key import Key, KeyFile
from boto.s3.bucket import Bucket
import textwrap
import boto
import re

class S3Storage(object):
    """
    Class for manipulating the Amazon S3 Storage

    Dependencies:
        - Assumes that your AWS keys are located in ~/.boto

    Example:
        [Credentials]
        aws_access_key_id = <your aws acess key, no quotes needed>
        aws_secret_access_key = <your secret key>

    """

    def __init__(self,bucket):
        """
        Initilize the class with the bucket name to access.
        :param bucket:
        :return:
        """

        self._bucketName = bucket
        self._re_bucket = bucket
        self._conn = None
        self._bconn = {}

    def get_connection(self):
        """
        Connect to the S3 service using boto.
        """

        # Access key and secret key stored in users ~/.boto
        #conn = S3Connection()

        if self._conn:
            return self._conn

        self._conn = boto.connect_s3()
        return self._conn

    def connect_bucket(self, bucket=None):
        """
        Connect to a named bucket, or to the initialilzed bucket.
        :param bucket:
        :return:
        """

        bucket = bucket or self._bucketName

        if self._bconn.has_key(bucket):
            return self._bconn[bucket]

        try:
            bconn = self.get_connection().get_bucket(bucket)
            self._bconn[bucket] = bconn
        except boto.S3ResponseError as e:
            bconn = None

        return bconn

    def getBucket(self):
        return self._bucketName

    def getBucketList(self, bucket=None):
        """
        Call the boto list function on the deafult bucket connection.
        """

        bconn = self.connect_bucket(bucket=bucket)
        if bconn:
            return bconn.list()

        return []

    def buildPath(self, path, file):
        """
        The bucket is stored in the paths, so we need to remove it..
        """

        path = os.path.join(path, file)
        m = re.match('^%s/(.*)$' % self._re_bucket,path)
        if m:
            path = m.group(1) # remove the leading bucket!

        return path

    def getFile(self, path, file, localfile):
        """
        Read the contents of the file given by path+file into
        the localfile.

        :param path:
        :param file:
        :param localfile:
        :return:
        """

        bconn = self.connect_bucket()
        if not bconn:
            raise Exception("No connection to default bucket ({}).".format(self._bucketName))

        k = Key(bconn)
        k.name = self.buildPath(path,file)
        if k.exists():
            k.get_contents_to_file(localfile)

    def exists(self,path,file):
        """
        Check if a file exists on the S3 server.
        """
        bconn = self.connect_bucket()
        if not bconn:
            raise Exception("No connection to default bucket ({}).".format(self._bucketName))

        k = Key(bconn)
        k.key = self.buildPath(path,file)
        return k.exists()

    def getFileData(self, path, file):
        """
        Get file data as a string.

        :param path:
        :param file:
        :return:
        """
        bconn = self.connect_bucket()
        if not bconn:
            raise Exception("No connection to default bucket ({}).".format(self._bucketName))

        k = Key(bconn)
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

    def get_file_from_location(self, path, file, location):
        """
        Perform a file seek, and return the file contents from that position.

        Uses the KeyFile to perform low-level file operations.

        :param path:
        :param file:
        :param location:
        :return:
        """

        bconn = self.connect_bucket()
        if not bconn:
            raise Exception("No connection to default bucket ({}).".format(self._bucketName))

        k = Key(bconn)
        k.key = self.buildPath(path,file)

        data = None
        if k.exists():
            kf = KeyFile(k)
            kf.seek(location)
            size = k.size
            data = kf.read(size-location)

        return data


    def storeFileData(self, path, file, data):
        """
        Write data to the path+file.

        :param path:
        :param file:
        :param data:
        :return:
        """
        bconn = self.connect_bucket()
        if not bconn:
            raise Exception("No connection to default bucket ({}).".format(self._bucketName))

        k = Key(bconn)
        k.key = self.buildPath(path,file)
        try:
            fileData = k.set_contents_from_string(data)
        except boto.exception.S3ResponseError as e:
            pass

    def storeFile(self,localfile,path,file):
        bconn = self.connect_bucket()
        if not bconn:
            raise Exception("No connection to default bucket ({}).".format(self._bucketName))

        k = Key(bconn)
        k.name = os.path.join(path,file)
        print ("Key name:%s" % k.name)
        k.set_contents_from_filename(localfile,replace=True)

def main():
    """
    Do some testing. But you'll need to provide a bucket.
    :return:
    """
    bucket = "partsim_eddev_projects"
    ps = S3Storage(bucket)

    data = textwrap.dedent("""
        Now is the time for all good men
        When in the course
        This is a test
        Hello World.
    """)

    ps.storeFileData('', 'testfile.txt', data)

    loc = data.find('Hello')

    tail = ps.get_file_from_location('', 'testfile.txt', loc)
    print("Here is the tail:{}".format(tail))



if __name__ == '__main__':
    main()


