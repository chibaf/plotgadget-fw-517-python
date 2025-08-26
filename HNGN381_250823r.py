#HNGN381_250510A_blk1.py

s0="""
* HNGN381_multi_degC_long_250507A.py  Created on 2025-05-07
* HNGN381_250510A_blk2.pyから、修正する
* 2025-07-24: 新しいデータフォーマット対応（20個の温度データ）
"""

s2="""FWの採集データをプロットします。データ量が多いので少し工夫をします。
実際のフォーマット：10個の温度データ（列2-11）+ 2個の電源オンオフ（列12-13）を処理します。"""

import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np  # 移動平均計算用


# データの例 {250724B}
d00="""
2025 Jul 24 16:34:27.216,451646.06,-9.0625,0.625,0.8125,0.6875,0.5,0.5625,0.3125,0.5,0.6875,0.5,0,0
"""

# ファイル設定
fdir = ''  # サブディレクトリがある場合は指定
#fname = './250805A1/LR5-SSR_2025-07-13_H18_M13_S50.csv'
#fname = './250805A1/LR5-SSR_2025-07-14_H14_M05_S01.csv'
#fname = './250805A1/LR5-SSR_2025-07-17_H21_M48_S10.csv'
#fname = 'LR5-SSR_2025-07-19_H11_M07_S01.csv'
#fname = 'LR5-SSR_2025-07-24_H17_M24_S08.csv'  # 新しいフォーマットのファイル名例
#fname = 'LR5-SSR_2025-07-25_H15_M07_S54.csv'
#fname = 'LR5-SSR_2025-08-01_H15_M18_S17_x.csv' 
#fname = 'LR5-SSR_2025-08-01_H15_M18_S17_2.csv' 
fname = 'LR5-SSR_2025-08-10_H14_M21_S59.csv'
fname = 'LR5-SSR_2025-08-12_H02_M27_S50.csv'
fname = 'LR5-SSR_2025-08-12_H15_M02_S06.csv'
fname = 'LR5-SSR_2025-08-15_H15_M22_S37.csv'
fname = 'LR5-SSR_2025-08-15_H22_M54_S49.csv'
fname = 'LR5-SSR_2025-08-17_H16_M11_S55.csv'
fname = 'LR5-SSR_2025-08-22_H17_M00_S00.csv'
f_dir_name = fdir + fname

# データ格納用のリスト
data = [[] for _ in range(20)]  # 20個の空のリストを用意（10個の温度データ + 2個の電源オンオフ + その他）
x_values = []  # X軸（経過時間）のデータを格納するリスト
power_onoff = [[], []]  # 電源オンオフ用のリスト（2個）

chunk_size = 20  # データを11行ごとに処理

# CSVファイルの読み込みとデータ処理
with open(f_dir_name, 'r') as file:
    csv_reader = csv.reader(file)
    chunk = []
    for i, row in enumerate(csv_reader, 1):
        chunk.append(row)
        if i % chunk_size == 0:
            # 経過時間データを抽出（列1：経過時間（秒））
            try:
                elapsed_time = float(chunk[0][1])  # 経過時間（秒）
                x_values.append(elapsed_time)  # X軸に経過時間を追加
            except (ValueError, IndexError):
                x_values.append(0.0)  # エラー時はデフォルト値
            
            # 温度データを抽出（列2～11：10個の温度データ）
            for j in range(2, 12):  # 温度データの列範囲
                if j < len(chunk[0]):  # 列が存在することを確認
                    try:
                        val = float(chunk[0][j])
                        # 直前10個の平均から±10度以上外れる場合は異常値とみなす
                        prev_vals = data[j][-10:] if len(data[j]) >= 10 else data[j]
                        if prev_vals:
                            prev_avg = sum(prev_vals) / len(prev_vals)
                            if abs(val - prev_avg) > 10.0:
                                # 異常値はNoneで格納（プロット対象外）
                                data[j].append(None)
                                continue
                        data[j].append(val)
                    except (ValueError, IndexError):
                        data[j].append(None)  # エラー時はNone
                else:
                    data[j].append(None)  # 列が存在しない場合はNone
            
            # 電源オンオフを抽出（列12～13：2個の電源オンオフ）
            for k in range(2):  # 電源オンオフは2個
                col_idx = 12 + k  # 列12, 13
                if col_idx < len(chunk[0]):
                    try:
                        power_onoff[k].append(int(chunk[0][col_idx]))
                    except (ValueError, IndexError):
                        power_onoff[k].append(0)
                else:
                    power_onoff[k].append(0)
                    
            chunk = []  # チャンクをリセット

