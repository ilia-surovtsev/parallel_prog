#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

using namespace std;

int main() {
    system("chcp 1251 > nul");
    setlocale(LC_ALL, "Russian");

    ifstream file1("input/matrix_a.txt");
    if (!file1.is_open()) {
        cerr << "Ошибка: Не удалось открыть файл input/matrix_a.txt!" << endl;
        return 1;
    }

    int m = 0;
    file1 >> m;
    
    vector<vector<double>> A(m, vector<double>(m));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            file1 >> A[i][j];
        }
    }
    file1.close();

    ifstream file2("input/matrix_b.txt");
    if (!file2.is_open()) {
        cerr << "Ошибка: Не удалось открыть файл input/matrix_b.txt!" << endl;
        return 1;
    }

    int n = 0;
    file2 >> n;
    
    vector<vector<double>> B(n, vector<double>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            file2 >> B[i][j];
        }
    }
    file2.close();

    if (m != n) {
        cerr << "Ошибка: Матрицы должны быть одинакового размера!" << endl;
        return 1;
    }

    cout << "Size matrix A: " << m << "x" << m << endl;
    cout << "Size matrix B: " << n << "x" << n << endl;

    vector<vector<double>> C(m, vector<double>(n, 0.0));

    auto start = chrono::high_resolution_clock::now();
    
    for (int i = 0; i < m; i++) {
        for (int k = 0; k < m; k++) {
            double temp = A[i][k];
            for (int j = 0; j < n; j++) {
                C[i][j] += temp * B[k][j];
            }
        }
    }
    
    auto end = chrono::high_resolution_clock::now();
    double time_sec = chrono::duration<double>(end - start).count();
    
    cout << "mult is comleted :)" << endl;
    cout << "Size matrix C: " << m << "x" << n << endl;
    cout << "time: " << time_sec << " sec" << endl;

    int total_elements = (m * m) + (n * n) + (m * n);  
    long long total_flops = 2LL * m * n * m; 
    cout << "Volume: " << total_elements << " elements" << endl;
    cout << endl;

    ofstream out("output/result.txt");
    if (!out.is_open()) {
        cerr << "Ошибка: Не удалось создать файл output/result.txt!" << endl;
        return 1;
    }
    
    out << m << endl;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            out << C[i][j] << " ";
        }
        out << endl;
    }
    out.close();

    ofstream info("output/info.txt");
    if (info.is_open()) {
        info << "=== Matrix Multiplication Info ===" << endl;
        info << "Matrix A size: " << m << "x" << m << endl;
        info << "Matrix B size: " << n << "x" << n << endl;
        info << "Matrix C size: " << m << "x" << n << endl;
        info << "Execution time: " << time_sec << " sec" << endl;
        info << "Task volume (Data): " << total_elements << " elements" << endl;
        info << "Task volume (Ops): " << total_flops << " FLOP" << endl;
        info.close();
    }

    cout << "Info saved to output/info.txt" << endl;
    cout << "The work has been completed!" << endl;
}
