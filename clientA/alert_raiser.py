import json
from datetime import datetime

import cv2
import pytz
import requests


def raise_alert(activity_recognized, cctv_location,configuration,server_address,frame):

    tz=pytz.timezone('Asia/Kolkata')
    Time = (datetime.datetime.now())
    Time.replace(tzinfo=tz)
    image_name=Time.strftime('%Y_%m_%d_%H_%M_%S_'+str(configuration["id"])+'.jpg')
    message_content = {"site_id": configuration["id"], "activity_recognized": activity_recognized,
                       "cctv_location": cctv_location, "time": str(Time)}
    requests.post(server_address + 'new_alert', json=json.dumps(message_content))
