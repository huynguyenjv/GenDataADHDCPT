import os
import random
import csv
import numpy as np

# ----------------------------------
# 1. THIẾT LẬP THÔNG SỐ
# ----------------------------------

NUM_SUBJECTS = 1000        # Số người cần (toàn ADHD)
NUM_TRIALS = 1200         # Số trial mỗi người
TARGET_RATE = 0.3        # Xác suất Target

# Ta vẫn random trong khoảng tương đối rộng,
# rồi kiểm tra ngưỡng ADHD; nếu chưa đủ thì random lại.
OMISSION_RANGE = (0.00, 0.40)
COMMISSION_RANGE = (0.00, 0.30)
RT_MEAN_RANGE = (300, 800)
RT_STD_RANGE  = (50, 200)

# Ngưỡng để gọi là ADHD:
OMISSION_THRESHOLD = 0.15
COMMISSION_THRESHOLD = 0.10
RT_MEAN_THRESHOLD = 600
RT_STD_THRESHOLD = 100

OUTPUT_DIR = "adhd_data_only_check"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ----------------------------------
# 2. HÀM SINH VÀ TÍNH TOÁN METRIC
# ----------------------------------

def generate_reaction_time(mean_val, std_val):
    rt = -1
    while rt <= 0:
        rt = np.random.normal(loc=mean_val, scale=std_val)
    return int(rt)

def generate_cpt_data_for_subject(num_trials, target_rate,
                                  omission_rate, commission_rate,
                                  rt_mean, rt_std):
    data_rows = []
    for trial_i in range(1, num_trials + 1):
        is_target = (random.random() < target_rate)
        stimulus_type = "Target" if is_target else "Non-Target"

        if is_target:
            if random.random() < omission_rate:
                reaction = "No"
                reaction_time = 0
                error_type = "Omission"
            else:
                reaction = "Yes"
                reaction_time = generate_reaction_time(rt_mean, rt_std)
                error_type = "None"
        else:
            if random.random() < commission_rate:
                reaction = "Yes"
                reaction_time = generate_reaction_time(rt_mean, rt_std)
                error_type = "Commission"
            else:
                reaction = "No"
                reaction_time = 0
                error_type = "None"

        row = {
            "Trial": trial_i,
            "StimulusType": stimulus_type,
            "Reaction": reaction,
            "ReactionTime": reaction_time,
            "ErrorType": error_type
        }
        data_rows.append(row)

    return data_rows

def compute_cpt_metrics(data_rows):
    num_target = sum(1 for r in data_rows if r["StimulusType"] == "Target")
    num_non_target = len(data_rows) - num_target

    num_omission = sum(1 for r in data_rows 
                       if r["StimulusType"] == "Target" 
                       and r["ErrorType"] == "Omission")
    num_commission = sum(1 for r in data_rows 
                         if r["StimulusType"] == "Non-Target" 
                         and r["ErrorType"] == "Commission")

    omission_rate = num_omission / num_target if num_target > 0 else 0.0
    commission_rate = num_commission / num_non_target if num_non_target > 0 else 0.0

    correct_target_rts = [
        r["ReactionTime"] for r in data_rows
        if r["StimulusType"] == "Target"
        and r["ErrorType"] == "None"
        and r["ReactionTime"] > 0
    ]
    if len(correct_target_rts) > 1:
        rt_mean = np.mean(correct_target_rts)
        rt_std = np.std(correct_target_rts, ddof=1)
    else:
        rt_mean = 0.0
        rt_std = 0.0

    return omission_rate, commission_rate, rt_mean, rt_std

def is_adhd(omr, cmr, rt_mean, rt_std):
    """
    Trả về True nếu THỎA MÃN tiêu chí ADHD.
    Tiêu chí: 
        OmR > 0.15 
        hoặc ComR > 0.10 
        hoặc RT_mean > 600 
        hoặc RT_std > 100
    """
    if (omr > OMISSION_THRESHOLD or
        cmr > COMMISSION_THRESHOLD or
        rt_mean > RT_MEAN_THRESHOLD or
        rt_std > RT_STD_THRESHOLD):
        return True
    return False


# ----------------------------------
# 3. MAIN: Random tới khi "đủ ADHD" thì thôi
# ----------------------------------

def main():
    for subject_id in range(1, NUM_SUBJECTS + 1):
        # Vòng lặp để chắc chắn ra được 1 subject ADHD
        while True:
            # 1) Random cấu hình
            sub_omr = random.uniform(*OMISSION_RANGE)
            sub_cmr = random.uniform(*COMMISSION_RANGE)
            sub_rt_mean = random.uniform(*RT_MEAN_RANGE)
            sub_rt_std  = random.uniform(*RT_STD_RANGE)

            # 2) Sinh trial
            data_rows = generate_cpt_data_for_subject(
                num_trials=NUM_TRIALS,
                target_rate=TARGET_RATE,
                omission_rate=sub_omr,
                commission_rate=sub_cmr,
                rt_mean=sub_rt_mean,
                rt_std=sub_rt_std
            )

            # 3) Tính metric thực tế
            actual_omr, actual_cmr, actual_rt_mean, actual_rt_std = compute_cpt_metrics(data_rows)

            # 4) Kiểm tra ngưỡng ADHD
            if is_adhd(actual_omr, actual_cmr, actual_rt_mean, actual_rt_std):
                # OK, ta đã có subject ADHD => dừng while
                break
            # Nếu chưa đủ tiêu chí => lặp tiếp (sinh lại)

        # Lưu file CSV
        filename = os.path.join(OUTPUT_DIR, f"ADHD_subject_{subject_id}.csv")
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Trial", 
                             "StimulusType", 
                             "Reaction", 
                             "ReactionTime(ms)", 
                             "ErrorType",
                             "Label"])
            for row in data_rows:
                writer.writerow([
                    row["Trial"],
                    row["StimulusType"],
                    row["Reaction"],
                    row["ReactionTime"],
                    row["ErrorType"],
                    "ADHD"  # Chắc chắn ADHD
                ])
        
        print(f"Subject {subject_id}: OmR={actual_omr:.3f}, CmR={actual_cmr:.3f}, "
              f"RTmean={actual_rt_mean:.2f}, RTstd={actual_rt_std:.2f} => ADHD")
        print(f"File saved: {filename}\n")

if __name__ == "__main__":
    main()
