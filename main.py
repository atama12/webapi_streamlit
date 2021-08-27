from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

KEY = "fd853f76f5f04eb8a3c7c6a19e90d55c"
ENDPOINT = "https://20210822atama.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    
    # Open local image file
    local_image = open(filepath, "rb")
    # Call API local image
    tags_result_local = computervision_client.tag_image_in_stream(local_image)

    tags = tags_result_local.tags
    tags_name = []

    for tag in tags:
        tags_name.append(tag.name)

    return tags_name

def detect_objects(filepath):
    
    local_image_objects = open(filepath, "rb")
    
    # Call API with local image
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image_objects)

    objects = detect_objects_results_local.objects
    
    return objects

st.title('物体検出アプリ')
uploaded_file = st.file_uploader('Choose an image...',type=['jpg','png','jpeg'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)

    objects = detect_objects(img_path)    

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font='./Helvetica.ttf',size=50)
    
    for object in objects:
        x = object.rectangle.x 
        y = object.rectangle.y 
        w = object.rectangle.w    
        h = object.rectangle.h
        caption = object.object_property
        

        text_w,text_h = draw.textsize(caption,font=font)
        
        draw.rectangle([(x,y),(x+text_w,y+text_h)], fill='green')
        draw.text((x,y),caption,fill='white',font=font)
        draw.rectangle([(x,y),(x+w,y+h)], fill=None,outline='green',width=5)
        
    st.image(img)
    
    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')




