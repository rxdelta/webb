# James Webb's sample code

Here's a place to share codes processing James Webb's images

## count celestials


The first code is named `count-celestials.py` which counts the objects on James Webb's First Deep Field released on July 11, 2022 (You can download the image file from [here](https://webbtelescope.org/contents/media/images/2022/038/01G7JGTH21B5GN9VCYAHBXKSD1) )

assume the gray-scale image as a 3D surface, where the height of each pixel is the value of brightness. the algorithm would scan the gray-scaled image from high-bright points to low-brigh ones, and count the peaks

to run the code, change `IMAGE_PATH` in the file and type 

    python3 count-celestials.py


there are three parameters to configure:
- `BRIGHTNESS_LOWER_THRESHOLD` : a number between 0-1, part of the image with lower brightness than this threshold, would not processed

- `NEIGBORHOOD_STEPS` : number of pixels in neighborhood

- `BRIGHTNESS_TOLERANCE` : a value between 0-1, the algorithm would assume the bightness with this margin (v +/- `BRIGHTNESS_TOLERANCE`%) is equal to v

this code counts around *12K* objects in James Webb's First Deep Field Image,

P.S. : this algorithm has still some FALSE positive/negative detection, and also the performance can be improved