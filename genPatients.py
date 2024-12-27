import os
import random
import csv
import numpy as np

# ----------------------------------
# 1. CÁC THÔNG SỐ CƠ BẢN
# ----------------------------------

NUM_ADHD_SUBJECTS = 500      # Số người bị ADHD
NUM_NON_ADHD_SUBJECTS = 500  # Số người không bị ADHD

NUM_TRIALS = 1200           # Số trial cho mỗi người (bạn có thể tăng lên 1200 nếu muốn 20 phút)
TARGET_RATE = 0.3          # Xác suất xuất hiện Target (30%)

# --- Các khoảng (range) cho nhóm ADHD ---
ADHD_OMISSION_RANGE = (0.15, 0.30)      # 15-30%
ADHD_COMMISSION_RANGE = (0.10, 0.20)    # 10-20%
ADHD_RT_MEAN_RANGE = (600, 800)         # 600-800ms
ADHD_RT_STD_RANGE  = (100, 150)         # 100-150ms

# --- Các khoảng (range) cho nhóm Non-ADHD ---
NONADHD_OMISSION_RANGE = (0.00, 0.10)   # 0-10%
NONADHD_COMMISSION_RANGE = (0.00, 0.05) # 0-5%
NONADHD_RT_MEAN_RANGE = (200, 500)      # 200-500ms
NONADHD_RT_STD_RANGE  = (20, 80)        # 20-80ms

# Thư mục đầu ra
OUTPUT_DIR = "cpt_data_combined"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------
# 2. HÀM SINH REACTION TIME
# ----------------------------------
def generate_reaction_time(mean_val, std_val):
    """
    Sinh ngẫu nhiên reaction time (Gaussian),
    đảm bảo > 0 ms.
    """
    rt = -1
    while rt <= 0:
        rt = np.random.normal(loc=mean_val, scale=std_val)
    return int(rt)

# ----------------------------------
# 3. SINH DỮ LIỆU CPT CHO MỘT SUBJECT
# ----------------------------------
def generate_cpt_data_for_subject(num_trials, target_rate,
                                  omission_rate, commission_rate,
                                  rt_mean, rt_std):
    data_rows = []

    for trial_i in range(1, num_trials + 1):
        # 1) Xác định Target hay Non-Target
        is_target = (random.random() < target_rate)
        stimulus_type = "Target" if is_target else "Non-Target"

        # 2) Sinh khả năng lỗi
        if is_target:
            # Tỷ lệ omission
            if random.random() < omission_rate:
                reaction = "No"
                reaction_time = 0
                error_type = "Omission"
            else:
                reaction = "Yes"
                reaction_time = generate_reaction_time(rt_mean, rt_std)
                error_type = "None"
        else:
            # Tỷ lệ commission
            if random.random() < commission_rate:
                reaction = "Yes"
                reaction_time = generate_reaction_time(rt_mean, rt_std)
                error_type = "Commission"
            else:
                reaction = "No"
                reaction_time = 0
                error_type = "None"

        # 3) Tạo dict lưu thông tin
        row = {
            "Trial": trial_i,
            "StimulusType": stimulus_type,
            "Reaction": reaction,
            "ReactionTime": reaction_time,
            "ErrorType": error_type
        }
        data_rows.append(row)

    return data_rows

# ----------------------------------
# 4. HÀM SINH MỘT CHỦ THỂ (ADHD hoặc Non-ADHD)
#    => Trả về data_rows, label
# ----------------------------------
def create_subject_data(label):
    """
    label = "ADHD" hoặc "Non-ADHD".
    Từ đó chọn ra range tương ứng, random omission, commission, rt_mean, rt_std.
    """
    if label == "ADHD":
        omr = random.uniform(*ADHD_OMISSION_RANGE)
        cmr = random.uniform(*ADHD_COMMISSION_RANGE)
        rt_mean = random.uniform(*ADHD_RT_MEAN_RANGE)
        rt_std = random.uniform(*ADHD_RT_STD_RANGE)
    else:  # "Non-ADHD"
        omr = random.uniform(*NONADHD_OMISSION_RANGE)
        cmr = random.uniform(*NONADHD_COMMISSION_RANGE)
        rt_mean = random.uniform(*NONADHD_RT_MEAN_RANGE)
        rt_std = random.uniform(*NONADHD_RT_STD_RANGE)

    # Sinh các trial theo tham số
    data_rows = generate_cpt_data_for_subject(
        num_trials=NUM_TRIALS,
        target_rate=TARGET_RATE,
        omission_rate=omr,
        commission_rate=cmr,
        rt_mean=rt_mean,
        rt_std=rt_std
    )
    return data_rows

# ----------------------------------
# 5. HÀM CHÍNH
# ----------------------------------
def main():
    # A) Tạo dữ liệu cho nhóm ADHD
    for i in range(1, NUM_ADHD_SUBJECTS + 1):
        data_rows = create_subject_data("ADHD")
        
        # Lưu vào file CSV
        filename = os.path.join(OUTPUT_DIR, f"ADHD_subject_{i}.csv")
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Ghi header (6 cột, cột cuối: Label)
            writer.writerow([
                "Trial", 
                "StimulusType", 
                "Reaction", 
                "ReactionTime(ms)", 
                "ErrorType",
                "Label"
            ])
            # Ghi data
            for row in data_rows:
                writer.writerow([
                    row["Trial"],
                    row["StimulusType"],
                    row["Reaction"],
                    row["ReactionTime"],
                    row["ErrorType"],
                    "ADHD"  # gắn nhãn
                ])
        print(f"Đã tạo xong: {filename}")

    # B) Tạo dữ liệu cho nhóm Non-ADHD
    for j in range(1, NUM_NON_ADHD_SUBJECTS + 1):
        data_rows = create_subject_data("Non-ADHD")
        
        # Lưu vào file CSV
        filename = os.path.join(OUTPUT_DIR, f"NonADHD_subject_{j}.csv")
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Trial", 
                "StimulusType", 
                "Reaction", 
                "ReactionTime(ms)", 
                "ErrorType",
                "Label"
            ])
            for row in data_rows:
                writer.writerow([
                    row["Trial"],
                    row["StimulusType"],
                    row["Reaction"],
                    row["ReactionTime"],
                    row["ErrorType"],
                    "Non-ADHD"
                ])
        print(f"Đã tạo xong: {filename}")

if __name__ == "__main__":
    main()
