import numpy as np
import pandas as pd
import os
import random

def generate_raw_trials_for_subject(subnum, blocks_info, rt_mean, rt_std, acc_target):
    """
    Sinh ra 'raw trial' cho 1 người, dựa trên:
      - blocks_info: danh sách (block_id, block_type, số trial trong block)
      - rt_mean, rt_std: phân phối RT (ms)
      - acc_target: độ chính xác mục tiêu (kỳ vọng), để xác định tỉ lệ trial đúng/sai
    Trả về list (mỗi element là 1 dict cho 1 trial).
    """
    all_trials = []
    trial_global_count = 0

    for (block_id, block_type, n_trials) in blocks_info:
        for i in range(1, n_trials + 1):
            trial_global_count += 1
            # correctres = P hoặc R (ngẫu nhiên)
            correctres = random.choice(["P", "R"])
            # stim = P hoặc R (cho sẵn, có thể trùng correctres hoặc không)
            stim = random.choice(["P", "R"])

            # Giả định "choice" = 1..4 (ngẫu nhiên)
            choice = random.choice([1,2,3,4])
            # x, y toạ độ (VD: 668, 532, 868, v.v.) - tùy bạn
            x = random.choice([668, 868])
            y = random.choice([332, 532])

            # starttime: Mô phỏng, mỗi trial cách nhau tầm 1500-3000 ms?
            # Hoặc cộng dồn, tuỳ ý. Ở đây cho random để minh hoạ.
            starttime = random.randint(1000, 50000)

            # RT: random theo Gaussian
            rt = -1
            while rt <= 0:
                rt = np.random.normal(rt_mean, rt_std)

            # Xác suất trial này "đúng" = acc_target => corr=1, sai => corr=0
            # Ta random theo 1 distribution thay vì so sánh stim/correctres thật
            is_correct = (random.random() < acc_target)
            corr = 1 if is_correct else 0

            # response: chuỗi text, ta chỉ mô phỏng 4 giá trị "700|300|1|<pressed>"
            #   x hoặc y thay đổi chút
            rx = random.randint(700, 800)
            ry = random.randint(300, 600)
            response = f"{rx}|{ry}|1|<pressed>"

            # responded: =1 nếu có phản hồi
            responded = 1

            # present: =1 (giả sử luôn hiển thị)
            present = 1

            row = {
                "subnum": subnum,
                "block": block_id,
                "type": block_type,
                "correctres": correctres,
                "trial": i,
                "choice": choice,
                "x": x,
                "y": y,
                "stim": stim,
                "present": present,
                "response": response,
                "responded": responded,
                "corr": corr,
                "starttime": starttime,
                "rt": rt
            }
            all_trials.append(row)
    return all_trials


def compute_accuracy_and_meanrt(trials):
    """
    Tính Accuracy (%) và mean RT (chỉ tính trial corr=1).
    """
    total_trials = len(trials)
    correct_trials = [t for t in trials if t["corr"] == 1]
    acc = 0.0
    mean_rt = 0.0
    if total_trials > 0:
        acc = (len(correct_trials) / total_trials) * 100.0
    if len(correct_trials) > 0:
        mean_rt = np.mean([t["rt"] for t in correct_trials])
    return acc, mean_rt


def impulsive_score(acc, mean_rt):
    """
    Impulsive Score = (100 - acc) * (1 + mean_rt/1000)
    """
    return (100 - acc) * (1 + mean_rt/1000.0)


def generate_subject_rawdata(subnum, label, blocks_info, rt_mean, rt_std, acc_mean, acc_std, threshold=15.613, max_attempts=10000):
    """
    Sinh raw trials cho 1 subject, đảm bảo:
      - label='ADHD' => impulsive_score >= threshold
      - label='Non-ADHD' => impulsive_score < threshold
    """
    for _ in range(max_attempts):
        # random acc_target ~ Normal(acc_mean, acc_std), giới hạn 0..1
        acc_target = np.clip(np.random.normal(acc_mean, acc_std), 0, 1)
        # Lưu ý: acc_target = 0.8 => 80%

        # Sinh trial
        trials = generate_raw_trials_for_subject(subnum, blocks_info, rt_mean, rt_std, acc_target)

        # Tính acc, mean_rt
        acc_val, mean_rt_val = compute_accuracy_and_meanrt(trials)
        score = impulsive_score(acc_val, mean_rt_val)

        # Kiểm tra label
        if label == "ADHD" and score >= threshold:
            return trials, acc_val, mean_rt_val, score
        if label == "Non-ADHD" and score < threshold:
            return trials, acc_val, mean_rt_val, score

    return None, None, None, None  # nếu thử max_attempts mà vẫn không ra


