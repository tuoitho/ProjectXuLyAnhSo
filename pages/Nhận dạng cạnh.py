import base64
import cv2
import numpy as np
import streamlit as st

# Tạo tiêu đề cho ứng dụng
st.title("Nhận dạng cạnh")
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


add_bg_from_local(r"images\NhanDangKhuonMat.jpg")
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #eac7ff;
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
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Tính toán Sobel
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    
    # Chuyển đổi Sobel kết quả sang uint8
    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    
    # Hiển thị ảnh gốc
    st.subheader("Original Image")
    st.image(img, channels="RGB")
    
    # Hiển thị ảnh Sobel X
    st.subheader("Sobel X")
    st.image(sobel_x, channels="GRAY")
    
    # Hiển thị ảnh Sobel Y
    st.subheader("Sobel Y")
    st.image(sobel_y, channels="GRAY")
