"""
Retrieval-Augmented In-Context Learning for Continuous Indoor Localization.
Main execution script for the Hybrid (Temporal + NCA) Strategy.
"""

import pandas as pd
import numpy as np
import os
import sys
import time
import gc
from tqdm import tqdm
import warnings

# Sklearn imports
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import accuracy_score, f1_score, classification_report, precision_score, recall_score, balanced_accuracy_score, matthews_corrcoef
from sklearn.neighbors import NearestNeighbors, NeighborhoodComponentsAnalysis

# Force TabPFN v2 (Ungated)
os.environ["TABPFN_MODEL_VERSION"] = "v2"
warnings.filterwarnings('ignore')

try:
    import torch
    # Use official package instead of local lib
    from tabpfn import TabPFNClassifier
    print("✅ TabPFN Library Loaded")
except ImportError:
    print("❌ TabPFN not found. Please run: pip install -r requirements.txt")
    sys.exit(1)

# ==========================================
# ⚙️ Configuration
# ==========================================
DATA_DIR = 'data'  # Place your Excel files here
WINDOW_SIZE = 10
RANDOM_SEED = 42
TARGET_COL = 'Location'
OUTPUT_FILE = 'results.txt'

# 🏆 Hybrid Strategy Hyperparameters
RETRIEVAL_K = 2048         # Total Context Size (Training Budget)
TEMPORAL_RATIO = 0.5       # 50% Anchor (Stability) + 50% Spark (Innovation)
NCA_COMPONENTS = 16        # Dimension of learned metric space
BATCH_SIZE = 50            # Batch size for inference loop

# ==========================================
# 1. Data Pipeline
# ==========================================
def load_and_preprocess():
    print(f"\\n📂 Loading data from {DATA_DIR}...")
    if not os.path.exists(DATA_DIR):
        print(f"❌ Data folder '{DATA_DIR}' missing. Please create it and add .xlsx files.")
        return None, None, None
        
    # Load all Excel files
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.xlsx')])
    dfs = []
    if not files:
        print("❌ No .xlsx files found in data folder.")
        return None, None, None

    for f in tqdm(files, desc="Reading Files"):
        try:
            dfs.append(pd.read_excel(os.path.join(DATA_DIR, f), engine='openpyxl'))
        except: pass
    
    if not dfs: return None, None, None
    df_merged = pd.concat(dfs, ignore_index=True)
    
    # Identify Columns
    target_candidates = [c for c in df_merged.columns if str(c).lower() == TARGET_COL.lower()]
    if not target_candidates: 
        print(f"❌ Target column '{TARGET_COL}' not found.")
        return None, None, None
    target_col = target_candidates[0]
    feature_cols = [c for c in df_merged.columns if c != target_col and 'value' in str(c)]
    
    df_clean = df_merged[feature_cols + [target_col]].dropna()
    
    # 🌟 Label Cleaning (Consistency is Key)
    def clean_labels(val):
        s = str(val).lower().strip()
        if 'transition' in s: return 'Transition'
        if 'bath' in s: return 'Bathroom'
        if 'bed' in s: return 'Bedroom'
        if 'kitchen' in s: return 'Kitchen'
        if 'sofa' in s or 'dining' in s: return 'Living/Dining'
        if 'office' in s: return 'Office'
        if 'door' in s: return 'Door'
        return 'Other'

    df_clean[target_col] = df_clean[target_col].apply(clean_labels)
    
    # Encode & Scale
    le = LabelEncoder()
    y_raw = le.fit_transform(df_clean[target_col].astype(str))
    
    scaler = MinMaxScaler()
    X_raw = scaler.fit_transform(df_clean[feature_cols].values)
    
    return X_raw, y_raw, le

def create_sliding_windows(X, y):
    Xs, ys = [], []
    for i in range(len(X) - WINDOW_SIZE):
        Xs.append(X[i : i+WINDOW_SIZE])
        ys.append(y[i+WINDOW_SIZE]) # Predict the NEXT step
    return np.array(Xs), np.array(ys)