# 移動平均計算関数
def moving_average(data_list, x_list, window_size=20):
    """
    移動平均を計算する関数
    data_list: 温度データのリスト
    x_list: X軸（時間）のリスト  
    window_size: 移動平均の窓サイズ（デフォルト20）
    戻り値: (移動平均データ, 対応するX軸データ)
    """
    if len(data_list) < window_size:
        return data_list, x_list  # データが不足の場合はそのまま返す
    
    moving_avg_data = []
    moving_avg_x = []
    
    for i in range(len(data_list) - window_size + 1):
        # 窓の範囲のデータを取得
        window_data = data_list[i:i + window_size]
        window_x = x_list[i:i + window_size]
        
        # None値を除外して平均計算
        valid_data = [x for x in window_data if x is not None]
        if len(valid_data) > 0:
            avg = sum(valid_data) / len(valid_data)
            moving_avg_data.append(avg)
            # X軸は窓の中央の時間を使用
            center_idx = window_size // 2
            moving_avg_x.append(window_x[center_idx])
        else:
            moving_avg_data.append(None)
            center_idx = window_size // 2
            moving_avg_x.append(window_x[center_idx])
    
    return moving_avg_data, moving_avg_x

# 3つのサブプロットに分割（温度1つ、SSR2つ）
# height_ratios で高さの比率を調整：上段3、中段1、下段1
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 10), sharex=True, 
                                   gridspec_kw={'height_ratios': [2, 0.6, 0.6]})

# 上段：移動平均した温度データ
for i in range(2, 12):  # 温度データの列範囲（2～11列）
    if data[i]:  # データが存在する場合のみ処理
        # データフィルタリング
        filtered_data = [
            value if value <= 1E9 and (value > 0.000005 or value < -0.000005) else None
            for value in data[i]
        ]
        
        # 移動平均計算（20個のデータで移動平均）
        ma_data, ma_x = moving_average(filtered_data, x_values, window_size=20)
        
        # 移動平均をプロット
        ax1.plot(ma_x, ma_data, label=f'Tc{i-1}', linewidth=2, alpha=0.8)

# 上段の設定
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.7, label='0°C (Frz pt)')
ax1.set_ylabel('Temperature (degC)')
ax1.set_title(f'{fname} - Moving Average Temperature Data (Window Size: 20)')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 凡例を右側に配置
ax1.grid(True, alpha=0.3)

# 中段：SSR OnOff 1（移動平均なし）
if power_onoff[0]:
    ax2.plot(x_values, power_onoff[0], label='Core OnOff', 
            marker='o', markersize=2, linewidth=1, alpha=0.8, color='red')

# 中段の設定
ax2.set_ylabel('Heater OnOff')
ax2.set_title(f'{fname} - SSR OnOff (Top/Wall/Bottom Heater))')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(-0.5, 1.5)

# 下段：SSR OnOff 2（移動平均なし）
if power_onoff[1]:
    ax3.plot(x_values, power_onoff[1], label='Freezer OnOff', 
            marker='o', markersize=2, linewidth=1, alpha=0.8, color='blue')

# 下段の設定
ax3.set_ylabel('Freezer OnOff')
ax3.set_xlabel('Elapsed Time (seconds)')
ax3.set_title(f'{fname} - SSR OnOff (Freezer Power))')
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax3.grid(True, alpha=0.3)
ax3.set_ylim(-0.5, 1.5)

# レイアウト調整
plt.tight_layout()
plt.subplots_adjust(right=0.85)  # 凡例のスペースを確保
plt.show()