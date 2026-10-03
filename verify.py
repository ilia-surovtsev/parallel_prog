import os
import numpy as np

def load_matrix(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        lines = f.readlines()
    size = int(lines[0].strip())
    matrix_data = [[float(x) for x in line.split()] for line in lines[1:] if line.strip()]
    return np.array(matrix_data)

def verify_results(input_dir="lab1/input", output_dir="lab1/output"):
    A = load_matrix(os.path.join(input_dir, "matrix_a.txt"))
    B = load_matrix(os.path.join(input_dir, "matrix_b.txt"))
    C_cpp = load_matrix(os.path.join(output_dir, "result.txt"))
    
    if A is None or B is None or C_cpp is None:
        print("Ошибка верификации: отсутствуют файлы матриц.")
        return False
        
    C_expected = np.dot(A, B)
    if np.allclose(C_cpp, C_expected, rtol=1e-5, atol=1e-5):
        print("Верификация успешна! Результаты C++ совпадают с NumPy.")
        return True
    else:
        print(f"ОШИБКА! Максимальное расхождение: {np.max(np.abs(C_cpp - C_expected))}")
        return False
