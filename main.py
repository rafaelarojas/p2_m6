import cv2

def detectFaces(input_video_path, output_video_path):
    video = cv2.VideoCapture(input_video_path)
    face_cascade_frontal = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_cascade_profile = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
    frames = []
    count = 0
    success = True

    while success:
        success, image = video.read()
        if not success:
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_frontal = face_cascade_frontal.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))
        faces_profile = face_cascade_profile.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

        valid_faces = []

        for (x, y, w, h) in faces_frontal:
            for (px, py, pw, ph) in faces_profile:
                if (x < px + pw and x + w > px and y < py + ph and y + h > py):
                    valid_faces.append((x, y, w, h))
                    break

        for (x, y, w, h) in valid_faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite("frame%d.jpg" % count, image)
            count += 1

        frames.append(image)

    video.release()

    if len(frames) > 0:
        height, width, layers = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()

if __name__ == "__main__":
    input_video_path = 'la_cabra.mp4'
    output_video_path = 'output.mp4'
    detectFaces(input_video_path, output_video_path)
