import os

import boto3

from hrmsrad.app.conf.development.settings import CONTENT_DIR

access_key_id =  'AKIAJHCBPERZTKMNBLUQ'
secret_access_key ='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'

photo = CONTENT_DIR+'/media/tmppics/'
pic = CONTENT_DIR+'/media/documents/'

source = os.path.basename(photo)
print(source)
target = os.path.basename(pic)
print(target)
client = boto3.client('rekognition',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key =secret_access_key,
                      region_name ='us-west-2'
                     )

with open(source, 'rb') as source_image:
    source_bytes = source_image.read()
with open(target, 'rb') as target_image:
    target_bytes = target_image.read()

response = client.rekoginiton(SourceImage={'Bytes': source_bytes},
                                        TargetImage={'Bytes':target_bytes})
for key, value in response.items():
    if key in ('FaceMatches', 'UnmatchedFaces'):
        print(key)
        for att in value:
            print(att)
print(response)


