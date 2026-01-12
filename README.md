# Retrieval-Augmented In-Context Learning (RA-ICL)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Paper](https://img.shields.io/badge/Paper-IEEE%20IoT--J%20(Submitted)-red)](https://github.com/baobingzhang/Retrieval-Augmented-In-Context-Learning)

> Official PyTorch implementation of the paper **"Retrieval-Augmented In-Context Learning for Continuous Indoor Localization"**.

## 🚀 Introduction

In the era of **Smart Homes** and **Service Robotics**, traditional localization methods struggle with **non-stationary distribution shifts** and **long-tail sparse events** (e.g., infrequent but critical room transitions).

This project introduces a **Hybrid Retrieval-Augmented Tabular Foundation Model** that solves these challenges without retraining. By treating localization as a **Bayesian Meta-Learning** problem, our framework dynamically retrieves the most relevant historical context to guide inference.

### Key Features
*   **🧠 Bayesian Meta-Learning**: Leverages TabPFN's pre-trained priors for ultra-robust few-shot inference.
*   **🎯 Hybrid Retrieval Strategy**:
    *   **Temporal Anchor**: Captures local physical continuity.
    *   **Semantic Spark**: Recalls long-tail events via a learned **Differentiable Manifold (NCA)**.
*   **⚡ SOTA Performance**: Verified on the real-world **Robot House** dataset, significantly outperforming LSTM and Random Forest baselines.
*   **🔒 Privacy-Preserving**: No camera images required—purely based on ambient binary sensors.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/baobingzhang/Retrieval-Augmented-In-Context-Learning.git
cd Retrieval-Augmented-In-Context-Learning

# Install dependencies
pip install -r requirements.txt
```

## ⚡ Quick Start

1.  **Prepare Data**: Place your sensor data (`.xlsx`) in the `data/` folder.
    *   *Note: Data should have sensor columns and a 'Location' target column.*
2.  **Run Inference**:

    ```bash
    python run_localization_hybrid.py
    ```

3.  **View Results**: Performance metrics will be saved to `results.txt`.

## 📂 Project Structure

```
.
├── run_localization_hybrid.py   # Main entry point (Hybrid Retrieval Strategy)
├── requirements.txt             # Dependency definitions
├── LICENSE                      # MIT License
└── README.md                    # Project documentation
```

## 🔗 Citation

If you find this code useful, please cite our work:

```bibtex
@article{zhang2026retrieval,
  title={Retrieval-Augmented In-Context Learning for Continuous Indoor Localization},
  author={Zhang, Baobing and et al.},
  journal={IEEE Internet of Things Journal (Submitted)},
  year={2026}
}
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
