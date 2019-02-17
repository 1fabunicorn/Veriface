from src import recognizer
import sys

if len(sys.argv) > 1:
    test = recognizer.Recognizer(debug=True)
    test.createProfile("Barack Obama", "/home/phillipsw1/Downloads/test")
    test.uploadVideo("/home/phillipsw1/Downloads/test/" + sys.argv[1])
    test.verify(showPreview=True)