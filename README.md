# SegmentAnything for Microscopy

Tools for segmentation and tracking in microscopy build on top of [SegmentAnything](https://segment-anything.com/).
Segment and track objects in microscopy images interactively with a few clicks!

We implement napari applications for:
- interactive 2d segmentation
- interactive 3d segmentation
- interactive tracking of 2d image data

**Early beta version**

This is an early beta version. Any feedback is welcome, but please be aware that the functionality is under active development and that several features are not finalized or thoroughly tested yet.
Once the functionality has matured we plan to release the interactive annotation applications as [napari plugins](https://napari.org/stable/plugins/index.html).


## Functionality overview

We implement applications for fast interactive 2d and 3d segmentation as well as tracking.
- Left: interactive 2d segmentation
- Middle: interactive 3d segmentation
- Right: interactive tracking

<img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/158459e1-e321-4810-b6b3-4428f436f01b" width="256">
<img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/ca4d6bcc-8674-455b-95c6-0eb516d2bc76" width="256">
<img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/a4a048de-fd3d-4718-b386-2160ac94bbf0" width="256">

## Installation

We require these dependencies:
- [PyTorch](https://pytorch.org/get-started/locally/)
- [SegmentAnything](https://github.com/facebookresearch/segment-anything#installation)
- [napari](https://napari.org/stable/)
- [elf](https://github.com/constantinpape/elf)

We recommend to use conda and provide two conda environment files with all necessary requirements:
- `environment_gpu.yaml`: sets up an environment with GPU support.
- `environment_cpu.yaml`: sets up an environment with CPU support.

To install via conda first clone this repository:
```
git clone https://github.com/computational-cell-analytics/micro-sam
```
and
```
cd micro_sam
```

Then create either the GPU or CPU environment via

```
conda env create -f <ENV_FILE>.yaml
```
Then activate the environment via
```
conda activate sam
```
And install our napari applications and the `micro_sam` library via
```
pip install -e .
```

## Usage

After installing the `micro_sam` python application the three interactive annotation tools can be started from the command line or from a python script (see details below).
They are built with napari to implement the viewer and user interaction. If you are not familiar with napari yet, [start here](https://napari.org/stable/tutorials/fundamentals/quick_start.html).
To use the apps the functionality of [napari point layers](https://napari.org/stable/howtos/layers/points.html) and [napari labels layers](https://napari.org/stable/howtos/layers/labels.html) is of particular importance.

### 2D Segmentation

The application for 2d segmentation can be started in two ways:
- Via the command line with the command `micro_sam.annotator_2d`. Run `micro_sam.annotator_2d -h` for details.
- From a python script with the function `micro_sam.sam_annotator.annotator_2d`. Check out [examples/sam_annotator_2d](https://github.com/computational-cell-analytics/micro-sam/blob/master/examples/sam_annotator_2d.py) for details. 

Below you can see the interface of the application for a cell segmentation example:

<img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/90055f2f-f6f3-4224-ab3c-57e545c278bc" width="768">

The most important parts of the user interface are:
1. The napari layers that contain the image, segmentations and prompts:
    - `prompts`: point layer that is used to provide prompts to SegmentAnything. Positive prompts (green points) for marking the object you want to segment, negative prompts (red points) for marking the outside of the object.
    - `current_object`: label layer that contains the object you're currently segmenting.
    - `committed_objects`: label layer with the objects that have already been segmented.
    - `auto_segmentation`: label layer results from using SegmentAnything for automatic instance segmentation.
    - `raw`: image layer that shows the image data.
2. The prompt menu for changing the currently selected point from positive to negative and vice versa. This can also be done by pressing `t`.
3. The menu for automatic segmentation. Pressing `Segment All Objects` will run automatic segmentation (this can take few minutes if you are using a CPU). The results will be displayed in the `auto_segmentation` layer. 
4. The menu for interactive segmentation. Pressing `Segment Object` (or `s`) will run segmentation for the current prompts. The result is displayed in `current_object`
5. The menu for commiting the segmentation. When pressing `Commit` (or `c`) the result from the selected layer (either `current_object` or `auto_segmentation`) will be transferred from the respective layer to `committed_objects`.

Check out [this video](https://youtu.be/DfWE_XRcqN8) for an overview of the interactive 2d segmentation functionality.

### 3D Segmentation

The application for 3d segmentation can be started as follows:
- Via the command line with the command `micro_sam.annotator_3d`. Run `micro_sam.annotator_3d -h` for details.
- From a python script with the function `micro_sam.sam_annotator.annotator_3d`. Check out [examples/sam_annotator_3d](https://github.com/computational-cell-analytics/micro-sam/blob/master/examples/sam_annotator_3d.py) for details.

<img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/3c35ba63-1b67-48df-9b11-94919bdc7c79" width="768">

The most important parts of the user interface are listed below. Most of these elements are the same as for [the 2d segmentation app](https://github.com/computational-cell-analytics/micro-sam#2d-segmentation).
1. The napari layers that contain the image, segmentation and prompts. Same as for [the 2d segmentation app](https://github.com/computational-cell-analytics/micro-sam#2d-segmentation) but without the `auto_segmentation` layer.
2. The prompt menu.
3. The menu for interactive segmentation.
4. The 3d segmentation menu. Pressing `Segment Volume` (or `v`) will extend the segmentation for the current object across the volume.
5. The menu for committing the segmentation.

Check out [this video](https://youtu.be/5Jo_CtIefTM) for an overview of the interactive 3d segmentation functionality.

### Tracking

The application for interactive tracking (of 2d data) can be started as follows:
- Via the command line with the command `micro_sam.annotator_tracking`. Run `micro_sam.annotator_tracking -h` for details.
- From a python script with the function `micro_sam.sam_annotator.annotator_tracking`. Check out [examples/sam_annotator_tracking](https://github.com/computational-cell-analytics/micro-sam/blob/master/examples/sam_annotator_tracking.py) for details. 

<img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/1fdffe3c-ff10-4d06-a1ba-9974a673b846" width="768">

The most important parts of the user interface are listed below. Most of these elements are the same as for [the 2d segmentation app](https://github.com/computational-cell-analytics/micro-sam#2d-segmentation).
1. The napari layers thaat contain the image, segmentation and prompts. Same as for [the 2d segmentation app](https://github.com/computational-cell-analytics/micro-sam#2d-segmentation) but without the `auto_segmentation` layer, `current_tracks` and `committed_tracks` are the equivalent of `current_object` and `committed_objects`.
2. The prompt menu.
3. The menu with tracking settings: `track_state` is used to indicate that the object you are tracking is dividing in the current frame. `track_id` is used to select which of the tracks after divsion you are following.
4. The menu for interactive segmentation.
5. The tracking menu. Press `Track Object` (or `v`) to track the current object across time.
6. The menu for committing the current tracking result.

TODO link to video tutorial

### Tips & Tricks

TODO
- speeding things up: precomputing the embeddings with a gpu, making input images smaller
- correcting existing segmentaitons via `segmentation_results`
- saving and loading intermediate results via segmentation results

### Limitations

TODO
- automatic instance segmentation limitations


## Using the micro_sam library

TODO
- link to the example image series application


## Contributing

```
micro_sam <- library with utility functionality for using SAM for microscopy data
    /sam_annotator <- the napari plugins for annotation
```


## Citation

If you are using this repository in your research please cite
- [SegmentAnything](https://arxiv.org/abs/2304.02643)
- and our repository on [zenodo](TODO) (we are working on a publication)
