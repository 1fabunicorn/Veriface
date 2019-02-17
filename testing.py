from src import recognizer

test = recognizer.Recognizer(debug=True)
test.createProfile("Barack Obama", "/home/phillipsw1/Downloads/test")
test.uploadVideo("/home/phillipsw1/Downloads/test/cut.mp4")
test.verify()