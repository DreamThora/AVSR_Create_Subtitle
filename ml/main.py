from pydantic import BaseModel
from service import *
from typing import Union
from fastapi import FastAPI, UploadFile, File
import sys

app = FastAPI()

class VideoData(BaseModel):
    filename: str
    content: str

class FN(BaseModel):
    filename:str

class history_video(BaseModel):
    video_name:str
    video_origin_path:str
    subtitle_path:str
    product_path:str
    status:str

class FileName(BaseModel):
    filename:str

class Sub_Format(BaseModel):
    start:str
    end:str
    message:str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# old lip reading
@app.post("/lipreading/")
def lip_reading(data: VideoData):
    # print(data)
    convert_file(data.filename,data.content)
    video_name,video_origin_path,subtitle_path,product_patth = lip_process_ml(data.filename)
    return_history_video = history_video(video_name= video_name
                                         , video_origin_path= video_origin_path
                                         , subtitle_path= subtitle_path
                                         , product_path= product_patth
                                         ,status = '200 OK')
    
    print(return_history_video)
    return return_history_video

# new lip reading
@app.post("/new_lipreading")
async def lip_reading(file: UploadFile = File(...)):
    print('come',file)
    with open(f"./origin/{file.filename}", "wb") as new_file:
        contents = await file.read()  # Read the contents of the uploaded file
        new_file.write(contents)  # Write the contents to the new file'
    
    print({"filename": file.filename})
    
    video_name, thumbnail_path, video_origin_path, subtitle_path, product_patth = lip_process_ml(file.filename)

    # translate
    new_filename_sub = file.filename.split('.')[0] + '.srt'
    path_sub  = f'/ML_proc/AVSR-Model/files/subtitle/{new_filename_sub }'
    print(new_filename_sub,path_sub)
    eng_sub = read_srt_file(path_sub)

    print('---eng---\n',eng_sub)
    # translate thai
    # แปลและสร้างลิสต์ข้อความที่แปลเป็นภาษาไทย
    thai_sub = translate_messages(eng_sub, 'th')

    # # พิมพ์ลิสต์ข้อมูลที่แปลแล้ว
    # for message in thai_sub:
    #     print(message)
    #     # thai_sub = transalte_thai(eng_sub)
    print(thai_sub)
    # save thai_sub to file
    sub_thai_path = '/ML_proc/AVSR-Model/files/thai_subtitle/' + file.filename.split('.')[0] + '_sub_thai' + '.txt'
    save_thai_sub_file(sub_thai_path,thai_sub)


    return_history_video = history_video(video_name= video_name
                                         , thumbnail_path = thumbnail_path
                                         , video_origin_path= video_origin_path
                                         , subtitle_path= subtitle_path
                                         ,sub_thai_path = sub_thai_path
                                         , product_path= product_patth
                                         ,status = '200 OK')
    
    print('return',return_history_video)
    return return_history_video   

# # return subtitle frame
# @app.post("/getFrameVideo")
# def getFrame(Filename:FN):
#     new_filename_sub = Filename.filename + '.srt'
#     path_sub  = f'/ML_proc/AVSR-Model/files/subtitle/{new_filename_sub }'
#     print(new_filename_sub,path_sub)
#     eng_sub = read_srt_file(path_sub)

#     print('---eng---\n',eng_sub)

#     # translate thai
#     # แปลและสร้างลิสต์ข้อความที่แปลเป็นภาษาไทย
#     thai_sub = translate_messages(eng_sub, 'th')

#     # # พิมพ์ลิสต์ข้อมูลที่แปลแล้ว
#     # for message in thai_sub:
#     #     print(message)
#     #     # thai_sub = transalte_thai(eng_sub)
#     print(thai_sub)
    
#     return {
#         'eng_sub': eng_sub,
#         'thai_sub': thai_sub
#     }

# @app.post("/translate-th")
# def translate_th(data:Subdock_Format):
#     translated_data = translate_messages(data, 'th')

#     # พิมพ์ลิสต์ข้อมูลที่แปลแล้ว
#     for message in translated_data:
#         print(message)

#     print(translated_data)


# @app.post("/download/")
# def download_file(filename:str):
#     return  download(filename)

# # old download
# @app.post("/download/")
# def download_file(Filename:FN):
#     return  download(Filename.filename)

# # new download
# @app.post("/new_download/")
# def download_file(Filename:FN):
#     return  new_download(Filename.filename)

@app.post("/delete/")
def delete_File(Filename:FN):
    print('delete')
    result =  delete(Filename.filename)
    print(result)

@app.get("/test/")
def test():
    print('pass')
    return 'test'
