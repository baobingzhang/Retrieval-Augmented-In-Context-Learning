# Retrieval-Augmented In-Context Learning for Continuous Indoor Localization

**Abstract**—Indoor human localization is a critical measurand in smart homes and service robotics, yet ambient-sensor streams are characterized by **long-horizon non-stationary distribution shifts**, asynchronous sampling, and inherent sparsity. Under such conditions, tabular foundation inference becomes highly sensitive to context quality and prone to instability under strict deployment budgets. This paper investigates the **real-world** Robot House multi-sensor environment and proposes a hybrid retrieval-augmented tabular foundation inference framework, framed through the lens of **Bayesian Meta-Learning**. Under a fixed context budget, we perform structured context optimization to fortify the model's context-driven inference mechanism. Specifically, we introduce a **dual-stream** temporal-anchor–semantic-retrieval approach: the temporal anchor retains recent sequences to capture local dynamics, while semantic retrieval performs stochastic neighbor search within a **differentiable manifold** learned by Neighborhood Components Analysis (NCA) to **recall long-tail sparse events**. Experiments demonstrate that the proposed framework consistently outperforms temporal-only and semantic-only baselines **(achieving SOTA performance)**. Ablation studies further reveal that naive Euclidean retrieval in the original feature space leads to **catastrophic degradation**, underscoring the necessity of **task-specific metric learning** for retrieval-augmented in-context learning. Overall, the framework enables practical, privacy-preserving, and deployable indoor localization with **superior robustness** under noisy and incomplete sensing conditions.

---

## Repository Structure

This repository contains the minimal code required to reproduce the core results of the paper.

- `run_localization_hybrid.py`: The main script implementing the Hybrid (NCA + Temporal) Retrieval TabPFN strategy.
- `requirements.txt`: Python dependencies.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1.  Place your dataset files (`.xlsx` format) in a folder named `data/` in the root directory.
    - Format expectation: Columns should contain sensor values (e.g., `feature_1_value`) and a target column `Location`.
2.  Run the framework:

```bash
python run_localization_hybrid.py
```

## Citation

If you use this code in your research, please cite our paper:

```bibtex
@article{zhang2026retrieval,
  title={Retrieval-Augmented In-Context Learning for Continuous Indoor Localization},
  author={Zhang, Baobing and et al.},
  journal={IEEE Internet of Things Journal (Submitted)},
  year={2026}
}
```

## License

MIT License.
