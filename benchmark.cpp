#include <iostream>
#include <vector>
#include <cmath>
#include <cstdint>

float poly_step(float a, float b, float c) {
    return (a * b + c) * 0.99999f + (a - b) * 0.00001f;
}

__attribute__((noinline))
void compute_polynomial(float* __restrict a, const float* __restrict b, const float* __restrict c, size_t n) {
    for (size_t i = 0; i < n; ++i) {
        a[i] = poly_step(a[i], b[i], c[i]);
    }
}

__attribute__((noinline))
float conditional_filter(const float* __restrict a, const float* __restrict b, size_t n, float threshold) {
    float sum = 0.0f;
    for (size_t i = 0; i < n; ++i) {
        if (a[i] > threshold) {
            sum += a[i] * b[i];
        } else {
            sum -= b[i] * 0.5f;
        }
    }
    return sum;
}

__attribute__((noinline))
float run_workload(size_t n, int iterations) {
    std::vector<float> a(n, 1.1f);
    std::vector<float> b(n, 2.2f);
    std::vector<float> c(n, 0.5f);

    for (size_t i = 0; i < n; ++i) {
        a[i] = static_cast<float>(i % 100) * 0.02f;
        b[i] = static_cast<float>((i + 37) % 100) * 0.01f;
    }

    float total_sum = 0.0f;
    for (int iter = 0; iter < iterations; ++iter) {
        compute_polynomial(a.data(), b.data(), c.data(), n);
        total_sum += conditional_filter(a.data(), b.data(), n, 1.0f);

        asm volatile("" : "+m"(a[0]), "+r"(total_sum) : : "memory");
    }
    return total_sum;
}

int main() {
    const size_t N = 65536;
    const int ITERATIONS = 15000;

    std::cout << "Starting benchmark..." << std::endl;
    float result = run_workload(N, ITERATIONS);
    std::cout << "Done. Checksum: " << result << std::endl;
    return 0;
}
