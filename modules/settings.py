from pathlib import Path
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # Get the absolute path of the current file
# FILE = Path(__file__).resolve()
# # Get the parent directory of the current file
# ROOT = FILE.parent
# # Add the root path to the sys.path list if it is not already there
# if ROOT not in sys.path:
#     sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = os.path.abspath(os.path.dirname(__file__))

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'

SOURCES_LIST = [IMAGE, VIDEO, WEBCAM]

# Images config
IMAGES_DIR = os.path.join(ROOT, 'images')
# IMAGES_DIR = ROOT / 'images'

DEFAULT_IMAGE = os.path.join(IMAGES_DIR, 'wa.jpg')
# DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'office_4_detected.jpg'
DEFAULT_IMAGE = './images/wa.jpg'

# Videos config
# VIDEO_DIR = os.path.join(ROOT, 'videos')
VIDEOS_DICT = {
    'video_1': './videos/wa.mp4'
    # 'video_2': VIDEO_DIR / 'video_2.mp4',
    # 'video_3': VIDEO_DIR / 'video_3.mp4',
}

# ML Model detection config
MODEL_DIR =os.path.join(ROOT, 'models')
MODEL_PATH='models/model_- 23 may 2024 14_23.pt'
# DETECTION_MODEL =os.path.join(MODEL_DIR, 'retails.pt') 
DETECTION_MODEL =os.path.join(MODEL_DIR, 'model_- 23 may 2024 13_59.pt') 

# SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# Webcam
WEBCAM_PATH = 0 # Use default webcam


FILE_DATASET='./price_list/database_price.csv'

TIME_DELETE_SAVED_VIDEO = 30