"""
数据分析脚本 - 全方位统计分析
==========================================
分析汇总并输出当前数据的全面统计信息
所有输出同时保存到文件
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# =============================================================================
# 配置
# =============================================================================
DATA_DIR = '/home/baobin/Desktop/icsr2026/data'
OUTPUT_DIR = '/home/baobin/Desktop/icsr2026/data_analysis'
REPORT_FILE = os.path.join(OUTPUT_DIR, 'data_statistics_report.txt')


class DualOutput:
    """同时输出到屏幕和文件"""
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.file = open(filepath, 'w', encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.file.flush()
    
    def close(self):
        self.file.close()


def load_all_data():
    """加载所有数据文件并合并"""
    excel_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.xlsx')])
    all_data = []
    file_info = []
    
    for filename in excel_files:
        filepath = os.path.join(DATA_DIR, filename)
        df = pd.read_excel(filepath)
        all_data.append(df)
        file_info.append({
            'filename': filename,
            'records': len(df),
            'columns': len(df.columns)
        })
    
    combined = pd.concat(all_data, ignore_index=True)
    combined['timestamp'] = pd.to_datetime(combined['timestamp'])
    
    return combined, file_info


def print_header(title):
    """打印标题"""
    print("\n")
    print("╔" + "═" * 80 + "╗")
    print("║" + f"  {title}  ".center(80) + "║")
    print("╚" + "═" * 80 + "╝")


def analyze_basic_info(data, file_info):
    """基本信息分析"""
    print_header("1. 数据集基本信息")
    
    print(f"""
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  数据集概览                                                                 │
    ├────────────────────────────────────────────────────────────────────────────┤
    │  数据文件数量:        {len(file_info):>10} 个                                        │
    │  总记录数:            {len(data):>10,} 条                                        │
    │  特征列数:            {len(data.columns):>10} 列                                        │
    │  数据时间范围:        {data['timestamp'].min().strftime('%Y-%m-%d %H:%M')} ~ {data['timestamp'].max().strftime('%Y-%m-%d %H:%M')}      │
    │  数据天数:            {(data['timestamp'].max() - data['timestamp'].min()).days + 1:>10} 天                                        │
    └────────────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n    各数据文件统计:")
    print("    " + "-" * 70)
    print(f"    {'序号':<6} {'文件名':<45} {'记录数':<12} {'列数':<8}")
    print("    " + "-" * 70)
    for i, info in enumerate(file_info, 1):
        print(f"    {i:<6} {info['filename']:<45} {info['records']:<12,} {info['columns']:<8}")
    print("    " + "-" * 70)


