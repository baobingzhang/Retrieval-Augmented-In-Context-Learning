# Manifold-Aligned In-Context Learning: Hybrid Retrieval-Augmented Tabular Foundation Models for Ambient Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Paper](https://img.shields.io/badge/Paper-IEEE%20IoT--J%20(Submitted)-red)](https://github.com/baobingzhang/Retrieval-Augmented-In-Context-Learning)

> Official PyTorch implementation of the paper **"Manifold-Aligned In-Context Learning: Hybrid Retrieval-Augmented Tabular Foundation Models for Ambient Intelligence"**.

## 🚀 Introduction

In the era of **Active Ambient Intelligence (AmI)** and **Service Robotics**, traditional localization methods struggle with **non-stationary distribution shifts** and **long-tail sparse events** across heterogeneous sensor networks.

This project introduces a **Manifold-Aligned Tabular Foundation Model** that bridges the gap between pre-trained priors and local deployment dynamics. By framing localization as a **Bayesian Meta-Learning** problem, our framework aligns the retrieval space with the task manifold to maximize context relevance.

### Key Features
*   **🧠 Manifold-Aligned Retrieval**: Uses **Neighborhood Components Analysis (NCA)** to learn a differentiable metric space that clusters semantically similar states, preventing "metric collapse" in high-dimensional spaces.
*   **🎯 Hybrid Context Contextualization**:
    *   **⚓ Temporal Anchor**: Preserves local physical continuity.
    *   **✨ Semantic Spark**: Recalls diverse, long-tail historical events via manifold-aligned search.
*   **⚡ SOTA Performance**: Verified on the real-world **Robot House** dataset, outperforming BiLSTM，Random Forest and modern Deep Learning baselines.
*   **🔒 Privacy-Preserving**: Operates purely on ambient binary sensors (PIR/Door), ensuring zero visual intrusion.

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
@article{zhang2026manifold,
  title={Manifold-Aligned In-Context Learning: Hybrid Retrieval-Augmented Tabular Foundation Models for Ambient Intelligence},
  author={Zhang, Baobing and et al.},
  journal={IEEE Internet of Things Journal (Submitted)},
  year={2026}
}
```


## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
