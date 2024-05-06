import base64
import pickle
import time

import cv2 as cv
import face_recognition
import imutils
import joblib
import numpy as np
import streamlit as st

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #efffc9;
    }
</style>
""", unsafe_allow_html=True)
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local(r"images\nhandangface.jpg")  

st.write(f"<span style='color:white; font-size:50px;'>Nhận dạng khuôn mặt</span>", unsafe_allow_html=True)

FRAME_WINDOW = st.image([])
cap = cv.VideoCapture(0)

if 'stop' not in st.session_state:
    st.session_state.stop = False
    stop = False

press = st.button('Stop')
if press:
    if st.session_state.stop == False:
        st.session_state.stop = True
        cap.release()
    else:
        st.session_state.stop = False


if 'frame_stop' not in st.session_state:
    frame_stop = cv.imread(r"pages\model\stop.jpg")
    st.session_state.frame_stop = frame_stop

if st.session_state.stop == True:
    FRAME_WINDOW.image(st.session_state.frame_stop, channels='BGR')


# svc = joblib.load('encodings.pickle')
with open(r"pages\model\encodings.pickle", 'rb') as f:
    svc = pickle.load(f)
# svc = joblib.load('svc.pkl')



def visualize(input, faces, fps, thickness=2):
    if faces[1] is not None:
        for idx, face in enumerate(faces[1]):
            # print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))

            coords = face[:-1].astype(np.int32)
            cv.rectangle(input, (coords[0], coords[1]), (coords[0] +
                         coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
            cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
            cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
            cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
            cv.circle(input, (coords[10], coords[11]),
                      2, (255, 0, 255), thickness)
            cv.circle(input, (coords[12], coords[13]),
                      2, (0, 255, 255), thickness)
    cv.putText(input, 'FPS: {:.2f}'.format(fps), (1, 16),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


if __name__ == '__main__':
    detector = cv.FaceDetectorYN.create(
       r"pages\model\face_detection_yunet_2023mar.onnx",
        "",
        (320, 320),
        0.9,
        0.3,
        5000)

    recognizer = cv.FaceRecognizerSF.create(
        r"pages\model\face_recognition_sface_2021dec.onnx", "")

    tm = cv.TickMeter()

    frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    detector.setInputSize([frameWidth, frameHeight])

    dem = 0
    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            print('No frames grabbed!')
            break

        # Inference
        tm.start()
        faces = detector.detect(frame) # faces is a tuple
        tm.stop()

        if faces[1] is not None:
            face_align = recognizer.alignCrop(frame, faces[1][0])
            face_feature = recognizer.feature(face_align)
            # test_predict = svc.predict(face_feature)
            
            
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            rgb = imutils.resize(rgb, width=750)
            r = frame.shape[1] / float(rgb.shape[1])
            boxes = face_recognition.face_locations(rgb, model=r'pages\model\encodings.pickle')
            encodings = face_recognition.face_encodings(rgb, boxes)
            names=[]
            for encoding in encodings:
                matches = face_recognition.compare_faces(
                    svc["encodings"], encoding)
                name = "Unknown"    # tạm thời vậy, sau này khớp thì đổi tên

                # Kiểm tra xem từng encoding có khớp với known encodings nào không,
                if True in matches:
                    # lưu các chỉ số mà encoding khớp với known encodings (nghĩa là b == True)
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]

                    # tạo dictionary để đếm tổng số lần mỗi face khớp
                    counts = {}
                    # duyệt qua các chỉ số được khớp và đếm số lượng
                    for i in matchedIdxs:
                        # tên tương ứng known encoding khiowps với encoding check
                        name = svc["names"][i]
                        # nếu chưa có trong dict thì + 1, có rồi thì lấy số cũ + 1
                        counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                names.append(name)
            
            # test_predict = names[0]
            # result = mydict[test_predict[0]]
            result=""
            # sort names giam dan theo so lan xuat hien
            
            if len(names) > 0:
                names.sort(key=names.count, reverse=True)
                result = names[0]
            cv.putText(frame,result,(1,50),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw results on the input image
        visualize(frame, faces, tm.getFPS())

        # Visualize results
        FRAME_WINDOW.image(frame, channels='BGR')
    cv.destroyAllWindows()
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     tm.start()
    #     faces=detector.detect(frame)
    #     tm.stop()
        
    #     rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #     rgb = imutils.resize(rgb, width=750)
    #     r = frame.shape[1] / float(rgb.shape[1])
    #     boxes = face_recognition.face_locations(rgb, model='encodings.pickle')
    #     encodings = face_recognition.face_encodings(rgb, boxes)

   
    #     names = []

    #     for encoding in encodings:
            
    #         matches = face_recognition.compare_faces(
    #             svc["encodings"], encoding)
    #         name = "Unknown"    # tạm thời vậy, sau này khớp thì đổi tên

    #         # Kiểm tra xem từng encoding có khớp với known encodings nào không,
    #         if True in matches:
    #             # lưu các chỉ số mà encoding khớp với known encodings (nghĩa là b == True)
    #             matchedIdxs = [i for (i, b) in enumerate(matches) if b]

    #             # tạo dictionary để đếm tổng số lần mỗi face khớp
    #             counts = {}
    #             # duyệt qua các chỉ số được khớp và đếm số lượng
    #             for i in matchedIdxs:
    #                 # tên tương ứng known encoding khiowps với encoding check
    #                 name = svc["names"][i]
    #                 # nếu chưa có trong dict thì + 1, có rồi thì lấy số cũ + 1
    #                 counts[name] = counts.get(name, 0) + 1
    #             name = max(counts, key=counts.get)
    #         names.append(name)
    #     for ((top, right, bottom, left), name) in zip(boxes, names):
    #         top = int(top * r)
    #         right = int(right * r)
    #         bottom = int(bottom * r)
    #         left = int(left * r)
    #         cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    #         y = top - 15 if top - 15 > 15 else top + 15

    #         cv.putText(frame, name, (left, y),
    #                     cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
    
    # cv.destroyAllWindows()