from cv2 import *
from cv2 import VideoCapture, rotate, ROTATE_90_COUNTERCLOCKWISE
import pygame
from pygame.locals import *
from random import randint

"""
This file is a little computer vision experiment I worked on in early 2019
The file features two classes: the camera and the sensor
The program uses your computer's webcam if available, and will crash
if you do not have one
The camera detects changes in its environment, and can mark target locations
as items with the most movement. This is easily seen if moving your head while
the program is running. The sensor is more accurate if the webcam is still

You can tinker with the drawn output on the screen by using drawOnScreen, drawVisionOnScreen, blitTarget and blitTargets available in the Sensor class

The program is not built for performance, and is not be suitable for real-time applications

@Author Harrison Boyle-Thomas
@Date: ~2019
"""

pygame.init()

window = pygame.display.set_mode((640, 480))

#cam = VideoCapture(0)
#s, img = cam.read()

"""
#surface = img
while True:
    s, img = cam.read()
    if s:
        a = 0

        surface = pygame.surfarray.make_surface(img)
        #for y in range(0, len(img)-1):
        #    for x in range(0, len(img[y])-1):
        #        a = a + 1
        #        surface.set_at((x,y), img[y][x])
        destroyWindow("cam-test")
        window.blit(surface,  (0,0))
        pygame.display.update()
        pygame.event.get()
"""



"""
Camera class that holds information about frame differences seen by the device's camera
"""
class Camera():
    """
        previousImage = image from the last cycle
        currentImage = image from the current cycle
        cam = the device's camera
        comparisonImage = the image used to detect changes between prev and cur images
        locations = list of key change areas on the comparisonImage
    """
    def __init__ (self):
        self.previousImage = None
        self.currentImage = None
        self.cam = VideoCapture(0)
        self.comparisonImage = None
        self.locations = []


    """
        updates the prev/cur images using the device's camera
        returns the currentImage
    """
    def getNextImage(self):
        self.clearLocations()
        successful, image = self.cam.read()
        if(successful):
            image = rotate(image, ROTATE_90_COUNTERCLOCKWISE)
            surface = pygame.surfarray.make_surface(image)
            if self.currentImage == None:
                self.currentImage = surface
            self.previousImage = self.currentImage
            self.currentImage = surface
            self.setComparisonImage()
            return surface
        return None


    """
        resets the locations list
    """
    def clearLocations(self):
        self.locations = []
    """
        creates a comparionImage by subtracting the new image from the old image
        this new image is monochrome- whiter = more change, darker = less change
        returns the comparison image
    """
    def setComparisonImage(self):
        if self.previousImage == None or self.currentImage == None:
            return None
        surface = self.previousImage.copy()
        #surface = pygame.surface.Surface((640,480)).convert()
        #surface.blit(self.previousImage, (0,0))
        surface.blit(self.currentImage, (0,0), special_flags = pygame.BLEND_RGBA_SUB)
        self.comparisonImage = surface

        
        return surface


    """
        return the comparisonImage
    """
    def getComparisonImage(self):
        return self.comparisonImage


    """
        using the comparison image, the camera looks for pixels with a colour value greater than the threshold,
        and marks these locations as possible targets
        @param threshold = average colour the pixel must be greater than to be marked
        returns the target locations
    """
    def getTargetLocations(self, threshold):
        if len(self.locations) > 0:
            return self.locations
        #locations = []
        #surface = self.getComparisonImage()
        #if surface == None:
        #    return locations
        #for x in range(0, surface.get_width()):
        #    for y in range(0, surface.get_height()):
        #        colour = surface.get_at((x,y))
        #        colourSum = colour[0] + colour[1] + colour[2]
        #        if colourSum/3 >= threshold:
        #            locations.append((x,y))
        #self.locations = locations


        #This new method is slightly faster than the older method, and produces the same results
        if(self.getComparisonImage() == None):
            return []
        array = pygame.PixelArray(self.getComparisonImage())
        locations = []
        for x in range(0, self.getComparisonImage().get_width()):
            for y in range(0, self.getComparisonImage().get_height()):
                colour = pygame.Color(array[x,y])
                colourSum = (colour[0] + colour[1] + colour[2])/3
                if colourSum >= threshold:
                    locations.append((x,y))
                
        self.locations = locations
        return locations

    """
        draws a mark at the given locations
        @param locations = list of target locations(x,y) on screen
    """
    def blitLocations(self, locations):
        mark = pygame.surface.Surface((5,5))
        mark.fill((255,0,0))
        for loc in locations:
            window.blit(mark, (loc[0]-2, loc[1]-2))

    """
        returns the current cycle image
    """
    def getCurrentImage(self):
        return self.currentImage
        



"""
Sensor class that holds information about targets
"""
class Sensor():
    """Contains a camera, current target, and sensitivity
        @param colourThreshold = sensitivity
    """
    def __init__ (self, colourThreshold):
        self.cam = Camera()
        self.target = None
        self.setSensitivity(colourThreshold)

    """
        sets the sensitivity for threat detection
         higher value = less sensive
         valuable range = 0-255
    """
    def setSensitivity(self, threshold):
        self.sensitivity = threshold
        if self.sensitivity > 255:
            self.sensitivity = 255
        if self.sensitivity < 0:
            self.sensitivity = 0
        return self.sensitivity

    """
        finds the first available target detected by the camera
    """
    def findTarget(self):
        #self.cam.getNextImage()
        locations = self.cam.getTargetLocations(self.sensitivity)
        if len(locations) > 0:
            self.target = locations[randint(0, len(locations)-1)]#locations[0]
        return locations

    """
        draws a red blip to show where the current target is in the image
    """
    def blitTarget(self, window):
        if self.target != None:
            self.cam.blitLocations([self.target])

    """
        draws all possible targets on the screen
    """
    def blitTargets(self, window):
        self.cam.blitLocations(self.cam.getTargetLocations(self.sensitivity))

    """
        returns the camera of the Sensor
    """
    def getCamera(self):
        return self.cam

    """
        updates the camera image slots(steps the recording forward
    """
    def updateCameraImages(self):
        self.cam.getNextImage()


    """
        returns the current target
    """
    def getTarget(self):
        return self.target
    """
        draws the current camera view on screen
    """
    def drawOnScreen(self, window):
        image = self.cam.getCurrentImage()
        if(image != None):
            window.blit(image, (0,0))

    """
        draws the Sensor's "vision"- a monochrome image
        with whiter = biggest change between frames
    """
    def drawVisionOnScreen(self, window):
        window.blit(self.cam.getComparisonImage(), (0,0))
        
        

sensor = Sensor(30)
cam = Camera()

while True:
    #cam.getNextImage()
    sensor.updateCameraImages()

    #DRAW VISION
    sensor.drawOnScreen(window) #Draw the video feed
    #sensor.drawVisionOnScreen(window) #Draw a monochrome image of what the sensor can see

    sensor.findTarget()

    #DRAW TARGETS
    sensor.blitTarget(window) #Draw the most likely target in red
    #sensor.blitTargets(window) #Draw all detected targets in red


    #window.blit(cam.getCurrentImage(), (0,0))
    #cam.blitLocations(cam.getTargetLocations(200))
    pygame.display.update()
    pygame.event.get()
    
        
