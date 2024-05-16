import base64

import streamlit as st

st.set_page_config(
    page_title="Final Project",
    page_icon="👋",
)

st.write("<h1 style='font-size: 50px;color:purple'>Welcome to the website of our team!</h1>",
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


add_bg_from_local('images/Home.jpg')
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
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.balloons()
st.balloons()
st.balloons()

st.markdown(
    """
        <div class="red-text">
        Wishing everyone an enjoyable time!
        This is the website created by our group during the Digital Image Processing course guided by Mr. Trần Tiến Đức.
        You and your friends can select items from the left sidebar to view the content on digital image processing.
        </div>
        <p><b style="font-size: 40px;">Group Members:</b></p>
        <div>
        <h3>Student 1:</h3>
        <h4>- Full name: Lê Đình Trí</h4>
        <h4>- Student code: 22110442</h4>
        <h4>- School name: HCMC University of Technology and Education</h4>
        </div>
        <div>
        <h3>Student 2:</h3>
        <h4>- Full name: Vũ Bảo Long</h4>
        <h4>- Student code: 22110368</h4>
        <h4>- School name: HCMC University of Technology and Education</h4>
        </div>
        <p><b style="font-size: 40px;">Contact:</b></p>
        <div>
        <p><b style="font-size: 20px;">Student 1:</b></p>
        <p>- Github: <a style="color:green" href="https://github.com/tuoitho/">https://github.com/tuoitho/</a></p>
        <p>- Facebook:<a style="color:green" href="https://web.facebook.com/tuoithodakhoc/"> https://web.facebook.com/tuoithodakhoc/</a></p>
        <p>- Email: <a style="color:green" href="tuoithokhoc1414@gmail.com"> tuoithokhoc1414@gmail.com</a></p>
        <p>- Phone: <a style="color:green" href="">0362092749</a></p>
        </div>
        <div>
        <p><b style="font-size: 20px;">Student 2:</b></p>
        <p>- Github: <a style="color:green" href="https://github.com/vubaolongkg/">https://github.com/vubaolongkg/</a></p>
        <p>- Facebook:<a style="color:green" href="https://www.facebook.com/profile.php?id=100010121539430/"> https://www.facebook.com/profile.php?id=100010121539430/</a></p>
        <p>- Email: <a style="color:green" href="vubaolong1484@gmail.com"> vubaolong1484@gmail.com</a></p>
        <p>- Phone: <a style="color:green" href="">0986585203</a></p>
        </div>
        <div>
        <h1>Teacher: Tran Tien Duc</h1>
        <p>- Email:<a style="color:green" href="ductt@hcmute.edu.vn"> ductt@hcmute.edu.vn</a></p>
        <p>- Phone:<a style="color:green" href="ductt@hcmute.edu.vn"> 0919622862</a></p>
        <p>- Github: <a style="color:green" href="https://github.com/TranTienDuc">https://github.com/TranTienDuc</a><p>
	</div>
    """,
    unsafe_allow_html=True
)