def analyze_columns(data):
    """列信息分析"""
    print_header("2. 数据列信息")
    
    # 分类列
    value_cols = [c for c in data.columns if c.endswith(' value')]
    other_cols = [c for c in data.columns if c not in value_cols]
    
    print(f"""
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  列分类统计                                                                 │
    ├────────────────────────────────────────────────────────────────────────────┤
    │  基础信息列:          {len(other_cols):>10} 列  (timestamp, Activity, Location)        │
    │  传感器 value 列:     {len(value_cols):>10} 列                                        │
    │  总计:                {len(data.columns):>10} 列                                        │
    └────────────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n    所有列名:")
    print("    " + "-" * 70)
    for i, col in enumerate(data.columns, 1):
        dtype = str(data[col].dtype)
        null_count = data[col].isnull().sum()
        null_pct = null_count / len(data) * 100
        print(f"    {i:>2}. {col:<40} [{dtype:<15}] 缺失: {null_pct:.1f}%")
    print("    " + "-" * 70)


def analyze_activity(data):
    """活动分析"""
    print_header("3. 活动 (Activity) 分析")
    
    activity_counts = data['Activity'].value_counts()
    total = len(data)
    
    print(f"""
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  活动类型统计                                                               │
    ├────────────────────────────────────────────────────────────────────────────┤
    │  活动类型数量:        {len(activity_counts):>10} 种                                        │
    │  缺失值数量:          {data['Activity'].isnull().sum():>10,} 条                                        │
    └────────────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n    各活动类型详情:")
    print("    " + "-" * 70)
    print(f"    {'序号':<6} {'活动名称':<30} {'记录数':<12} {'占比':<10}")
    print("    " + "-" * 70)
    for i, (activity, count) in enumerate(activity_counts.items(), 1):
        pct = count / total * 100
        print(f"    {i:<6} {activity:<30} {count:<12,} {pct:.2f}%")
    print("    " + "-" * 70)
    print(f"    {'总计':<6} {'':<30} {total:<12,} {'100.00%':<10}")


def analyze_location(data):
    """位置分析"""
    print_header("4. 位置 (Location) 分析")
    
    location_counts = data['Location'].value_counts()
    total = len(data)
    
    print(f"""
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  位置统计                                                                   │
    ├────────────────────────────────────────────────────────────────────────────┤
    │  位置类型数量:        {len(location_counts):>10} 种                                        │
    │  缺失值数量:          {data['Location'].isnull().sum():>10,} 条                                        │
    └────────────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n    各位置详情:")
    print("    " + "-" * 70)
    print(f"    {'序号':<6} {'位置名称':<35} {'记录数':<12} {'占比':<10}")
    print("    " + "-" * 70)
    for i, (location, count) in enumerate(location_counts.items(), 1):
        pct = count / total * 100
        print(f"    {i:<6} {str(location):<35} {count:<12,} {pct:.2f}%")
    print("    " + "-" * 70)


def analyze_sensors(data):
    """传感器分析"""
    print_header("5. 传感器 (Sensor) 分析")
    
    value_cols = [c for c in data.columns if c.endswith(' value')]
    
    # 按类别分组
    categories = {
        '动作传感器 (Motion)': [],
        '门传感器 (Door)': [],
        '抽屉传感器 (Drawer)': [],
        '接触传感器 (Contact/Lid)': [],
        '座位传感器 (Seatplace)': []
    }
    
    for col in value_cols:
        sensor_name = col.replace(' value', '')
        if 'motion' in sensor_name.lower():
            categories['动作传感器 (Motion)'].append(col)
        elif 'door' in sensor_name.lower():
            categories['门传感器 (Door)'].append(col)
        elif 'drawer' in sensor_name.lower():
            categories['抽屉传感器 (Drawer)'].append(col)
        elif 'contact' in sensor_name.lower() or 'lid' in sensor_name.lower():
            categories['接触传感器 (Contact/Lid)'].append(col)
        elif 'seatplace' in sensor_name.lower():
            categories['座位传感器 (Seatplace)'].append(col)
    
    print(f"""
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  传感器概览                                                                 │
    ├────────────────────────────────────────────────────────────────────────────┤
    │  传感器总数:          {len(value_cols):>10} 个                                        │
    └────────────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n    传感器分类统计:")
    for category, cols in categories.items():
        if cols:
            print(f"\n    【{category}】({len(cols)}个)")
            for col in sorted(cols):
                sensor_name = col.replace(' value', '')
                non_zero = (data[col].fillna(0) != 0).sum()
                non_zero_pct = non_zero / len(data) * 100
                mean_val = data[col].mean()
                print(f"        • {sensor_name:<35} 非零记录: {non_zero:>6,} ({non_zero_pct:>5.1f}%)  均值: {mean_val:.3f}")


def analyze_sensor_statistics(data):
    """传感器统计详情"""
    print_header("6. 传感器数值统计")
    
    value_cols = [c for c in data.columns if c.endswith(' value')]
    
    print("\n    传感器数值统计详情:")
    print("    " + "-" * 90)
    print(f"    {'传感器名称':<35} {'最小值':<10} {'最大值':<10} {'均值':<12} {'标准差':<12} {'非零占比':<10}")
    print("    " + "-" * 90)
    
    for col in sorted(value_cols):
        sensor_name = col.replace(' value', '')
        min_val = data[col].min()
        max_val = data[col].max()
        mean_val = data[col].mean()
        std_val = data[col].std()
        non_zero_pct = (data[col].fillna(0) != 0).sum() / len(data) * 100
        
        print(f"    {sensor_name:<35} {min_val:<10.2f} {max_val:<10.2f} {mean_val:<12.4f} {std_val:<12.4f} {non_zero_pct:<10.1f}%")
    
    print("    " + "-" * 90)


def analyze_time_distribution(data):
    """时间分布分析"""
    print_header("7. 时间分布分析")
    
    data = data.copy()
    data['hour'] = data['timestamp'].dt.hour
    data['date'] = data['timestamp'].dt.date
    
    hourly = data.groupby('hour').size()
    daily = data.groupby('date').size()
    
    print(f"""
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  时间分布统计                                                               │
    ├────────────────────────────────────────────────────────────────────────────┤
    │  每日平均记录数:      {daily.mean():>10.0f} 条                                        │
    │  每小时平均记录数:    {hourly.mean():>10.0f} 条                                        │
    │  记录最多的日期:      {daily.idxmax()} ({daily.max():,} 条)                     │
    │  记录最少的日期:      {daily.idxmin()} ({daily.min():,} 条)                     │
    │  记录最多的小时:      {hourly.idxmax():>2}:00 ({hourly.max():,} 条)                           │
    │  记录最少的小时:      {hourly.idxmin():>2}:00 ({hourly.min():,} 条)                             │
    └────────────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n    每日数据量:")
    print("    " + "-" * 50)
    for date, count in daily.items():
        bar = "█" * int(count / daily.max() * 30)
        print(f"    {date}  {bar} {count:,}")
    print("    " + "-" * 50)
    
    print("\n    每小时数据量分布:")
    print("    " + "-" * 50)
    for hour in range(24):
        if hour in hourly.index:
            count = hourly[hour]
            bar = "█" * int(count / hourly.max() * 30)
            print(f"    {hour:02d}:00  {bar} {count:,}")
    print("    " + "-" * 50)


def generate_summary_report(data, file_info):
    """生成汇总报告"""
    print_header("8. 数据集汇总报告")
    
    value_cols = [c for c in data.columns if c.endswith(' value')]
    
    print(f"""
    ══════════════════════════════════════════════════════════════════════════════
                              数 据 集 汇 总 报 告
    ══════════════════════════════════════════════════════════════════════════════
    
    数据规模
       ├─ 数据文件:       {len(file_info)} 个
       ├─ 总记录数:       {len(data):,} 条
       ├─ 特征列数:       {len(data.columns)} 列
       └─ 数据大小:       约 {len(data) * len(data.columns) / 1000:.1f}K 数据点
    
    时间跨度
       ├─ 起始时间:       {data['timestamp'].min().strftime('%Y-%m-%d %H:%M:%S')}
       ├─ 结束时间:       {data['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')}
       └─ 持续天数:       {(data['timestamp'].max() - data['timestamp'].min()).days + 1} 天
    
    活动类型
       ├─ 活动种类:       {data['Activity'].nunique()} 种
       ├─ 主要活动:       {data['Activity'].value_counts().index[0]} ({data['Activity'].value_counts().iloc[0]:,}条, {data['Activity'].value_counts().iloc[0]/len(data)*100:.1f}%)
       └─ 缺失率:         {data['Activity'].isnull().sum()/len(data)*100:.2f}%
    
    位置信息
       ├─ 位置种类:       {data['Location'].nunique()} 种
       ├─ 主要位置:       {data['Location'].value_counts().index[0]} ({data['Location'].value_counts().iloc[0]:,}条, {data['Location'].value_counts().iloc[0]/len(data)*100:.1f}%)
       └─ 缺失率:         {data['Location'].isnull().sum()/len(data)*100:.2f}%
    
    传感器信息
       ├─ 传感器总数:     {len(value_cols)} 个
       ├─ 动作传感器:     {len([c for c in value_cols if 'motion' in c.lower()])} 个
       ├─ 门传感器:       {len([c for c in value_cols if 'door' in c.lower()])} 个
       ├─ 抽屉传感器:     {len([c for c in value_cols if 'drawer' in c.lower()])} 个
       ├─ 座位传感器:     {len([c for c in value_cols if 'seatplace' in c.lower()])} 个
       └─ 其他传感器:     {len([c for c in value_cols if not any(k in c.lower() for k in ['motion', 'door', 'drawer', 'seatplace'])])} 个
    
    ══════════════════════════════════════════════════════════════════════════════
    """)


def main():
    # 设置双重输出（屏幕 + 文件）
    dual_output = DualOutput(REPORT_FILE)
    sys.stdout = dual_output
    
    try:
        print("\n" + "=" * 80)
        print(f"        数据集全方位统计分析")
        print(f"        生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 加载数据
        print("\n  正在加载数据...")
        data, file_info = load_all_data()
        print(f"  已加载 {len(data):,} 条记录\n")
        
        # 各项分析
        analyze_basic_info(data, file_info)
        analyze_columns(data)
        analyze_activity(data)
        analyze_location(data)
        analyze_sensors(data)
        analyze_sensor_statistics(data)
        analyze_time_distribution(data)
        generate_summary_report(data, file_info)
        
        print("\n" + "=" * 80)
        print("  分析完成!")
        print(f"  完整报告已保存: {REPORT_FILE}")
        print("=" * 80 + "\n")
        
    finally:
        # 恢复标准输出
        sys.stdout = dual_output.terminal
        dual_output.close()
        
    print(f"\n  完整报告已保存: {REPORT_FILE}\n")


if __name__ == "__main__":
    main()