# ==========================================
# 2. 🧠 Hybrid Temporal-Contrastive Logic
# ==========================================
def main():
    print(f"🚀 Running Final Hybrid Script (ICSR 2026 -> IEEE IoT-J)")
    print(f"   Strategy: 50% Temporal Anchor + 50% NCA Contrastive Retrieval")
    
    # A. Prepare Data
    X_raw, y_raw, le = load_and_preprocess()
    if X_raw is None: return
    
    print("🪟 Creating Windows...")
    X_3d, y_seq = create_sliding_windows(X_raw, y_raw)
    
    # Flatten for TabPFN (N, T*F)
    X_flat = X_3d.reshape(len(X_3d), -1)
    
    # Split 80/20
    split_idx = int(len(X_flat) * 0.8)
    X_train, X_test = X_flat[:split_idx], X_flat[split_idx:]
    y_train, y_test = y_seq[:split_idx], y_seq[split_idx:]
    
    print(f"   Train Bank: {len(X_train)}")
    print(f"   Test Query: {len(X_test)}")
    
    # B. Phase 1: Train Metric Learner (NCA)
    print(f"\\n🔍 [Setup] Learning Manifold Metric (NCA/Metric Learning)...")
    st = time.time()
    
    # Subsample for NCA training if dataset is huge (optional, here 6k is fine)
    nca = NeighborhoodComponentsAnalysis(n_components=NCA_COMPONENTS, random_state=RANDOM_SEED)
    nca.fit(X_train, y_train)
    
    # Project Training Data to Learned Space
    X_train_nca = nca.transform(X_train)
    
    # Build Semantic Index
    knn_semantic = NearestNeighbors(n_neighbors=int(RETRIEVAL_K * (1-TEMPORAL_RATIO)), metric='euclidean', n_jobs=-1)
    knn_semantic.fit(X_train_nca)
    
    print(f"   -> NCA Training Done ({time.time()-st:.1f}s)")

    # C. Phase 2: Hybrid Inference Loop
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    classifier = TabPFNClassifier(device=device, n_estimators=32)
    
    print(f"\\n🏎️  Starting Inference Loop (Batch Size={BATCH_SIZE})...")
    y_preds = []
    
    # Compute Temporal Context Indices ONCE (The "Anchor")
    n_temporal = int(RETRIEVAL_K * TEMPORAL_RATIO)
    temporal_indices = np.arange(len(X_train) - n_temporal, len(X_train))
    
    num_batches = int(np.ceil(len(X_test) / BATCH_SIZE))
    
    t_start_inf = time.time()
    for b in tqdm(range(num_batches), desc="Hybrid Predicting"):
        start = b * BATCH_SIZE
        end = min((b + 1) * BATCH_SIZE, len(X_test))
        
        X_batch_flat = X_test[start:end]
        
        # 1. Semantic Retrieval (The "Spark")
        # Project Batch to NCA Space
        X_batch_nca = nca.transform(X_batch_flat)
        
        # We need a representative query for the batch context.
        # Strategy: Use the Mean of the batch in projected space.
        batch_center = np.mean(X_batch_nca, axis=0).reshape(1, -1)
        
        # Retrieve KNN
        _, semantic_indices = knn_semantic.kneighbors(batch_center)
        semantic_indices = semantic_indices[0] # Flatten
        
        # 2. Merge Contexts
        # Union of indices (Time Anchor + Semantic Spark) via np.unique
        combined_indices = np.unique(np.concatenate([temporal_indices, semantic_indices]))
        
        # If union exceeds budget, trim
        if len(combined_indices) > RETRIEVAL_K:
            # Sort to maintain some order, then take last K (bias towards recent)
            combined_indices.sort() 
            combined_indices = combined_indices[-RETRIEVAL_K:]
            
        X_ctx = X_train[combined_indices]
        y_ctx = y_train[combined_indices]
        
        # 3. Predict
        classifier.fit(X_ctx, y_ctx)
        preds = classifier.predict(X_batch_flat)
        y_preds.extend(preds)
        
        # Cleanup
        if b % 10 == 0:
            gc.collect()
            if device=='cuda': torch.cuda.empty_cache()

    dur_inf = time.time() - t_start_inf
    
    # D. Results
    acc = accuracy_score(y_test, y_preds)
    f1_w = f1_score(y_test, y_preds, average='weighted')
    f1_m = f1_score(y_test, y_preds, average='macro')
    prec_w = precision_score(y_test, y_preds, average='weighted', zero_division=0)
    rec_w = recall_score(y_test, y_preds, average='weighted', zero_division=0)
    rec_m = recall_score(y_test, y_preds, average='macro', zero_division=0)
    bal_acc = balanced_accuracy_score(y_test, y_preds)
    mcc = matthews_corrcoef(y_test, y_preds)
    
    print(f"\\n🏆 Final Hybrid Results:")
    print(f"Accuracy:      {acc:.4f}")
    print(f"F1-Weighted:   {f1_w:.4f}")
    print(f"F1-Macro:      {f1_m:.4f}")
    print(f"Prec-Weighted: {prec_w:.4f}")
    print(f"Rec-Weighted:  {rec_w:.4f}")
    print(f"Rec-Macro:     {rec_m:.4f}")
    print(f"Balanced Acc:  {bal_acc:.4f}")
    print(f"MCC:           {mcc:.4f}")
    print(f"Time:          {dur_inf:.1f}s")
    
    # Classification Report
    try:
        class_names = [str(c) for c in le.classes_]
        rpt = classification_report(y_test, y_preds, target_names=class_names, labels=range(len(class_names)))
    except:
        rpt = classification_report(y_test, y_preds)
        
    print(rpt)
    
    with open(OUTPUT_FILE, "w") as f:
        f.write("IEEE IoT-J Consideration - Final Hybrid Strategy Results\\n")
        f.write("========================================================\\n")
        f.write(f"Accuracy:        {acc:.4f}\\n")
        f.write(f"F1-Weighted:     {f1_w:.4f}\\n")
        f.write(f"F1-Macro:        {f1_m:.4f}\\n")
        f.write(f"Precision-W:     {prec_w:.4f}\\n")
        f.write(f"Recall-Weighted: {rec_w:.4f}\\n")
        f.write(f"Recall-Macro:    {rec_m:.4f}\\n")
        f.write(f"Balanced Acc:    {bal_acc:.4f}\\n")
        f.write(f"MCC:             {mcc:.4f}\\n\\n")
        f.write("\\nDetailed Report:\\n")
        f.write(rpt)
        
    print(f"\\n📄 Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
