/*
 * array_access.cpp
 * Benchmark Program for Cache Associativity Evaluation
 * 
 * This program generates memory access patterns that stress the cache
 * with different behaviors to reveal the impact of cache associativity:
 *   1. Sequential Access  - Good spatial locality
 *   2. Stride Access      - Stresses specific cache sets
 *   3. Conflict Access    - Creates conflict misses in low-associativity caches
 *
 * Compile: g++ -O1 -static -o array_access array_access.cpp
 */

#include <iostream>
using namespace std;

int main()
{
    const int SIZE = 100000;     // Array size
    const int REPEAT = 100;      // Number of repetitions
    int *arr = new int[SIZE];

    // ====== Phase 1: Initialize array ======
    for (int i = 0; i < SIZE; i++)
        arr[i] = i;

    long long sum = 0;

    // ====== Phase 2: Sequential Access ======
    // Tests spatial locality - all associativities should perform similarly
    for (int r = 0; r < REPEAT; r++)
    {
        for (int i = 0; i < SIZE; i++)
        {
            sum += arr[i];
        }
    }

    // ====== Phase 3: Stride Access ======
    // Stride = 16 elements = 64 bytes (1 cache line)
    // This creates pressure on specific cache sets
    for (int r = 0; r < REPEAT; r++)
    {
        for (int i = 0; i < SIZE; i += 16)
        {
            sum += arr[i];
        }
    }

    // ====== Phase 4: Conflict-Inducing Access ======
    // Access elements that map to the same cache set
    // For 32kB cache with 64B lines = 512 sets
    // Stride of 512 * 16 = 8192 elements maps to same set
    // Direct-mapped (1-way) will suffer heavy conflict misses
    // Higher associativity will handle this better
    const int CONFLICT_STRIDE = 8192;
    for (int r = 0; r < REPEAT * 2; r++)
    {
        for (int i = 0; i < SIZE; i += CONFLICT_STRIDE)
        {
            sum += arr[i];
        }
    }

    cout << "Sum = " << sum << endl;

    delete[] arr;
    return 0;
}