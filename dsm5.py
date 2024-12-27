import random
import pandas as pd

def generate_adhd_data(num_records=1000):
    """
    Sinh dữ liệu giả lập cho nhóm 'có ADHD' dựa trên DSM-5.
    Tăng xác suất cho các đáp án nặng (ví dụ: "Thường xuyên").
    """

    # Danh sách tên tiếng Việt (có thể thêm/bớt tuỳ ý)
    names = [
        "Nguyễn Văn A", "Trần Thị B", "Lê Minh C", "Phạm Thị D", "Ngô Quang E", 
        "Đỗ Thị F", "Bùi Quang G", "Hoàng Thị H", "Vũ Thị I", "Mai Anh K",
        "Phạm Văn M", "Lý Thị N", "Đào Quang P", "Trần Thị Q", "Nguyễn Anh R",
        "Đinh Thị S", "Trần Văn T", "Nguyễn Hoàng U", "Phạm Thị V", "Lê Minh W"
    ]
    
    # Nhóm tuổi (giả lập) từ 16 đến 25
    age_range = list(range(16, 26))
    
    # Các loại đáp án, giả sử với nhóm ADHD ta sẽ:
    # - Tăng xác suất "Thường xuyên" và "Thỉnh thoảng"
    # - Giảm "Hiếm khi" và "Không bao giờ"
    possible_responses = ["Không bao giờ", "Hiếm khi", "Thỉnh thoảng", "Thường xuyên"]
    weights_for_adhd = [0.05, 0.15, 0.30, 0.50]  # Ví dụ phân bố xác suất
    
    # Danh sách 18 câu hỏi DSM-5 (một số câu bạn đã liệt kê)
    # Lưu ý tách riêng câu 9 và 10 vì chuỗi gốc của bạn dường như bị dính liền
    questions = [
        "1.	Bạn thường không chú ý kỹ đến các chi tiết hoặc mắc lỗi bất cẩn trong việc học tập, làm việc hoặc trong các hoạt động khác (ví dụ: bỏ sót hoặc bỏ qua các chi tiết, công việc không chính xác).",
        "2. Thường gặp khó khăn trong việc duy trì sự chú ý trong các nhiệm vụ hoặc hoạt động vui chơi (ví dụ: gặp khó khăn trong việc tập trung trong khi nghe giảng, trò chuyện hoặc đọc sách dài).",
        "3.	Thường có vẻ không lắng nghe khi được nói chuyện trực tiếp (ví dụ, tâm trí dường như ở nơi khác, ngay cả khi không có bất kỳ sự xao lãng rõ ràng nào).",
        "4.	Thường không làm theo hướng dẫn và không hoàn thành bài tập ở trường, công việc nhà hoặc nhiệm vụ ở nơi làm việc (ví dụ: bắt đầu làm việc nhưng nhanh chóng mất tập trung và dễ bị phân tâm).",
        "5.	Thường gặp khó khăn trong việc tổ chức các nhiệm vụ và hoạt động (ví dụ: khó khăn trong việc quản lý các nhiệm vụ theo trình tự; khó khăn trong việc sắp xếp vật liệu và đồ đạc theo thứ tự; công việc lộn xộn, thiếu tổ chức; quản lý thời gian kém; không đáp ứng được thời hạn).",
        "6.	Thường tránh né, không thích hoặc miễn cưỡng tham gia vào các nhiệm vụ đòi hỏi nỗ lực tinh thần liên tục (ví dụ: bài tập ở trường hoặc bài tập về nhà; đối với thanh thiếu niên lớn hơn và người lớn, là chuẩn bị báo cáo, hoàn thành biểu mẫu, xem xét các bài viết dài).",
        "7.	Thường làm mất những đồ dùng cần thiết cho công việc hoặc hoạt động (ví dụ: đồ dùng học tập, bút chì, sách, dụng cụ, ví, chìa khóa, giấy tờ, kính mắt, điện thoại di động).",
        "8.	Thường dễ bị phân tâm bởi các kích thích bên ngoài (đối với thanh thiếu niên lớn tuổi và người lớn, có thể bao gồm những suy nghĩ không liên quan).",
        "9.	Thường hay quên trong các hoạt động hàng ngày (ví dụ như làm việc nhà, chạy việc vặt; đối với thanh thiếu niên lớn tuổi và người lớn, là quên gọi điện thoại, thanh toán hóa đơn, giữ đúng lịch hẹn)."
        "10.	Thường xuyên ngọ nguậy hoặc gõ tay, gõ chân hoặc ngọ nguậy trên ghế.",
        "11.	Thường rời khỏi chỗ ngồi trong những tình huống mà người ta yêu cầu phải ngồi yên (ví dụ: rời khỏi chỗ trong lớp học, trong văn phòng hoặc nơi làm việc khác hoặc trong những tình huống khác đòi hỏi phải ngồi yên).",
        "12.	Thường chạy nhảy hoặc leo trèo trong những tình huống không phù hợp. (Lưu ý: Ở thanh thiếu niên hoặc người lớn, có thể chỉ giới hạn ở cảm giác bồn chồn).",
        "13.	Thường không thể chơi hoặc tham gia các hoạt động giải trí một cách yên tĩnh.",
        "14.	Thường “luôn di chuyển” như thể “được điều khiển bằng động cơ” (ví dụ: không thể hoặc không thoải mái khi phải ngồi yên trong thời gian dài, như trong nhà hàng, cuộc họp; người khác có thể cảm thấy bồn chồn hoặc khó theo kịp).",
        "15.	Thường nói quá nhiều.",
        "16.	Thường buột miệng trả lời trước khi câu hỏi được hoàn tất (ví dụ: hoàn thành câu của người khác; không thể chờ đến lượt mình trong cuộc trò chuyện).",
        "17.	Thường gặp khó khăn khi phải chờ đến lượt mình (ví dụ như khi xếp hàng).",
        "18.	Thường xuyên ngắt lời hoặc xen vào việc của người khác (ví dụ: xen vào cuộc trò chuyện, trò chơi hoặc hoạt động; có thể bắt đầu sử dụng đồ của người khác mà không xin phép hoặc không được phép; đối với thanh thiếu niên và người lớn, có thể xen vào hoặc chiếm mất việc của người khác)."
    ]
    
    data = []
    for _ in range(num_records):
        name = random.choice(names)
        age = random.choice(age_range)
        
        # Sinh câu trả lời với xác suất "thường xuyên" cao
        responses_data = {}
        for question in questions:
            chosen_response = random.choices(
                possible_responses,
                weights=weights_for_adhd,  # Xác suất cho từng đáp án
                k=1
            )[0]
            responses_data[question] = chosen_response
        
        # Thêm thông tin cá nhân
        responses_data["Họ và tên"] = name
        responses_data["Độ tuổi"] = age
        
        data.append(responses_data)
    
    # Chuyển sang DataFrame
    df = pd.DataFrame(data)
    return df


# --------------------------
# Sử dụng hàm để sinh 1000 người
# --------------------------
if __name__ == "__main__":
    import os
    
    # Sinh dữ liệu ADHD
    adhd_df = generate_adhd_data(num_records=2000)
    
    # Tạo thư mục lưu file CSV nếu chưa có
    os.makedirs("pre-data", exist_ok=True)
    
    # Lưu vào file CSV
    output_path = "pre-data/adhd_sample_data.csv"
    adhd_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"Đã sinh dữ liệu ADHD (1.000 người) và lưu tại: {output_path}")
