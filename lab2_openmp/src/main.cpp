#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <iomanip>
#include <omp.h>

using namespace std;

int main(int argc, char* argv[]) {
    system("chcp 1251 > nul");
    setlocale(LC_ALL, "Russian");

    int m = 200;
    int num_threads = 4;

    if (argc > 1) m = atoi(argv[1]);
    if (argc > 2) num_threads = atoi(argv[2]);

    omp_set_num_threads(num_threads);

    ifstream file1("input/matrix_a.txt");
    if (!file1.is_open()) return 1;
    int size_a; file1 >> size_a;
    vector<vector<double>> A(m, vector<double>(m));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < m; j++)
            file1 >> A[i][j];
    file1.close();

    ifstream file2("input/matrix_b.txt");
    if (!file2.is_open()) return 1;
    int size_b; file2 >> size_b;
    vector<vector<double>> B(m, vector<double>(m));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < m; j++)
            file2 >> B[i][j];
    file2.close();

    vector<vector<double>> C(m, vector<double>(m, 0.0));

    auto start = chrono::high_resolution_clock::now();
    
    #pragma omp parallel for shared(A, B, C)
    for (int i = 0; i < m; i++) {
        for (int k = 0; k < m; k++) {
            double temp = A[i][k];
            for (int j = 0; j < m; j++) {
                C[i][j] += temp * B[k][j];
            }
        }
    }
    
    auto end = chrono::high_resolution_clock::now();
    double time_sec = chrono::duration<double>(end - start).count();

    ofstream out("output/result.txt");
    if (out.is_open()) {
        out << m << endl;
        out << setprecision(15);
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) out << C[i][j] << " ";
            out << endl;
        }
        out.close();
    }

    ofstream info("output/info.txt");
    if (info.is_open()) {
        info << "Execution time: " << time_sec << " sec" << endl;
        info << "Task volume (Data): " << (m * m * 3) << " elements" << endl;
        info.close();
    }

    cout << "Time: " << time_sec << endl;
}
