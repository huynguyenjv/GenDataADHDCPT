import pandas as pd
import os

def evaluate_adhd_condition(datafile, threshold=15.613):
    """
    Đọc file CSV (raw data), gom nhóm theo subnum (mỗi người),
    tính Accuracy, Mean RT, Impulsive Score, và suy ra Label (ADHD / Non-ADHD).
    
    Trả về DataFrame với cột:
      subnum, Accuracy, Mean_RT, Impulsive_Score, Label
    """
    # Đọc dữ liệu raw
    df = pd.read_csv(datafile)

    results = []
    
    # Gom nhóm theo subnum
    for subnum, group in df.groupby('subnum'):
        # 1) Tính tổng trial
        total_trials = len(group)
        
        # 2) Số trial đúng (corr = 1)
        correct_trials = group[group['corr'] == 1]
        num_correct = len(correct_trials)
        
        # 3) Accuracy (%)
        if total_trials > 0:
            acc_percent = (num_correct / total_trials) * 100
        else:
            acc_percent = 0.0

        # 4) Mean RT (chỉ tính trial đúng)
        if num_correct > 0:
            mean_rt = correct_trials['rt'].mean()
        else:
            mean_rt = 0.0

        # 5) Impulsive Score
        impulsive_score = (100 - acc_percent) * (1 + mean_rt / 1000.0)

        # 6) Gán nhãn
        label = "ADHD" if impulsive_score >= threshold else "Non-ADHD"

        results.append({
            "subnum": subnum,
            "Accuracy": acc_percent,
            "Mean_RT": mean_rt,
            "Impulsive_Score": impulsive_score,
            "Label": label
        })

    # Tạo DataFrame kết quả
    df_results = pd.DataFrame(results)
    return df_results

def main():
    # Giả sử bạn có 2 file:
    #   - raw_data_generated/ADHD_raw_1000.csv
    #   - raw_data_generated/NonADHD_raw_1000.csv
    # Sinh bởi code trước đó.
    
    # Đánh giá file ADHD_raw_1000.csv
    adhd_file = "raw_data_generated/ADHD_raw_1000.csv"
    if os.path.exists(adhd_file):
        df_adhd_eval = evaluate_adhd_condition(adhd_file)
        df_adhd_eval.to_csv("raw_data_generated/ADHD_evaluation.csv", index=False)
        print("[*] Đã đánh giá dữ liệu trong", adhd_file)
        print(df_adhd_eval.head(10))
    else:
        print("Không tìm thấy file:", adhd_file)

    # Đánh giá file NonADHD_raw_1000.csv
    nonadhd_file = "raw_data_generated/NonADHD_raw_1000.csv"
    if os.path.exists(nonadhd_file):
        df_nonadhd_eval = evaluate_adhd_condition(nonadhd_file)
        df_nonadhd_eval.to_csv("raw_data_generated/NonADHD_evaluation.csv", index=False)
        print("[*] Đã đánh giá dữ liệu trong", nonadhd_file)
        print(df_nonadhd_eval.head(10))
    else:
        print("Không tìm thấy file:", nonadhd_file)

if __name__ == "__main__":
    main()
