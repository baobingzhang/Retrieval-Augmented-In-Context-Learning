"""
传感器数据可视化脚本 V0 - 4张核心图表
============================================
生成2行2列的统计可视化图表
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# =============================================================================
# 配置 - 学术论文风格
# =============================================================================
DATA_DIR = './data'
OUTPUT_DIR = './pics'

# 设置学术论文风格
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'figure.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# 配色
PALETTE = ['#2C3E50', '#3498DB', '#E74C3C', '#27AE60', '#F39C12', '#9B59B6', '#1ABC9C', '#E67E22']
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
}

def load_all_data():
    """加载所有数据文件并合并"""
    excel_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.xlsx')])
    all_data = []
    
    for filename in excel_files:
        filepath = os.path.join(DATA_DIR, filename)
        df = pd.read_excel(filepath)
        all_data.append(df)
    
    combined = pd.concat(all_data, ignore_index=True)
    combined['timestamp'] = pd.to_datetime(combined['timestamp'])
    combined['hour'] = combined['timestamp'].dt.hour
    combined['date'] = combined['timestamp'].dt.date
    
    return combined


def plot_activity_distribution(ax, data):
    """Top 10 活动分布 - 水平柱状图"""
    activity_counts = data['Activity'].value_counts().head(10)
    
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(activity_counts))]
    
    bars = ax.barh(range(len(activity_counts)), activity_counts.values, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_yticks(range(len(activity_counts)))
    ax.set_yticklabels([a.replace('_', ' ').title() for a in activity_counts.index], fontsize=8)
    ax.set_xlabel('Number of Records')
    ax.set_title('(a) Top 10 Activity Distribution')
    ax.invert_yaxis()
    
    for i, (bar, val) in enumerate(zip(bars, activity_counts.values)):
        ax.text(val + 50, i, f'{val:,}', va='center', fontsize=7, color=COLORS['primary'])


def main():
    print("\n" + "=" * 60)
    print("  生成4张核心可视化图表 (V0)")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n  [1/3] 加载数据...")
    data = load_all_data()
    print(f"        已加载 {len(data):,} 条记录")
    
    print("\n  [2/3] 生成可视化图表...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    plot_activity_distribution(axes[0, 0], data)
    
    plt.tight_layout()
    
    print("\n  [3/3] 保存图像...")
    output_path = os.path.join(OUTPUT_DIR, 'data_visualization_v0.png')
    plt.savefig(output_path, dpi=300, facecolor='white', edgecolor='none')
    print(f"        已保存: {output_path}")
    
    plt.close()
    
    print("\n" + "=" * 60)
    print("  ✅ 可视化完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
