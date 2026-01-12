# Robot House Sensor-based Human Activity Recognition

A research project focusing on Human Activity Recognition (HAR) using sensor data from a robot house environment.

## Project Overview

This project analyzes sensor data collected from a smart home environment to recognize and classify human activities. The dataset includes various types of sensors such as motion sensors, door sensors, drawer sensors, contact sensors, and seat sensors.

## Dataset Description

- **Data Files**: 11 Excel files containing sensor readings
- **Total Records**: 14,447 data points
- **Time Range**: July 11-13, 2024
- **Features**: 24 columns including 21 sensor values
- **Activities**: 39 different activity types
- **Locations**: 15 different locations

### Sensor Types

| Category | Count | Examples |
|----------|-------|----------|
| Motion Sensors | 6 | Kitchen, Bedroom, Corridor, Dining, Sofa, Bathroom |
| Door Sensors | 6 | Bathroom door, Bedroom door, Fridge door, etc. |
| Drawer Sensors | 2 | Floor cupboard drawers |
| Contact Sensors | 2 | Bed contact, Toilet Lid |
| Seat Sensors | 5 | Sofa Seatplace 0-4 |

### Main Activities

- Working (42.8%)
- Resting (11.1%)
- Toiletting (7.1%)
- Having lunch (5.8%)
- Cooking (5.2%)
- And 34 more activity types...

## Project Structure

```
.
├── data/                    # Sensor data files
├── data_backup/             # Backup of original data
├── data_analysis/           # Analysis scripts and reports
│   ├── clean_sensor_columns.py
│   ├── data_analysis.py
│   └── data_statistics_report.txt
├── visualization/           # Visualization scripts
│   ├── data_visualization_v0.py
│   ├── data_visualization_v1.py
│   ├── data_visualization_v2.py
│   └── data_visualization_v3.py
└── pics/                    # Generated visualizations
```

## Requirements

```
pandas
numpy
matplotlib
seaborn
openpyxl
```

## Usage

1. **Data Cleaning**:
   ```bash
   python data_analysis/clean_sensor_columns.py
   ```

2. **Data Analysis**:
   ```bash
   python data_analysis/data_analysis.py
   ```

3. **Generate Visualizations**:
   ```bash
   python visualization/data_visualization_v0.py
   ```

## License

This project is for academic research purposes.

## Citation

If you use this dataset or code, please cite our ICSR 2026 paper (forthcoming).
