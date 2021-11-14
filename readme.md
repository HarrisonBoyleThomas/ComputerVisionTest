This project is a little computer vision experiment I worked on in early 2019
The python file features two classes: the camera and the sensor
The program uses your computer's webcam if available, and will crash
if you do not have one
The camera detects changes in its environment, and can mark target locations
as items with the most movement. This is easily seen if moving your head while
the program is running. The sensor is more accurate if the webcam is still

You can tinker with the drawn output on the screen by using drawOnScreen, drawVisionOnScreen, blitTarget and blitTargets available in the Sensor class

The program is not built for performance, and is not be suitable for real-time applications. It was only intended as an experiment

The camera records the world using the webcame, and detects changes between frames, which produces a monochrome image with white = high change, black = no change

The camera detects all pixels with a change above the specified threshold. For efficiency, a target is randomly chosen to be the "current target", but this could be improved

The camera's vision is drawn on screen, then the camera's targets are drawn over this to show the output


REQUIREMENTS:

    opencv for python (python3 -m pip install opencv-python)

    pygame (python3 -m pip install pygame)

@Author Harrison Boyle-Thomas
@Date: ~2019
