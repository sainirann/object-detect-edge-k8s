from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import range
from PIL import Image
from flask import Flask
from flask import request

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import collections
# Set headless-friendly backend.
import matplotlib;matplotlib.use('Agg')  # pylint: disable=multiple-statements
# import matplotlib.pyplot as plt  # pylint: disable=g-import-not-at-top
import numpy as np
import os
import requests
import six
import sys

app = Flask(__name__)

PATH_TO_LABELS = 'mscoco_complete_label_map.pbtxt'

PORT = 9080

BIND_HOST = '0.0.0.0'
IMAGE_PATH = 'object_detection.jpeg'

URL_HOST = os.getenv('MY_POD_IP')

MODEL_SERVER_URL = f"http://{URL_HOST}:8080/v1/models/default:predict"
EMAIL_NOTIFIER_URL = f"http://{URL_HOST}:3000/send_notification"

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)


def get_boxes(image, boxes, classes, scores, category_index, instance_masks=None, instance_boundaries=None,
              keypoints=None, track_ids=None, use_normalized_coordinates=False, max_boxes_to_draw=20,
              min_score_thresh=.5, agnostic_mode=False, line_thickness=4, groundtruth_box_visualization_color='black',
              skip_scores=False, skip_labels=False, skip_track_ids=False):
    box_to_display_str_map = collections.defaultdict(list)
    box_to_color_map = collections.defaultdict(str)
    box_to_instance_masks_map = {}
    box_to_instance_boundaries_map = {}
    box_to_keypoints_map = collections.defaultdict(list)
    box_to_track_ids_map = {}
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            if instance_masks is not None:
                box_to_instance_masks_map[box] = instance_masks[i]
            if instance_boundaries is not None:
                box_to_instance_boundaries_map[box] = instance_boundaries[i]
            if keypoints is not None:
                box_to_keypoints_map[box].extend(keypoints[i])
            if track_ids is not None:
                box_to_track_ids_map[box] = track_ids[i]
            if scores is None:
                box_to_color_map[box] = groundtruth_box_visualization_color
            else:
                display_str = ''
                if not skip_labels:
                    if not agnostic_mode:
                        if classes[i] in six.viewkeys(category_index):
                            class_name = category_index[classes[i]]['name']
                        else:
                            class_name = 'N/A'
                        display_str = str(class_name)
                if not skip_scores:
                    if not display_str:
                        display_str = '{}%'.format(int(100 * scores[i]))
                    else:
                        display_str = '{}: {}%'.format(display_str, int(100 * scores[i]))
                if not skip_track_ids and track_ids is not None:
                    if not display_str:
                        display_str = 'ID {}'.format(track_ids[i])
                    else:
                        display_str = '{}: ID {}'.format(display_str, track_ids[i])
                box_to_display_str_map[box].append(display_str)
                if agnostic_mode:
                    box_to_color_map[box] = 'DarkOrange'
                elif track_ids is not None:
                    prime_multipler = vis_util._get_multiplier_for_color_randomness()
                    box_to_color_map[box] = vis_util.STANDARD_COLORS[
                        (prime_multipler * track_ids[i]) % len(vis_util.STANDARD_COLORS)]
                else:
                    box_to_color_map[box] = vis_util.STANDARD_COLORS[classes[i] % len(vis_util.STANDARD_COLORS)]

    return box_to_display_str_map


def show_inference(image_path):
    image_np = np.array(Image.open(image_path))
    payload = {"instances": [image_np.tolist()]}
    res = requests.post(MODEL_SERVER_URL, json=payload)
    output_dict = res.json()['predictions'][0]
    boxes = get_boxes(image_np, np.array(output_dict['detection_boxes']),
        np.array(output_dict['detection_classes'], dtype=np.int),
        np.array(output_dict['detection_scores']),
        category_index,
        instance_masks=output_dict.get('detection_masks_reframed', None),
        use_normalized_coordinates=True,
        line_thickness=8)
    for box, categories in boxes.items():
        category_score = dict()
        for category_and_score in categories:
            category, score = category_and_score.split(':')
            score = int(score.replace('%', ''))
            category_score[category] = score
        category, score = max(category_score.items(), key=lambda k: k[1])
        if category in categories_to_notify:
            print('Person Found')
            return True
        else:
            print('Not a person')
    return False


@app.route('/', methods=['POST'])
def do_post():
    image_file = request.files['image']
    image_file.save(IMAGE_PATH)
    decision = show_inference(IMAGE_PATH)
    if decision:
        res = requests.post(EMAIL_NOTIFIER_URL)
        if res.status_code != 200:
            print('Email not properly sent')
    if os.path.exists(IMAGE_PATH):
        os.remove(IMAGE_PATH)
    return 'ok', 200


categories_to_notify = set([k for k in sys.argv[1].split(',')]) if len(sys.argv) == 2 else {'person'}

app.run(host=BIND_HOST, port=PORT, debug=True)
