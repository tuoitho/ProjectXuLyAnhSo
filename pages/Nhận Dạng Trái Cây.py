import streamlit as st
import numpy as np
from PIL import Image
import cv2
import base64
st.balloons()
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        .title-text {{
            font-size: 24px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #efffc9;
    }
</style>
""", unsafe_allow_html=True)

# Add background image
add_bg_from_local(r'images\NhanDangTraiCay.jpg')  

st.markdown("<h1 class='title-text'>Nhận dạng trái cây</h1>", unsafe_allow_html=True)

try:
    if st.session_state["LoadModel"] == True:
        print('Đã load model rồi')
except:
    st.session_state["LoadModel"] = True
    st.session_state["Net"] = cv2.dnn.readNet(r"pages\modeltraicay\trai_cay.onnx")
    print(st.session_state["LoadModel"])
    print('Load model lần đầu') 

# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.45

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1

# Colors.
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)

def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    cv2.rectangle(im, (x, y), (x + dim[0], y + dim[1] + baseline), BLACK, cv2.FILLED)
    cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)

def pre_process(input_image, net):
    blob = cv2.dnn.blobFromImage(input_image, 1/255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs

def post_process(input_image, outputs):
    class_ids = []
    confidences = []
    boxes = []
    rows = outputs[0].shape[1]
    image_height, image_width = input_image.shape[:2]
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    for r in range(rows):
        row = outputs[0][0][r]
        confidence = row[4]
        if confidence >= CONFIDENCE_THRESHOLD:
            classes_scores = row[5:]
            class_id = np.argmax(classes_scores)
            if classes_scores[class_id] > SCORE_THRESHOLD:
                confidences.append(confidence)
                class_ids.append(class_id)
                cx, cy, w, h = row[0], row[1], row[2], row[3]
                left = int((cx - w/2) * x_factor)
                top = int((cy - h/2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        cv2.rectangle(input_image, (left, top), (left + width, top + height), BLUE, 3*THICKNESS)
        label = "{}:{:.2f}".format(classes[class_ids[i]], confidences[i])
        draw_label(input_image, label, left, top)
    return input_image

img_file_buffer = st.file_uploader("Upload an image", type=["bmp", "png", "jpg", "jpeg"])
col1,colmid,col2 = st.columns(3)
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    frame = np.array(image)
    frame = frame[:, :, [2, 1, 0]]  # RGB -> BGR for OpenCV
    with  col1:
        st.image(image, caption='Uploaded Image', use_column_width=True)  # Display the uploaded image larger
    if st.button('Predict'):
        with colmid:
            st.image(r"images\muitendo.png", channels="BGR")
        classes = ['Buoi', 'Cam', 'Coc', 'Khe', 'Mit']
        detections = pre_process(frame, st.session_state["Net"])
        img = post_process(frame.copy(), detections)
        t, _ = st.session_state["Net"].getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        # print(label)
        cv2.putText(img, label, (20, 40), FONT_FACE, FONT_SCALE, (0, 0, 255), THICKNESS, cv2.LINE_AA)
        with col2:
            st.image(img, caption='Detected Image', use_column_width=True)  # Display the result image larger

