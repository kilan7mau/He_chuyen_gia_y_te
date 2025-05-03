import streamlit as st
import pandas as pd
from experta import *
import os
import tempfile
import base64
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="Hệ Chuyên Gia Y Tế",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Basic page styling
st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Global variables
diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}


def create_temp_files():
    """Create temporary files with sample data if they don't exist"""

    # Create directory structure
    os.makedirs("Disease symptoms", exist_ok=True)
    os.makedirs("Disease descriptions", exist_ok=True)
    os.makedirs("Disease treatments", exist_ok=True)

    # Sample diseases
    sample_diseases = [
        "Jaundice", "Alzheimers", "Arthritis", "Tuberculosis",
        "Asthma", "Sinusitis", "Epilepsy", "Heart Disease",
        "Diabetes", "Glaucoma", "Hyperthyroidism", "Heat Stroke", "Hypothermia"
    ]

    # Write to diseases.txt
    with open("diseases.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sample_diseases))

    # Create symptom files
    symptoms = {
        "Jaundice": ["no", "no", "no", "no", "no", "no", "yes", "no", "no", "yes", "no", "yes", "no"],
        "Alzheimers": ["no", "no", "no", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "no"],
        "Arthritis": ["no", "yes", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "no", "no"],
        "Tuberculosis": ["no", "no", "yes", "yes", "no", "no", "no", "no", "no", "yes", "no", "no", "no"],
        "Asthma": ["no", "no", "yes", "yes", "no", "no", "no", "yes", "no", "no", "no", "no", "no"],
        "Sinusitis": ["yes", "no", "no", "yes", "no", "yes", "no", "no", "no", "yes", "no", "no", "no"],
        "Epilepsy": ["no", "no", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "no", "no"],
        "Heart Disease": ["no", "no", "yes", "no", "no", "no", "no", "no", "no", "no", "no", "yes", "no"],
        "Diabetes": ["no", "no", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "yes", "yes"],
        "Glaucoma": ["yes", "no", "no", "no", "no", "no", "no", "no", "no", "no", "no", "yes", "yes"],
        "Hyperthyroidism": ["no", "no", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "yes", "no"],
        "Heat Stroke": ["yes", "no", "no", "no", "no", "no", "no", "no", "no", "yes", "no", "yes", "no"],
        "Hypothermia": ["no", "no", "no", "no", "yes", "no", "no", "no", "yes", "no", "no", "no", "no"]
    }

    descriptions = {
        "Jaundice": "Vàng da là tình trạng da, màng nhầy hoặc mắt chuyển sang màu vàng do nồng độ bilirubin cao trong máu. Điều này có thể liên quan đến các vấn đề về gan, túi mật hoặc các tình trạng khác.",
        "Alzheimers": "Bệnh Alzheimer là một rối loạn thoái hóa thần kinh tiến triển gây ra suy giảm trí nhớ, suy nghĩ và hành vi. Các triệu chứng phát triển dần dần và trở nên tồi tệ hơn theo thời gian.",
        "Arthritis": "Viêm khớp là tình trạng viêm một hoặc nhiều khớp của bạn, gây ra đau và cứng khớp thường tăng lên theo tuổi tác.",
        "Tuberculosis": "Bệnh lao là một bệnh nhiễm trùng do vi khuẩn gây ra chủ yếu ảnh hưởng đến phổi. Vi khuẩn gây lao lây lan khi người bị nhiễm ho, hắt hơi hoặc nói chuyện.",
        "Asthma": "Hen suyễn là một tình trạng mà trong đó đường thở của bạn bị hẹp và sưng lên và có thể sản xuất dịch nhầy thêm. Điều này có thể gây khó thở, ho, thở khò khè và thở gấp.",
        "Sinusitis": "Viêm xoang là tình trạng viêm lớp lót xoang mũi. Đây là một tình trạng phổ biến mà hàng triệu người phải điều trị mỗi năm.",
        "Epilepsy": "Động kinh là một rối loạn thần kinh trung ương (rối loạn não) trong đó hoạt động của não trở nên bất thường, gây ra co giật hoặc các giai đoạn hành vi bất thường, cảm giác và đôi khi mất ý thức.",
        "Heart Disease": "Bệnh tim là một thuật ngữ chung cho nhiều loại bệnh tim. Bệnh tim bao gồm các bệnh về mạch máu, như bệnh động mạch vành; nhịp tim bất thường (loạn nhịp tim); các khiếm khuyết tim bẩm sinh; và nhiều loại khác.",
        "Diabetes": "Bệnh tiểu đường là một nhóm các bệnh ảnh hưởng đến cách cơ thể bạn sử dụng đường trong máu (glucose). Glucose là nguồn năng lượng quan trọng cho các tế bào tạo nên cơ bắp và mô của bạn. Đó cũng là nguồn nhiên liệu chính cho não của bạn.",
        "Glaucoma": "Glaucoma là một nhóm các bệnh về mắt có thể gây tổn thương dây thần kinh thị giác của bạn, là thần kinh gửi thông tin từ mắt bạn đến não của bạn. Tổn thương này thường do áp lực bên trong mắt quá cao.",
        "Hyperthyroidism": "Cường giáp xảy ra khi tuyến giáp của bạn sản xuất quá nhiều một số hormone tuyến giáp. Điều này có thể đẩy nhanh quá trình trao đổi chất của bạn đáng kể, gây ra giảm cân đột ngột, nhịp tim nhanh hoặc không đều, đổ mồ hôi và dễ cáu kỉnh.",
        "Heat Stroke": "Say nắng là tình trạng nguy hiểm nhất liên quan đến nhiệt. Nó xảy ra khi cơ thể bạn trở nên quá nóng và không thể kiểm soát nhiệt độ của mình: mồ hôi cơ chế làm mát tự nhiên thất bại và nhiệt độ cơ thể bạn tăng lên quá cao.",
        "Hypothermia": "Hạ thân nhiệt là một tình trạng y tế khẩn cấp xảy ra khi nhiệt độ cơ thể bạn giảm xuống dưới 35°C. Khi điều này xảy ra, hệ thần kinh, tim và các cơ quan khác của bạn không thể hoạt động bình thường."
    }

    treatments = {
        "Jaundice": "- Điều trị phụ thuộc vào nguyên nhân\n- Thuốc kháng sinh cho nhiễm trùng\n- Truyền máu hoặc phẫu thuật trong một số trường hợp\n- Uống nhiều nước, nghỉ ngơi\n- Liệu pháp ánh sáng có thể được sử dụng cho trẻ sơ sinh",
        "Alzheimers": "- Thuốc ức chế cholinesterase (Aricept, Exelon, Razadyne)\n- Memantine (Namenda)\n- Liệu pháp hành vi và nhận thức\n- Thay đổi lối sống: tập thể dục, chế độ ăn lành mạnh\n- Hỗ trợ cho người chăm sóc",
        "Arthritis": "- Thuốc giảm đau như paracetamol\n- Thuốc chống viêm không steroid (NSAIDs)\n- Steroid\n- Thuốc chống thấp khớp làm thay đổi bệnh (DMARDs)\n- Vật lý trị liệu và tập thể dục\n- Trong trường hợp nặng, có thể cần phẫu thuật thay khớp",
        "Tuberculosis": "- Kết hợp nhiều thuốc kháng sinh trong thời gian dài (6-9 tháng)\n- Thường bao gồm isoniazid, rifampin, ethambutol và pyrazinamide\n- Điều trị phải được hoàn thành đầy đủ để tránh kháng thuốc\n- Nghỉ ngơi và dinh dưỡng tốt\n- Cách ly trong giai đoạn đầu nếu lao phổi truyền nhiễm",
        "Asthma": "- Thuốc giãn phế quản tác dụng nhanh (thuốc cấp cứu)\n- Thuốc kiểm soát dài hạn như corticosteroid hít\n- Thuốc ức chế leukotriene\n- Thuốc đồng vận beta tác dụng dài\n- Tránh các yếu tố kích thích hen\n- Lập kế hoạch hành động hen suyễn",
        "Sinusitis": "- Thuốc giảm đau như paracetamol hoặc ibuprofen\n- Thuốc kháng sinh cho viêm xoang do vi khuẩn\n- Thuốc xịt mũi corticosteroid\n- Thuốc kháng histamine cho viêm xoang dị ứng\n- Rửa mũi bằng nước muối\n- Phẫu thuật trong trường hợp mãn tính nghiêm trọng",
        "Epilepsy": "- Thuốc chống động kinh (như carbamazepine, valproate, lamotrigine)\n- Chế độ ăn ketogenic (trong một số trường hợp)\n- Kích thích dây thần kinh phế vị\n- Phẫu thuật cho các trường hợp không đáp ứng với thuốc\n- Tránh các yếu tố kích thích co giật\n- Giáo dục về quản lý co giật",
        "Heart Disease": "- Thuốc như statin, thuốc chẹn beta, ACE inhibitors\n- Thay đổi lối sống: chế độ ăn lành mạnh, tập thể dục, bỏ hút thuốc\n- Thủ thuật như nong mạch vành, đặt stent\n- Phẫu thuật bắc cầu động mạch vành cho trường hợp nặng\n- Kiểm soát các bệnh đi kèm như tiểu đường, cao huyết áp\n- Phục hồi chức năng tim",
        "Diabetes": "- Insulin cho tiểu đường type 1\n- Thuốc uống hạ đường huyết cho tiểu đường type 2\n- Theo dõi đường huyết thường xuyên\n- Chế độ ăn kiểm soát đường, kiểm soát cân nặng\n- Tập thể dục đều đặn\n- Kiểm tra định kỳ mắt, thận và chân",
        "Glaucoma": "- Thuốc nhỏ mắt để giảm áp lực nội nhãn\n- Thuốc uống trong trường hợp nặng\n- Điều trị laser để cải thiện thoát dịch\n- Phẫu thuật (trabeculectomy, shunt) cho trường hợp nặng\n- Kiểm tra nhãn áp định kỳ\n- Theo dõi thị trường",
        "Hyperthyroidism": "- Thuốc kháng giáp (methimazole, propylthiouracil)\n- Thuốc chẹn beta để kiểm soát triệu chứng\n- Điều trị iốt phóng xạ\n- Phẫu thuật cắt tuyến giáp (toàn bộ hoặc một phần)\n- Chế độ ăn phù hợp\n- Theo dõi hormone tuyến giáp định kỳ",
        "Heat Stroke": "- Làm mát cơ thể nhanh chóng (chăn ướt, gói đá)\n- Truyền dịch tĩnh mạch\n- Theo dõi nhiệt độ cơ thể\n- Điều trị các biến chứng nếu có\n- Phòng ngừa: uống đủ nước, tránh nắng gắt\n- Thích nghi dần với nhiệt độ cao",
        "Hypothermia": "- Làm ấm cơ thể từ từ\n- Chăn nhiệt, dịch truyền ấm\n- Theo dõi nhịp tim (cẩn thận loạn nhịp)\n- Oxy bổ sung nếu cần\n- Điều trị các bệnh tiềm ẩn\n- Phòng ngừa: quần áo ấm, tránh tiếp xúc lâu với lạnh"
    }

    # Write to files
    for disease in sample_diseases:
        # Write symptoms
        with open(f"Disease symptoms/{disease}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(symptoms[disease]))

        # Write descriptions
        with open(f"Disease descriptions/{disease}.txt", "w", encoding="utf-8") as f:
            f.write(descriptions[disease])

        # Write treatments
        with open(f"Disease treatments/{disease}.txt", "w", encoding="utf-8") as f:
            f.write(treatments[disease])


def preprocess():
    global diseases_list, diseases_symptoms, symptom_map, d_desc_map, d_treatment_map

    # Check if files exist, if not create them
    if not os.path.exists("diseases.txt"):
        create_temp_files()

    diseases = open("diseases.txt", encoding="utf-8")
    diseases_t = diseases.read()
    diseases_list = diseases_t.split("\n")
    diseases.close()

    for disease in diseases_list:
        disease_s_file = open("Disease symptoms/" + disease + ".txt", encoding="utf-8")
        disease_s_data = disease_s_file.read()
        s_list = disease_s_data.split("\n")
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = disease
        disease_s_file.close()

        disease_s_file = open("Disease descriptions/" + disease + ".txt", encoding="utf-8")
        disease_s_data = disease_s_file.read()
        d_desc_map[disease] = disease_s_data
        disease_s_file.close()

        disease_s_file = open("Disease treatments/" + disease + ".txt", encoding="utf-8")
        disease_s_data = disease_s_file.read()
        d_treatment_map[disease] = disease_s_data
        disease_s_file.close()


def identify_disease():
    symptoms = [
        "headache", "back_pain", "chest_pain", "cough", "fainting",
        "sore_throat", "fatigue", "restlessness", "low_body_temp",
        "fever", "sunken_eyes", "nausea", "blurred_vision"
    ]

    vietnamese_symptoms = [
        "Đau đầu", "Đau lưng", "Đau ngực", "Ho", "Ngất xỉu",
        "Đau họng", "Mệt mỏi", "Mất ngủ, lo âu", "Thân nhiệt thấp",
        "Sốt", "Mắt hõm", "Buồn nôn", "Mắt mờ"
    ]

    # Get user symptoms
    st.header("🔍 Hãy cho biết các triệu chứng của bạn", divider="rainbow")

    user_symptoms = []
    symptom_values = {}

    col1, col2 = st.columns(2)

    with col1:
        for i in range(0, 7):
            symptom_values[symptoms[i]] = "yes" if st.checkbox(f"{vietnamese_symptoms[i]}") else "no"

    with col2:
        for i in range(7, 13):
            symptom_values[symptoms[i]] = "yes" if st.checkbox(f"{vietnamese_symptoms[i]}") else "no"

    if st.button("Chẩn đoán", use_container_width=True):
        # Process diagnosis
        user_symptoms_list = [
            symptom_values["headache"], symptom_values["back_pain"],
            symptom_values["chest_pain"], symptom_values["cough"],
            symptom_values["fainting"], symptom_values["sore_throat"],
            symptom_values["fatigue"], symptom_values["restlessness"],
            symptom_values["low_body_temp"], symptom_values["fever"],
            symptom_values["sunken_eyes"], symptom_values["nausea"],
            symptom_values["blurred_vision"]
        ]

        # Check for exact match
        disease_found = False
        for disease_symptoms, disease in zip(diseases_symptoms, diseases_list):
            if disease_symptoms == user_symptoms_list:
                display_result(disease)
                disease_found = True
                break

        # If no exact match, find the closest match
        if not disease_found:
            max_count = 0
            max_disease = ""

            for key, val in symptom_map.items():
                count = 0
                temp_list = eval(key)

                for j in range(0, len(user_symptoms_list)):
                    if temp_list[j] == user_symptoms_list[j] and user_symptoms_list[j] == "yes":
                        count += 1

                if count > max_count:
                    max_count = count
                    max_disease = val

            if max_disease:
                st.info("Không tìm thấy bệnh nào khớp chính xác với các triệu chứng của bạn. Đây là kết quả gần nhất:")
                display_result(max_disease)
            else:
                st.warning("Không tìm thấy đủ thông tin để chẩn đoán. Vui lòng chọn thêm triệu chứng.")


def display_result(disease):
    # Tạo container với màu nền và viền cho kết quả
    st.markdown("## 🏥 Kết quả chẩn đoán")

    # Sử dụng success box cho kết quả chẩn đoán
    st.success(f"### Căn bệnh có khả năng cao nhất mà bạn đang mắc phải là: {disease}")

    # Dùng expander cho mô tả
    with st.expander("📋 Mô tả chi tiết về bệnh", expanded=True):
        st.write(d_desc_map[disease])

    # Dùng info box cho phương pháp điều trị
    st.info("### Phương pháp điều trị đề xuất")

    # Hiển thị điều trị dưới dạng markdown
    treatments = d_treatment_map[disease].split('\n')
    for treatment in treatments:
        if treatment.strip():  # Chỉ hiển thị dòng không trống
            st.markdown(f"- {treatment.strip()}")

    # Thêm lưu ý
    st.caption(
        "*Lưu ý: Đây chỉ là đề xuất từ hệ thống. Vui lòng tham khảo ý kiến bác sĩ để có phương pháp điều trị chính xác.*")


def add_logo():
    # Create a simple medical logo using PIL
    width, height = 200, 200
    image = Image.new('RGB', (width, height), color=(240, 248, 255))

    # Convert the image to a byte array
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    # Encode the image as base64
    b64 = base64.b64encode(img_byte_array).decode()

    # Display the image in the sidebar
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{b64}" width="150" style="border-radius: 10px; margin-bottom: 20px;">
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    # Load disease data
    preprocess()

    # Add logo to sidebar
    add_logo()

    # Sidebar
    st.sidebar.title("🏥 Hệ Chuyên Gia Y Tế")
    st.sidebar.info(
        """
        Hệ thống này sử dụng các triệu chứng bạn cung cấp để xác định bệnh có thể mắc phải và đề xuất phương pháp điều trị.

        **Lưu ý**: Đây chỉ là công cụ hỗ trợ và không thay thế cho tư vấn y tế chuyên nghiệp.
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Thông tin bổ sung")
    expand_diseases = st.sidebar.expander("Danh sách bệnh trong hệ thống")
    with expand_diseases:
        for disease in diseases_list:
            st.write(f"• {disease}")

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 Hệ Chuyên Gia Y Tế")

    # Main content
    st.title("HỆ CHUYÊN GIA Y TẾ")

    st.write("""
    Chào mừng bạn đến với Hệ Chuyên Gia Y Tế! Hệ thống này sẽ giúp bạn xác định 
    căn bệnh tiềm ẩn dựa trên các triệu chứng của bạn và đề xuất các phương pháp điều trị phổ biến.

    **Hướng dẫn sử dụng:**
    1. Chọn tất cả các triệu chứng bạn đang gặp phải
    2. Nhấn nút "Chẩn đoán" để nhận kết quả
    3. Xem kết quả chẩn đoán và đề xuất điều trị
    """)

    st.markdown("---")

    # Call the identify_disease function
    identify_disease()


if __name__ == "__main__":
    main()