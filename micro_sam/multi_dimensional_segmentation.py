from typing import Any, Optional

import numpy as np
from segment_anything.predictor import SamPredictor

from . import util
from .prompt_based_segmentation import segment_from_mask


def segment_mask_in_volume(
    segmentation: np.ndarray,
    predictor: SamPredictor,
    image_embeddings: util.ImageEmbeddings,
    segmented_slices: np.ndarray,
    stop_lower: bool,
    stop_upper: bool,
    iou_threshold: float,
    projection: str,
    progress_bar: Optional[Any] = None,
    box_extension: int = 0,
):
    """
    """
    assert projection in ("mask", "bounding_box", "points")
    if projection == "mask":
        use_box, use_mask, use_points = True, True, False
    elif projection == "points":
        use_box, use_mask, use_points = True, True, True
    else:
        use_box, use_mask, use_points = True, False, False

    def _update_progress():
        if progress_bar is not None:
            progress_bar.update(1)

    def segment_range(z_start, z_stop, increment, stopping_criterion, threshold=None, verbose=False):
        z = z_start + increment
        while True:
            if verbose:
                print(f"Segment {z_start} to {z_stop}: segmenting slice {z}")
            seg_prev = segmentation[z - increment]
            seg_z = segment_from_mask(predictor, seg_prev, image_embeddings=image_embeddings, i=z,
                                      use_mask=use_mask, use_box=use_box, use_points=use_points,
                                      box_extension=box_extension)
            if threshold is not None:
                iou = util.compute_iou(seg_prev, seg_z)
                if iou < threshold:
                    msg = f"Segmentation stopped at slice {z} due to IOU {iou} < {iou_threshold}."
                    print(msg)
                    break
            segmentation[z] = seg_z
            z += increment
            if stopping_criterion(z, z_stop):
                if verbose:
                    print(f"Segment {z_start} to {z_stop}: stop at slice {z}")
                break
            _update_progress()

    z0, z1 = int(segmented_slices.min()), int(segmented_slices.max())

    # segment below the min slice
    if z0 > 0 and not stop_lower:
        segment_range(z0, 0, -1, np.less, iou_threshold)

    # segment above the max slice
    if z1 < segmentation.shape[0] - 1 and not stop_upper:
        segment_range(z1, segmentation.shape[0] - 1, 1, np.greater, iou_threshold)

    verbose = False
    # segment in between min and max slice
    if z0 != z1:
        for z_start, z_stop in zip(segmented_slices[:-1], segmented_slices[1:]):
            slice_diff = z_stop - z_start
            z_mid = int((z_start + z_stop) // 2)

            if slice_diff == 1:  # the slices are adjacent -> we don't need to do anything
                pass

            elif z_start == z0 and stop_lower:  # the lower slice is stop: we just segment from upper
                segment_range(z_stop, z_start, -1, np.less_equal, verbose=verbose)

            elif z_stop == z1 and stop_upper:  # the upper slice is stop: we just segment from lower
                segment_range(z_start, z_stop, 1, np.greater_equal, verbose=verbose)

            elif slice_diff == 2:  # there is only one slice in between -> use combined mask
                z = z_start + 1
                seg_prompt = np.logical_or(segmentation[z_start] == 1, segmentation[z_stop] == 1)
                segmentation[z] = segment_from_mask(
                    predictor, seg_prompt, image_embeddings=image_embeddings, i=z,
                    use_mask=use_mask, use_box=use_box, use_points=use_points,
                    box_extension=box_extension
                )
                _update_progress()

            else:  # there is a range of more than 2 slices in between -> segment ranges
                # segment from bottom
                segment_range(
                    z_start, z_mid, 1, np.greater_equal if slice_diff % 2 == 0 else np.greater, verbose=verbose
                )
                # segment from top
                segment_range(z_stop, z_mid, -1, np.less_equal, verbose=verbose)
                # if the difference between start and stop is even,
                # then we have a slice in the middle that is the same distance from top bottom
                # in this case the slice is not segmented in the ranges above, and we segment it
                # using the combined mask from the adjacent top and bottom slice as prompt
                if slice_diff % 2 == 0:
                    seg_prompt = np.logical_or(segmentation[z_mid - 1] == 1, segmentation[z_mid + 1] == 1)
                    segmentation[z_mid] = segment_from_mask(
                        predictor, seg_prompt, image_embeddings=image_embeddings, i=z_mid,
                        use_mask=use_mask, use_box=use_box, use_points=use_points,
                        box_extension=box_extension
                    )
                    _update_progress()

    return segmentation
