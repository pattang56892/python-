#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ninapro Database Hand Gesture Recognition Training Script
"""

import os
import sys
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 禁用oneDNN自定义操作以减少日志输出
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 设置数据路径
DATA_PATH = r'E:/test/Ninapro_DB1_npz'

# 确保文件存在并且正确权限
def check_file_permissions(file_path):
    """检查文件权限并尝试修复"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 检查文件权限
        if not os.access(file_path, os.R_OK):
            print(f"尝试修复文件权限: {file_path}")
            # Windows上修改权限
            if os.name == 'nt':
                import win32api
                import win32security
                import ntsecuritycon as con
                
                # Get file security
                sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
                dacl = sd.GetSecurityDescriptorDacl()
                
                # Add read permission for current user
                user, domain, type = win32security.LookupAccountName("", win32api.GetUserName())
                dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_GENERIC_READ, user)
                
                # Set the new DACL
                sd.SetSecurityDescriptorDacl(1, dacl, 0)
                win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)
                
        return True
    except Exception as e:
        print(f"权限检查失败: {e}")
        return False

def load_data(data_path):
    """Load Ninapro database from npz files"""
    try:
        check_file_permissions(data_path)
        
        # Load the compressed numpy data
        data = np.load(data_path)
        
        # Extract EMG signals and labels
        X = data['emg_signals']  # EMG sensor data
        y = data['gestures']     # Gesture labels
        subjects = data['subjects']  # Subject IDs
        
        print(f"Data loaded successfully:")
        print(f"  EMG signals shape: {X.shape}")
        print(f"  Gesture labels shape: {y.shape}")
        print(f"  Number of subjects: {len(np.unique(subjects))}")
        print(f"  Number of gesture classes: {len(np.unique(y))}")
        
        return X, y, subjects
        
    except Exception as e:
        print(f"数据加载失败: {e}")
        raise

def preprocess_data(X, y):
    """Preprocess EMG signals"""
    # Normalize EMG signals
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
    
    # Convert labels to categorical
    num_classes = len(np.unique(y))
    y_categorical = tf.keras.utils.to_categorical(y, num_classes)
    
    return X_scaled, y_categorical, scaler

def create_model(input_shape, num_classes):
    """Create CNN model for gesture recognition"""
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        
        # Convolutional layers for feature extraction
        tf.keras.layers.Conv1D(64, 3, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling1D(2),
        tf.keras.layers.Dropout(0.2),
        
        tf.keras.layers.Conv1D(128, 3, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling1D(2),
        tf.keras.layers.Dropout(0.2),
        
        tf.keras.layers.Conv1D(256, 3, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.GlobalAveragePooling1D(),
        
        # Dense layers for classification
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_model(model, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
    """Train the gesture recognition model"""
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )
    
    # Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=8,
            min_lr=1e-7
        ),
        tf.keras.callbacks.ModelCheckpoint(
            'best_gesture_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    return history

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    test_loss, test_accuracy, test_top_k = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\nModel Evaluation Results:")
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Top-K Accuracy: {test_top_k:.4f}")
    
    return test_accuracy

def main():
    """Main training pipeline"""
    print("=== Ninapro Hand Gesture Recognition Training ===")
    
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    try:
        # Load data
        print("Loading Ninapro database...")
        X, y, subjects = load_data(DATA_PATH)
        
        # Preprocess data
        print("Preprocessing data...")
        X_processed, y_processed, scaler = preprocess_data(X, y)
        
        # Split data (subject-independent split)
        unique_subjects = np.unique(subjects)
        train_subjects, test_subjects = train_test_split(
            unique_subjects, test_size=0.2, random_state=42
        )
        
        train_mask = np.isin(subjects, train_subjects)
        test_mask = np.isin(subjects, test_subjects)
        
        X_train_full, y_train_full = X_processed[train_mask], y_processed[train_mask]
        X_test, y_test = X_processed[test_mask], y_processed[test_mask]
        
        # Further split training data for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_full, y_train_full, test_size=0.2, random_state=42
        )
        
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Validation set: {X_val.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # Create model
        print("Creating model...")
        input_shape = X_train.shape[1:]
        num_classes = y_train.shape[1]
        model = create_model(input_shape, num_classes)
        
        print(f"Model input shape: {input_shape}")
        print(f"Number of classes: {num_classes}")
        model.summary()
        
        # Train model
        print("Starting training...")
        history = train_model(model, X_train, y_train, X_val, y_val)
        
        # Evaluate model
        print("Evaluating model...")
        test_accuracy = evaluate_model(model, X_test, y_test)
        
        # Save final model and scaler
        model.save('final_gesture_model.h5')
        np.save('scaler.npy', scaler.scale_)
        
        print(f"\nTraining completed successfully!")
        print(f"Final test accuracy: {test_accuracy:.4f}")
        
    except Exception as e:
        print(f"Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()