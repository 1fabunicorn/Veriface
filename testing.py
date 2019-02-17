from src import recognizer
import sys

name = "Test Demo"

if len(sys.argv) > 1:
    test = recognizer.Recognizer(debug=True)
    test.createProfile("Barack Obama", "/home/[user]/Downloads/test")
    test.uploadVideo("/home/[user]/Downloads/test/" + sys.argv[1])
    if len(sys.argv) > 2:
        name = sys.argv[2]

    test.verify(showPreview=True, title=name)
