from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import collections
# Set headless-friendly backend.
import matplotlib;

matplotlib.use('Agg')  # pylint: disable=multiple-statements
import matplotlib.pyplot as plt  # pylint: disable=g-import-not-at-top
import numpy as np
import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import six
from six.moves import range
from six.moves import zip
import tensorflow as tf

from object_detection.core import standard_fields as fields
from object_detection.utils import shape_utils

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


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
