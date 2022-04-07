from botocore.client import Config
import boto3
from datetime import datetime
import json
import os
f=open('/home/optisoladmin/Woolworths/theft-detection/openpose/Optiscan/Optiscan-Theft-detection/modules/capture-video/.git/config.json','r')
data=json.load(f)
f.close()
def upload_folder_to_s3(s3bucket, inputDir, s3Path):
        print("Uploading results to s3 initiated...")
        print("Local Source:",inputDir)
        os.system("ls -ltR " + inputDir)

        print("Dest  S3path:",s3Path)

        try:
            for path, subdirs, files in os.walk(inputDir):
                for file in files:
                    dest_path = path.replace(inputDir,"")
                    __s3file = os.path.normpath(s3Path + '/' + dest_path + '/' + file)
                    __local_file = os.path.join(path, file)
                    print("upload : ", __local_file, " to Target: ", __s3file, end="")
                    s3.upload_file(__local_file,s3bucket, __s3file)
                    print(" ...Success")
        except Exception as e:
            print(" ... Failed!! Quitting Upload!!")
            print(e)
            raise e



config = Config(connect_timeout=500, retries={'max_attempts': 10})
now = datetime.now()
date=now.date()

for i in data.items(): 
    s3 = boto3.client('s3', aws_access_key_id=i[1]["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=i[1]["AWS_SECRET_ACCESS_KEY"], config=config)
    
    save_path='/home/optisoladmin/Woolworths/theft-detection/openpose/Optiscan/Optiscan-Theft-detection/data/recordings/{}/'.format(date)
    print("save_path: ",save_path)
    # crr_path='/home/optisoladmin/Woolworths/theft-detection/openpose/Optiscan/Optiscan-Theft-detection/data/recordings/'
    # s3.upload_file('./test/','woolworths-cctv-footages','woolworths-videos/')
    upload_folder_to_s3(i[1]['bucket'],save_path,'woolworths-videos/{}/'.format(date))       

os.rmdir(save_path)
