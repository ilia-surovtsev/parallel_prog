import os
import numpy as np

def generate_and_save_matrices(size, base_path="lab1/input"):
    os.makedirs(base_path, exist_ok=True)
    matrix_a = np.random.rand(size, size) * 10
    matrix_b = np.random.rand(size, size) * 10
    
    with open(os.path.join(base_path, "matrix_a.txt"), "w") as f:
        f.write(f"{size}\n")
        np.savetxt(f, matrix_a, fmt="%.6f")
        
    with open(os.path.join(base_path, "matrix_b.txt"), "w") as f:
        f.write(f"{size}\n")
        np.savetxt(f, matrix_b, fmt="%.6f")
