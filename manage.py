from admin import app, db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
import sqlalchemy_utils
import boto3, os

def downloadDirectoryFroms3(bucketName,remoteDirectoryName):
    os.system('rm -rf build')
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for object in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(object.key)):
            os.makedirs(os.path.dirname(object.key))
        bucket.download_file(object.key,object.key)

# react app 빌드파일 업데이트
downloadDirectoryFroms3('career-client','build')
print('S3 Download complete!')

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()