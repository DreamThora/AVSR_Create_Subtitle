import base64
import os

# from moviepy.editor import VideoFileClip
from translate import Translator
import sys


# แปลง base64 เป็น video file
def convert_file(filename,content):
    origin_path = f'./origin/{filename}'
    content = content.replace('data:video/mp4;base64,','')
    print(content)
    with open(origin_path, "wb") as video_file:
        video_file.write(base64.b64decode(content))

    video_file.close()

    print('save video success')
    return '200 OK'

# set path
def file_path(filename):
    origin_path = f'/files/origin_video/{filename}'
    name,ex = filename.split(".")
    new_filename_merge = name + '_sub.' + ex
    merge_path  = f'/files/merge_video/{new_filename_merge }'

    new_filename_sub = name + '.txt'
    sub_path  = f'/files/subtitle/{new_filename_sub }'
    

    # return name, extendtion file, origin path, product file, product path, subtitle_path
    return name, ex, new_filename_merge,origin_path, merge_path , sub_path

# แปลง video file เป็น base64
def download(filename):
    print('download')
    # name,ex = filename.split(".")
    # new_filename_merge = name + '_sub.' + ex
    # path_merge  = f'./merge_file/{new_filename_merge }'

    name, ex, new_filename_merge, origin_path, merge_path, sub_path = file_path(filename)

    # origin video
    with open(origin_path , "rb") as video_file:
        video_data = video_file.read()
        # print(video_data)
        content_origin  = base64.b64encode(video_data).decode('utf-8')

    video_file.close()

    # merge video
    with open(merge_path , "rb") as video_file:
        video_data = video_file.read()
        content_merge  = base64.b64encode(video_data).decode('utf-8')

    video_file.close()


    # subtitle text
    with open(sub_path , "rb") as video_file:
        video_data = video_file.read()
        content_sub  = base64.b64encode(video_data).decode('utf-8')

    video_file.close()
    print(content_merge)
    print(content_sub)
    print('origin')

    return {
        'content_origin' : content_origin,
        'content_merge' : content_merge,
        'content_sub' : content_sub
    } 

def new_download(filename):
    print('download')
    # name,ex = filename.split(".")
    # new_filename_merge = name + '_sub.' + ex
    # path_merge  = f'./merge_file/{new_filename_merge }'

    name, ex, new_filename_merge, origin_path, merge_path, sub_path = file_path(filename)

    # # origin video
    # with open(origin_path , "rb") as video_file:
    #     video_data = video_file.read()
    #     # print(video_data)
    #     content_origin  = base64.b64encode(video_data).decode('utf-8')

    # video_file.close()

    # # merge video
    # with open(merge_path , "rb") as video_file:
    #     video_data = video_file.read()
    #     content_merge  = base64.b64encode(video_data).decode('utf-8')

    # video_file.close()


    # # subtitle text
    # with open(sub_path , "rb") as video_file:
    #     video_data = video_file.read()
    #     content_sub  = base64.b64encode(video_data).decode('utf-8')

    # video_file.close()
    # print(content_merge)
    # print(content_sub)
    print('new',origin_path,merge_path,sub_path)

    return {
        'origin_path' : origin_path,
        'merge_path' : merge_path,
        'sub_path' : sub_path
    } 

# delete file
def delete(filename):
    print('delete')
    # name,ex = filename.split(".")
    # new_filename_merge = name + '_sub.' + ex
    # path_merge  = f'./merge_file/{new_filename_merge }'

    name, ex, origin_path, new_filename_merge, path_merge, path_sub = file_path(filename)
    path_srt = name + '.srt'

    # open 
    # close
    # os.close(origin_path)
    # os.close(path_merge)
    # os.close(path_sub)
    # os.close(path_srt)
    # # origin
    # os.remove(origin_path)
    # # product
    # os.remove(path_merge)
    # # subtitle
    # os.remove(path_sub)
    # # srt
    # os.remove(path_srt)

    # merge video
    with open(path_merge , "rb") as video_file:
        video_data = video_file.read()
        content_merge  = base64.b64encode(video_data).decode('utf-8')

    video_file.close()

    # subtitle text
    with open(path_sub , "rb") as video_file:
        video_data = video_file.read()
        content_sub  = base64.b64encode(video_data).decode('utf-8')

    video_file.close()

    return {
       "success delete"
    } 

# # translate
# def translate_text(text, target_language):
#     translator = Translator(to_lang=target_language)
#     translation = translator.translate(text)
#     return translation

# # to thai
# def transalte_thai(text_to_translate):
#     # print(text_to_translate)
#     sys.stdout.reconfigure(encoding='utf-8')
#     # text_to_translate = "Hello, how are you?"
#     target_language = 'th'  # Change this to the target language code

#     translated_text = translate_text(text_to_translate, target_language)
#     decoded_text = translated_text.encode('utf-8').decode('utf-8')
#     # print(decoded_text)
#     print(f"Translated text: {decoded_text}")

#     return decoded_text

# translate text
def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation

# translate list text
def translate_messages(messages_list, target_language):
    translated_list = []
    for message in messages_list:
        translated_message = {
            'start': message['start'],
            'end': message['end'],
            'message': translate_text(message['text'], target_language)
        }
        translated_list.append(translated_message)

    return translated_list

def save_thai_sub_file(filename, thai_sub):
    with open(filename, 'w') as file:
        for item in thai_sub:
            file.write('%s\n' % item)

# read subtitle file
def read_srt_file(file_path):
    srt_format = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        entry = {}
        for line in lines:
            line = line.strip()
            
            if line.isdigit():
                if entry:
                    srt_format.append(entry)
                entry = {'id': int(line)}
            elif ' --> ' in line:
                start, end = line.split(' --> ')
                entry['start'] = start
                entry['end'] = end
            elif line:
                entry.setdefault('text', '')
                entry['text'] += ' ' + line

        if entry:
            srt_format.append(entry)

    return srt_format


cfg = {
    "gpu_idx": 0,
}

# lipreading process
def lip_process_ml(filename):
    try:
        #/ML_proc
        # current_directory = os.getcwd()
        list_file = arr = os.listdir("/ML_proc/AVSR-Model/files/origin_video/")
        print(list_file)
        os.system(f"python3.8 /ML_proc/AVSR-Model/infer.py {filename}")
        origin_path = f"/files/original_video/{filename}"
        vid_name = filename.split('/')[-1].split('.')[0]
        subtitle_path = f'/files/subtitle/{vid_name}.srt'
        thumbnail_path = f"/files/thumbnail/{vid_name}.png"
        product_path = f'/files/merge_video/{filename}'
    except Exception as e:
        print('Error = ', e)  
    return filename,thumbnail_path,origin_path,subtitle_path,product_path