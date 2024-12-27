import os
import random
import csv
import numpy as np

# ----------------------------------
# 1. THIẾT LẬP THÔNG SỐ
# ----------------------------------

NUM_SUBJECTS = 1000        # Số người cần sinh dữ liệu (toàn Non-ADHD)
NUM_TRIALS = 1200         # Số trial mỗi người
TARGET_RATE = 0.3        # Xác suất xuất hiện Target (VD: 30%)

# Khoảng random CHO NHÓM "KHÔNG ADHD" (thấp hơn hẳn)
OMISSION_RANGE = (0.00, 0.10)     # < 10%
COMMISSION_RANGE = (0.00, 0.05)   # < 5%
RT_MEAN_RANGE = (200, 500)        # phản ứng nhanh (200~500 ms)
RT_STD_RANGE  = (20, 80)          # độ lệch chuẩn thấp (20~80 ms)

# Thư mục đầu ra
OUTPUT_DIR = "non_adhd_data"
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
# 3. SINH DỮ LIỆU CHO TỪNG SUBJECT
# ----------------------------------
def generate_cpt_data_for_subject(num_trials, target_rate,
                                  omission_rate, commission_rate,
                                  rt_mean, rt_std):
    """
    Tạo danh sách (list) các trial (mỗi trial là dict).
    """
    data_rows = []

    for trial_i in range(1, num_trials + 1):
        # 1) Xác định Target hay Non-Target
        is_target = (random.random() < target_rate)
        stimulus_type = "Target" if is_target else "Non-Target"

        # 2) Sinh phản hồi
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

        # 3) Lưu dữ liệu
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
# 4. CHẠY CHÍNH
# ----------------------------------
def main():
    for subject_id in range(1, NUM_SUBJECTS + 1):
        # a) Random “đặc điểm” trong vùng thấp (Non-ADHD)
        sub_omr = random.uniform(*OMISSION_RANGE)
        sub_cmr = random.uniform(*COMMISSION_RANGE)
        sub_rt_mean = random.uniform(*RT_MEAN_RANGE)
        sub_rt_std = random.uniform(*RT_STD_RANGE)

        # b) Sinh dữ liệu trial
        data_rows = generate_cpt_data_for_subject(
            num_trials=NUM_TRIALS,
            target_rate=TARGET_RATE,
            omission_rate=sub_omr,
            commission_rate=sub_cmr,
            rt_mean=sub_rt_mean,
            rt_std=sub_rt_std
        )

        # c) Lưu file CSV
        filename = os.path.join(OUTPUT_DIR, f"NonADHD_subject_{subject_id}.csv")
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow([
                "Trial", 
                "StimulusType", 
                "Reaction", 
                "ReactionTime(ms)", 
                "ErrorType"
            ])
            # Ghi data
            for row in data_rows:
                writer.writerow([
                    row["Trial"],
                    row["StimulusType"],
                    row["Reaction"],
                    row["ReactionTime"],
                    row["ErrorType"]
                ])
        
        print(f"Đã tạo xong file: {filename}")

if __name__ == "__main__":
    main()
