"""
数据清洗脚本 - 删除传感器的 XYCoord 和 status 列
============================================
只保留 value 列，覆盖原数据文件
"""

import pandas as pd
import os
from datetime import datetime

# =============================================================================
# 配置
# =============================================================================
DATA_DIR = './data'

def clean_sensor_columns(df):
    """
    删除所有传感器的 XYCoord 和 status 列，只保留 value 列
    """
    columns_to_drop = []
    
    for col in df.columns:
        # 检查是否是 XYCoord 列
        if col.endswith(' XYCoord'):
            columns_to_drop.append(col)
        # 检查是否是 status 列
        elif col.endswith(' status'):
            columns_to_drop.append(col)
    
    # 删除这些列
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')
    
    return df_cleaned, columns_to_drop


def main():
    print("\n" + "=" * 60)
    print("  数据清洗 - 删除 XYCoord 和 status 列")
    print("=" * 60)
    
    # 获取所有Excel文件
    excel_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.xlsx')])
    print(f"\n  发现 {len(excel_files)} 个数据文件")
    
    total_dropped = set()
    
    for i, filename in enumerate(excel_files, 1):
        filepath = os.path.join(DATA_DIR, filename)
        print(f"\n  [{i}/{len(excel_files)}] 处理: {filename}")
        
        # 读取数据
        df = pd.read_excel(filepath)
        original_cols = len(df.columns)
        
        # 清洗数据
        df_cleaned, dropped_cols = clean_sensor_columns(df)
        new_cols = len(df_cleaned.columns)
        
        total_dropped.update(dropped_cols)
        
        print(f"        原始列数: {original_cols}")
        print(f"        删除列数: {len(dropped_cols)}")
        print(f"        保留列数: {new_cols}")
        
        # 覆盖保存
        df_cleaned.to_excel(filepath, index=False)
        print(f"        ✅ 已保存")
    
    print("\n" + "=" * 60)
    print("  清洗完成!")
    print("=" * 60)
    
    print(f"\n  删除的列类型汇总:")
    xycoord_cols = [c for c in total_dropped if c.endswith(' XYCoord')]
    status_cols = [c for c in total_dropped if c.endswith(' status')]
    
    print(f"  - XYCoord 列: {len(xycoord_cols)} 个")
    print(f"  - status 列:  {len(status_cols)} 个")
    print(f"  - 总计删除:   {len(total_dropped)} 个")
    
    print("\n  删除的列清单:")
    for col in sorted(total_dropped):
        print(f"    - {col}")


if __name__ == "__main__":
    main()
