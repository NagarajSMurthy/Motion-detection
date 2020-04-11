# Motion-detection

Visual motion indicates dynamics in the scene such as moving objects, behavior, tracking objects, analyze trajectories, etc. 
A video is nothing but a sequence of frames captured over time. A minimum number of frames needed to detect the motion pattern is two.

### Motion detection by background subtraction

One of the simplest ways to detect motion is by background subtraction which works on the principle of moving averages. Another method is Optical flow. 
![](Motion_detector.gif)

### Optical flow
Optical flow refers to the problem of estimating a vector field of pixel displacememt in a sequence of images. That is, when we fix our attention to a single point and measure velocities flowing through that location, then the problem is called Optical Flow. 
Optical flow methods try to calculate the motion between two image frames which are taken at times 't' and 't+dt' at every position. These methods are based on Taylor's series approximations. 

  ### Lucas-Kanade method
  Assumptions:
  1. The motion is essentially constant in a local neighborhood of pixels(window) 
  2. The displacement of the image contents between two frames is small. 
  
  That is why, Lucas-kanade method only works for small movements and fails when there is large motion. However, the OpenCV     implementation of this algorithm makes use of the concept of Optical pyramids where it tries to detect large motion on a     reduced resolution. 
![](optical_flow.gif)
  
