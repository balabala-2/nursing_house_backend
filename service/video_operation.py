from fastapi.responses import StreamingResponse
from dao.user_head_img_operation import get_user_head_img
from schemas.request import Face_video_info
from algorithm.face_detection.face_pose import Face_pose
from algorithm.invade_detection.detect import Invade_detect
from algorithm.emotion_detection.detect import Detection
from algorithm.fall_detection.detect import Fall_detection
from algorithm.interactive_detection.detect import Interactive_detection
from algorithm.interactive_detection.audio import Audio_detection
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
sched.start()

def get_img_by_id(user_type, user_id):
    img = get_user_head_img(user_type=user_type, user_id=user_id)
    return StreamingResponse(iter([img]), media_type='image/jpg')

def face_image_collect(face_video_info: Face_video_info):
    return Face_pose(face_video_info).video_generate()

def get_invade_video():
    # return 0
    return Invade_detect().video_generate()

def get_emotion_video():
    # return 0
    return Detection().video_generate()

def get_fall_video():
    # return 0
    return Fall_detection().video_generate()

def audio_job():
    Audio_detection.init()
    Audio_detection.run()

def get_interactive_audio():
    job = sched.get_job(job_id='audio_job')
    print(job)
    if job is None:
        sched.add_job(func=audio_job, id='audio_job')

def get_interactive_video():
    get_interactive_audio()
    return Interactive_detection().video_generate()

