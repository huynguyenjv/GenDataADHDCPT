import random
import pandas as pd
import os

def generate_adhd_data(num_records=1000):
    """
    Sinh dữ liệu giả lập cho nhóm 'có ADHD' dựa trên DSM-5.
    Tăng xác suất cho các đáp án nặng ('Thường xuyên').
    """
    names = [
        "Nguyễn Văn A", "Trần Thị B", "Lê Minh C", "Phạm Thị D", "Ngô Quang E", 
        "Đỗ Thị F", "Bùi Quang G", "Hoàng Thị H", "Vũ Thị I", "Mai Anh K",
        "Phạm Văn M", "Lý Thị N", "Đào Quang P", "Trần Thị Q", "Nguyễn Anh R",
        "Đinh Thị S", "Trần Văn T", "Nguyễn Hoàng U", "Phạm Thị V", "Lê Minh W"
    ]
    age_range = list(range(16, 26))
    
    possible_responses = ["Không bao giờ", "Hiếm khi", "Thỉnh thoảng", "Thường xuyên"]
    weights_for_adhd = [0.05, 0.15, 0.30, 0.50]  # Nghiêng về 'Thường xuyên'
    
    questions = [
        "1. Bạn thường không chú ý kỹ ...",
        "2. Thường gặp khó khăn trong việc duy trì ...",
        "3. Thường có vẻ không lắng nghe khi ...",
        "4. Thường không làm theo hướng dẫn ...",
        "5. Thường gặp khó khăn trong việc tổ chức ...",
        "6. Thường tránh né, không thích hoặc miễn cưỡng ...",
        "7. Thường làm mất những đồ dùng cần thiết ...",
        "8. Thường dễ bị phân tâm bởi ...",
        "9. Thường hay quên trong các hoạt động hàng ngày ...",
        "10. Thường xuyên ngọ nguậy hoặc gõ tay ...",
        "11. Thường rời khỏi chỗ ngồi trong những tình huống ...",
        "12. Thường chạy nhảy hoặc leo trèo trong ...",
        "13. Thường không thể chơi hoặc tham gia các hoạt động ...",
        "14. Thường “luôn di chuyển” như thể “được điều khiển bằng động cơ” ...",
        "15. Thường nói quá nhiều.",
        "16. Thường buột miệng trả lời trước ...",
        "17. Thường gặp khó khăn khi phải chờ ...",
        "18. Thường xuyên ngắt lời hoặc xen vào việc của người khác ..."
    ]
    
    data = []
    for _ in range(num_records):
        name = random.choice(names)
        age = random.choice(age_range)
        
        responses_data = {}
        for question in questions:
            chosen_resp = random.choices(possible_responses, weights=weights_for_adhd, k=1)[0]
            responses_data[question] = chosen_resp
        
        responses_data["Họ và tên"] = name
        responses_data["Độ tuổi"] = age
        
        data.append(responses_data)
    
    df = pd.DataFrame(data)
    return df

def generate_nonadhd_data(num_records=1000):
    """
    Sinh dữ liệu giả lập cho nhóm 'Non-ADHD' dựa trên DSM-5.
    Giảm xác suất 'Thường xuyên', tăng 'Không bao giờ' / 'Hiếm khi'.
    """
    names = [
        "Nguyễn Văn A", "Trần Thị B", "Lê Minh C", "Phạm Thị D", "Ngô Quang E", 
        "Đỗ Thị F", "Bùi Quang G", "Hoàng Thị H", "Vũ Thị I", "Mai Anh K",
        "Phạm Văn M", "Lý Thị N", "Đào Quang P", "Trần Thị Q", "Nguyễn Anh R",
        "Đinh Thị S", "Trần Văn T", "Nguyễn Hoàng U", "Phạm Thị V", "Lê Minh W"
    ]
    age_range = list(range(16, 26))
    
    possible_responses = ["Không bao giờ", "Hiếm khi", "Thỉnh thoảng", "Thường xuyên"]
    # Ví dụ: nhóm Non-ADHD có nhiều 'Không bao giờ' / 'Hiếm khi'
    weights_for_nonadhd = [0.40, 0.30, 0.20, 0.10]
    
    questions = [
        "1. Bạn thường không chú ý kỹ ...",
        "2. Thường gặp khó khăn trong việc duy trì ...",
        "3. Thường có vẻ không lắng nghe khi ...",
        "4. Thường không làm theo hướng dẫn ...",
        "5. Thường gặp khó khăn trong việc tổ chức ...",
        "6. Thường tránh né, không thích hoặc miễn cưỡng ...",
        "7. Thường làm mất những đồ dùng cần thiết ...",
        "8. Thường dễ bị phân tâm bởi ...",
        "9. Thường hay quên trong các hoạt động hàng ngày ...",
        "10. Thường xuyên ngọ nguậy hoặc gõ tay ...",
        "11. Thường rời khỏi chỗ ngồi trong những tình huống ...",
        "12. Thường chạy nhảy hoặc leo trèo trong ...",
        "13. Thường không thể chơi hoặc tham gia các hoạt động ...",
        "14. Thường “luôn di chuyển” như thể “được điều khiển bằng động cơ” ...",
        "15. Thường nói quá nhiều.",
        "16. Thường buột miệng trả lời trước ...",
        "17. Thường gặp khó khăn khi phải chờ ...",
        "18. Thường xuyên ngắt lời hoặc xen vào việc của người khác ..."
    ]
    
    data = []
    for _ in range(num_records):
        name = random.choice(names)
        age = random.choice(age_range)
        
        responses_data = {}
        for question in questions:
            chosen_resp = random.choices(possible_responses, weights=weights_for_nonadhd, k=1)[0]
            responses_data[question] = chosen_resp
        
        responses_data["Họ và tên"] = name
        responses_data["Độ tuổi"] = age
        
        data.append(responses_data)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Số người trong mỗi nhóm
    num_adhd = 1000
    num_nonadhd = 1000
    
    # Sinh dữ liệu
    adhd_df = generate_adhd_data(num_records=num_adhd)
    nonadhd_df = generate_nonadhd_data(num_records=num_nonadhd)
    
    # Tạo thư mục chính
    main_dir = "pre-data-individual"
    os.makedirs(main_dir, exist_ok=True)
    
    # Tạo 2 thư mục con: ADHD, NonADHD
    adhd_dir = os.path.join(main_dir, "ADHD")
    nonadhd_dir = os.path.join(main_dir, "NonADHD")
    os.makedirs(adhd_dir, exist_ok=True)
    os.makedirs(nonadhd_dir, exist_ok=True)
    
    # Lưu từng người trong nhóm ADHD
    for idx, row in adhd_df.iterrows():
        person_df = pd.DataFrame([row])  # 1 dòng
        person_file = os.path.join(adhd_dir, f"ADHD_person_{idx+1}.csv")
        person_df.to_csv(person_file, index=False, encoding='utf-8-sig')
    
    # Lưu từng người trong nhóm Non-ADHD
    for idx, row in nonadhd_df.iterrows():
        person_df = pd.DataFrame([row])  # 1 dòng
        person_file = os.path.join(nonadhd_dir, f"NonADHD_person_{idx+1}.csv")
        person_df.to_csv(person_file, index=False, encoding='utf-8-sig')
    
    print(f"Đã sinh {num_adhd} file CSV cho ADHD trong: {adhd_dir}")
    print(f"Đã sinh {num_nonadhd} file CSV cho Non-ADHD trong: {nonadhd_dir}")