def main():
    # ------------------------------------------------
    # 1) THIẾT LẬP THAM SỐ
    # ------------------------------------------------
    NUM_ADHD = 1000
    NUM_NONADHD = 1000
    IMPULSIVE_THRESHOLD = 15.613

    # Mỗi người sẽ có 2 block: practice (10 trial), test (20 trial)
    blocks_info = [
        (0, "practice", 10),
        (1, "test", 20)
    ]

    # Giả sử: 
    #  - Nhóm ADHD => RT_mean=450, RT_std=40, acc_mean=0.8 (80%), acc_std=0.1
    #  - Nhóm Non-ADHD => RT_mean=350, RT_std=30, acc_mean=0.95 (95%), acc_std=0.05
    ADHD_RT_MEAN, ADHD_RT_STD = 450, 40
    ADHD_ACC_MEAN, ADHD_ACC_STD = 0.8, 0.1

    NONADHD_RT_MEAN, NONADHD_RT_STD = 350, 30
    NONADHD_ACC_MEAN, NONADHD_ACC_STD = 0.95, 0.05

    # ------------------------------------------------
    # 2) SINH NHÓM ADHD
    # ------------------------------------------------
    print("Đang sinh dữ liệu ADHD...")
    all_adhd_rows = []
    sub_count = 0
    while sub_count < NUM_ADHD:
        sub_id = sub_count + 1
        trials, acc_val, mean_rt_val, score_val = generate_subject_rawdata(
            subnum=sub_id,
            label="ADHD",
            blocks_info=blocks_info,
            rt_mean=ADHD_RT_MEAN,
            rt_std=ADHD_RT_STD,
            acc_mean=ADHD_ACC_MEAN,
            acc_std=ADHD_ACC_STD,
            threshold=IMPULSIVE_THRESHOLD
        )
        if trials is not None:
            # Lưu
            all_adhd_rows.extend(trials)
            sub_count += 1
        else:
            # Nếu hiếm khi random ko đạt => có thể điều chỉnh
            print("Không thể sinh subject ADHD hợp lệ (score >= 15.613) sau nhiều lần thử.")
            break

    # ------------------------------------------------
    # 3) SINH NHÓM NON-ADHD
    # ------------------------------------------------
    print("Đang sinh dữ liệu Non-ADHD...")
    all_nonadhd_rows = []
    sub_count = 0
    while sub_count < NUM_NONADHD:
        sub_id = sub_count + 1
        trials, acc_val, mean_rt_val, score_val = generate_subject_rawdata(
            subnum=sub_id,
            label="Non-ADHD",
            blocks_info=blocks_info,
            rt_mean=NONADHD_RT_MEAN,
            rt_std=NONADHD_RT_STD,
            acc_mean=NONADHD_ACC_MEAN,
            acc_std=NONADHD_ACC_STD,
            threshold=IMPULSIVE_THRESHOLD
        )
        if trials is not None:
            all_nonadhd_rows.extend(trials)
            sub_count += 1
        else:
            print("Không thể sinh subject Non-ADHD hợp lệ (score < 15.613) sau nhiều lần thử.")
            break

    # ------------------------------------------------
    # 4) LƯU CSV RA 2 FILE
    # ------------------------------------------------
    os.makedirs("raw_data_generated", exist_ok=True)

    # ADHD
    df_adhd = pd.DataFrame(all_adhd_rows)
    df_adhd.to_csv("raw_data_generated/ADHD_raw_1000.csv", index=False)

    # Non-ADHD
    df_nonadhd = pd.DataFrame(all_nonadhd_rows)
    df_nonadhd.to_csv("raw_data_generated/NonADHD_raw_1000.csv", index=False)

    print(f"Done. ADHD: {df_adhd.shape[0]} rows, Non-ADHD: {df_nonadhd.shape[0]} rows.")

    # In thử 5 dòng
    print("\n--- ADHD (5 rows) ---")
    print(df_adhd.head())
    print("\n--- Non-ADHD (5 rows) ---")
    print(df_nonadhd.head())


if __name__ == "__main__":
    main()
