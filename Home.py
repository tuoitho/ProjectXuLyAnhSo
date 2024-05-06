import base64

import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("<h1 style='font-size: 50px;color:black'>Chào thầy và các bạn đã đến với website của nhóm chúng em !</h1>",
         unsafe_allow_html=True)
st.sidebar.success("You can choose one of my projects above.")


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


add_bg_from_local('Background/Home.jpg')
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

st.markdown(
    """
        <div class="red-text">
        Chúc mọi người có những phút giây thú vị!
    Đây là website mà nhóm đã làm trong quá trình học môn Xử lý ảnh số do thầy Trần Tiến Đức hướng dẫn.
    Thầy và các bạn có thể chọn các mục ở sidebar bên trái để xem nội dung về xử lý ảnh số.
    </div>
        <p><b style="font-size: 40px;">Thông tin nhóm thực hiện:</b></p>
        <div>
        <h3>Student 1:</h3>
    - Full name: Le Dinh Tri</p>
        - Student code: 22110442</p>
        - School name: HCMC University of Technology and Education
        </div>
        <div>
        <h3>Student 2:</h3>
    - Full name: Le Dinh Tri</p>
        - Student code: 22110442</p>
        - School name: HCMC University of Technology and Education
        </div>
    <p><b style="font-size: 40px;">Contact me:</b></p>
    <div>
        <p>- Github: <a style="color:green" href="https://github.com/tuoitho/">https://github.com/tuoitho/</a></p>
        <p>- Facebook:<a style="color:green" href=""> https://www.facebook.com/</a></p>
        <p>- Email: <a style="color:green" href=""> gmail.com</a></p>
        <p>- Phone: <a style="color:green" href=""> 0</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
