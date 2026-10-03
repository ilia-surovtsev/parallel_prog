import os
import numpy as np

def generate_and_save_matrices(size, base_path="lab1/input"):
    os.makedirs(base_path, exist_ok=True)
    A = np.random.rand(size, size) * 10
    B = np.random.rand(size, size) * 10
    np.savetxt(f"{base_path}/matrix_a.txt", A, fmt="%.14f", header=str(size), comments='')
    np.savetxt(f"{base_path}/matrix_b.txt", B, fmt="%.14f", header=str(size), comments='')
