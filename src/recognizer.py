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
           bool: True if folder successful
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
                self.profile_paths.append(self.profile_folder_path+"/"+path)
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
           bool: True if successful
        """

        if not os.path.isfile(file_path):
            self.debugPrint("ERROR: Video not found!")
            return False

        self.video_path = file_path
        self.debugPrint("INFO: Reading video...")
        video = cv2.VideoCapture(self.video_path)

        self.debugPrint("INFO: Processing frames...")
        self.video_frames = []
        ret = True

        while ret:
            ret, frame = video.read()
            self.video_frames.append(frame)

        self.debugPrint("INFO: Video at '" + file_path + "' was uploaded successfully!")
        return True

    def verify(self, showPreview=False):
        """
        Compares the detected faces of each frame with list of uploaded encoders.

        Parameters:
           showPreview (bool): If true, will pop-up a window showing the face analyses.
        Returns:
           results (dictionary):
                percent (double): The average percentage of encoders that match
                    the face with the greatest percentage in each frame
                frame_percentages (list): The percentage of encoders that matched per frame.
                frames_verified (int): The number of frames that detected a face
                frames_total (int): Total number of frames in video
        """

        #Initialize variables to return and initial buffers
        frame_sums = []
        percent = 0
        frames_verified = 0
        frames_total = len(self.video_frames)
        frames_percentages = 0

        face_locations = []
        face_encodings = []

        # Loops through each frame in the video
        for frame in self.video_frames:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

            # Matches temporarily stores the sums of each fade match with an encoder
            matches = []

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches.append(sum(fr.compare_faces(self.profile_encoders, face_encoding)))

            if not matches:
                frame_sums.append(-1)
            else:
                frame_sums.append(max(matches))

            self.debugPrint("Frame " + len(frame_sums) + "matches with sum of: " + frame_sums[-1])

        # This will contain only the frames that contained a face (not -1 sums)
        validated_percents = []
        for sum in frame_sums:
            if sum != -1:
                validated_percents.append(sum / len(self.profile_encoders))

        # Set frames verified to length of validated sums
        frames_percentages = len(validated_percents)

        # obtain average percentage of face validation
        percent = sum(frames_percentages) / len(frames_percentages)

        self.debugPrint("INFO: Video processing complete with verification of: " + str(percent * 100) + "%")

        results = {
            "percent": percent,
            "frames_verified": frames_verified,
            "frames_total":  frames_total,
            "frames_percentages": validated_percents
        }