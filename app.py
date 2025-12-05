import streamlit as st
from google.cloud import vision
import io

st.set_page_config(page_title="Image Recognition with Google Vision API", page_icon="📷")

st.title("📷 Google Vision API 이미지 인식 앱")
st.write("이미지를 업로드하면 Google Cloud Vision API가 무엇인지 분석해줍니다.")

# 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# Vision API 클라이언트 생성 함수
def get_vision_client():
    try:
        client = vision.ImageAnnotatorClient()
        return client
    except Exception as e:
        st.error(f"Vision API 초기화 오류: {e}")
        return None

# 분석 함수
def detect_labels(image_bytes):
    client = get_vision_client()
    if client is None:
        return None

    image = vision.Image(content=image_bytes)
    response = client.label_detection(image=image)

    if response.error.message:
        st.error(f"API 오류 발생: {response.error.message}")
        return None

    return response.label_annotations

# 이미지 업로드 후 처리
if uploaded_file:
    st.image(uploaded_file, caption="업로드한 이미지", use_column_width=True)

    if st.button("이미지 분석하기"):
        bytes_data = uploaded_file.read()
        labels = detect_labels(bytes_data)

        if labels:
            st.subheader("🔍 인식된 항목들:")
            for label in labels:
                st.write(f"- **{label.description}** (정확도: {label.score:.2f})")

st.write("\n---\n🔑 **주의:** 이 앱이 정상 작동하려면 Streamlit Cloud 또는 서버 환경에 `GOOGLE_APPLICATION_CREDENTIALS` 환경 변수를 설정해야 합니다.")
