# prepare-ck-
create the flow images of CK+ for two-stream emotion-recognition
## description
Most of the code to generate optical flow images is designed for the video. However I download the CK+ dataset is consist of a series of pictures which can be regarded as frames of the video.

Firstly run prepare_ck.py to generate the rgb images gather by their labels.

Then extract_flow.py is to generate optical flow images for CK+.
