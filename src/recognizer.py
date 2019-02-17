import face_recognition as fr
import cv2
import numpy
import os.path
from os import listdir

class Recognizer:
    """
    This is a class for verifying videos for the authenticity
    of a face present in the video.

    Attributes:
        debug (bool): If set to True, will print debug messages to console.

    """

    profile_name = None
    profile_folder_path = None
    profile_paths = []
    profile_images = []
    profile_encoders = []

    video_path = None
    video_frames = []
    debug = False

    def __init__(self, debug=False):
        """
        Creates a recognizer object that can be used to verify
        if a person in a video matches their identity.

        Parameters:
           debug (bool): If set to True, will print debug messages to console.
        """

        self.debug = debug
        self.debugPrint("Security System Engaged!")

    def debugPrint(self, msg):
        """
        Calls print function if debug is set to True

        Parameters:
           msg (str): Text to print to console
        """

        if self.debug:
            print("[Recognizer] " + msg)

    def createProfile(self, name, image_dir):
        """
        This will set the template image of the face being verified.
        This code only works with one template at a time for simplicity.

        Parameters:
           name (str): Full name of person's face being verified.
           image_dir (str): Path for all reference images.
        Returns:
           bool: True if folder exists
        """

        # Checks if the provided image_dir is an existing folder
        if not os.path.isdir(image_dir):
            self.debugPrint("ERROR: Folder not found!")
            return False

        self.profile_folder_path = image_dir
        self.profile_name = name

        # Reset lists for holding images
        self.profile_paths = []
        self.profile_images = []
        self.profile_encoders = []

        self.debugPrint("INFO: Scanning '" + self.profile_folder_path + "' for images...")
        path_buffer = listdir(self.profile_folder_path)
        for path in path_buffer:
            if path.endswith(".jpg") or path.endswith(".png"):
                self.debugPrint("INFO: Uploading '" + path + "' as encoder...")
                self.profile_paths.append(self.profile_folder_path+path)
                self.profile_images.append(fr.load_image_file(self.profile_paths[-1]))
                self.profile_encoders.append(fr.face_encodings(self.profile_images[-1])[0])

        self.debugPrint("INFO: " + str(len(self.profile_encoders)) + " images were successfully uploaded.")
        return True

    def uploadVideo(self, file_path):
        """
        Get path for sample video.

        Parameters:
           file_path (str): File path of reference image.
        Returns:
           bool: True if file exists
        """

        if os.path.isfile(file_path):
            self.debugPrint("ERROR: File not found!")
            return False

        self.video_path = file_path
        self.debugPrint("INFO: Reading video...")
        video = cv2.VideoCapture(self.video_path)

        self.debugPrint("INFO: Processing frames...")
        self.video_frames = []
        while video.isOpened():
            ret, frame = video.read()
            self.video_frames.append(self, frame)

        self.debugPrint("INFO: Video at '" + file_path + "' was uploaded successfully!")
        return True

    def verify(self):
        """
        Get path for sample video.

        Parameters:
           name (str): Full name of person's face being verified.
           file_path (str): File path of reference image.
        Returns:
           results (list):
                frames_verified (int): The number of frames
        """
