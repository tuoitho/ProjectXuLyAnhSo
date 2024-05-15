import base64
import numpy as np 
import cv2 
import streamlit as st

# Tạo tiêu đề cho ứng dụng
st.title("Tìm toạ độ đường viền")
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


add_bg_from_local(r"images\bg_duongvien.jpg")
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #aaa7ff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .red-text {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Nút tải lên file
uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Đọc ảnh từ file tải lên
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img2 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    # Chuyển đổi ảnh sang ảnh nhị phân
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
    
    # Phát hiện các đường viền trong ảnh
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Vẽ và hiển thị các đường viền
    font = cv2.FONT_HERSHEY_COMPLEX
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)
        
        n = approx.ravel()
        i = 0
        for j in n:
            if i % 2 == 0:
                x = n[i]
                y = n[i + 1]
                string = str(x) + " " + str(y)
                if i == 0:
                    cv2.putText(img2, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))
                else:
                    cv2.putText(img2, string, (x, y), font, 0.5, (0, 255, 0))
            i = i + 1

    # Hiển thị ảnh gốc với các đường viền
    st.subheader("Image with Contours")
    st.image(img2, channels="BGR")
