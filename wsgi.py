from admin import app, db
from admin.control.user_mgmt import registerAdmin
import boto3, os

def downloadDirectoryFroms3(bucketName,remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for object in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(object.key)):
            os.makedirs(os.path.dirname(object.key))
        bucket.download_file(object.key,object.key)

db.create_all()
registerAdmin()
downloadDirectoryFroms3('career-client','build')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000',debug=True)
