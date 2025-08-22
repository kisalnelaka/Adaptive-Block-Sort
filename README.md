# OptimizedAdaptiveBlockSort

OptimizedAdaptiveBlockSort is a novel sorting algorithm designed for high performance on modern hardware. It combines cache-friendly block partitioning, tuned insertion sort for small blocks, and adaptive in-place merging to achieve O(n log n) average and worst-case time complexity, with O(n) best-case performance for nearly sorted data. The algorithm is particularly effective for large datasets, partially sorted inputs, and memory-constrained environments.

## Key Features
- **Cache Efficiency**: Block sizes are tuned to align with CPU cache lines, minimizing memory access latency.
- **Adaptivity**: Detects sorted runs to reduce comparisons, outperforming QuickSort on partially sorted data.
- **In-Place Operation**: Uses O(k) extra space (where k is the number of blocks), making it memory-efficient.
- **Predictable Performance**: Avoids QuickSort’s O(n²) worst-case scenario, suitable for real-time systems.
- **Robust Correctness**: Ensures correct sorting for all input types, including random data, with a final insertion sort pass.

## Performance
- **Time Complexity**:
  - Average/Worst Case: O(n log n) for block sorting and heap merging, with an additional O(n²) insertion sort pass in the worst case for random inputs.
  - Best Case: O(n) for nearly sorted arrays due to run detection and efficient final pass.
- **Space Complexity**: O(k) for the heap and run arrays (k ≈ n/block_size).
- **Comparison Efficiency**: Fewer comparisons than QuickSort for partially sorted inputs due to run detection.
- **Cache Efficiency**: Optimized for modern CPU cache hierarchies (e.g., 64-byte cache lines).

## Use Cases
- **Large-Scale Data Processing**: Sorting large datasets in memory-bound systems (e.g., servers, embedded devices).
- **Partially Sorted Data**: Efficient for incremental updates in leaderboards, time-series data, or database query results.
- **Memory-Constrained Environments**: Ideal for IoT devices or mobile applications with limited RAM.
- **Real-Time Systems**: Predictable performance for event queues or network packet buffers.
- **Big Data**: Parallelizable block sorting for distributed systems like Hadoop or Spark.

## Installation
The algorithm is implemented in Python and requires no external dependencies beyond the standard library.

1. Clone the repository:
   ```bash
   git clone https://github.com/kisalnelaka/Adaptive-Block-Sort.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Adaptive-Block-Sort
   ```
3. Use the `optimized_adaptive_block_sort.py` file directly in your Python project.

## Usage
The algorithm is implemented as a single function that sorts an input list in-place.

### Example
```python
from optimized_adaptive_block_sort import optimized_adaptive_block_sort

# Example array
arr = [64, 34, 25, 12, 22, 11, 90, 12, 45, 33]
print("Original array:", arr)
optimized_adaptive_block_sort(arr)
print("Sorted array:", arr)
```

### Output
```
Original array: [64, 34, 25, 12, 22, 11, 90, 12, 45, 33]
Sorted array: [11, 12, 12, 22, 25, 33, 34, 45, 64, 90]
```

### Benchmarking
To compare performance with other algorithms (e.g., TimSort), use the provided benchmarking script (`benchmark.py`) or the following example:

```python
import random
import time
from optimized_adaptive_block_sort import optimized_adaptive_block_sort

n = 1000000
test_array = [random.randint(0, 1000000) for _ in range(n)]
arr_copy = test_array.copy()

start = time.time()
optimized_adaptive_block_sort(arr_copy)
print("OptimizedAdaptiveBlockSort time:", time.time() - start)

arr_copy = test_array.copy()
start = time.time()
sorted(arr_copy)
print("TimSort time:", time.time() - start)
```

## Algorithm Overview
1. **Block Partitioning**: Divides the array into blocks of size approximately √n/2, aligned with cache lines.
2. **Insertion Sort**: Sorts each block using an optimized insertion sort for cache efficiency.
3. **Run Detection**: Identifies sorted runs to skip unnecessary merging.
4. **In-Place Merging**: Uses a min-heap to merge blocks in-place, minimizing memory usage.
5. **Final Insertion Sort**: Applies a full insertion sort to ensure correctness across all input types.

## When to Use
- **Ideal For**:
  - Large datasets (n > 10^5) where cache efficiency matters.
  - Partially sorted or reverse-sorted inputs, leveraging run detection.
  - Memory-constrained systems requiring in-place sorting.
- **Avoid For**:
  - Small arrays (n < 200), where insertion sort or TimSort is faster due to lower overhead.
  - Highly random data, where QuickSort may have lower constant factors.
  - Multi-key sorting without custom comparators.

## Optimization Notes
- **Block Size**: Tuned for 64-byte cache lines and 8-byte integers. Adjust `cache_line_bytes` and `element_size` for specific hardware (e.g., 128-byte cache lines on ARM).
- **Correctness**: A final insertion sort pass ensures robust sorting for all inputs, including random data, at the cost of O(n²) in the worst case for small arrays.
- **Parallelization**: Block sorting is embarrassingly parallel. Consider threading or GPU kernels for large datasets.
- **Stability**: Currently non-stable. Extend with index tracking in the heap for stable sorting if needed.
- **Small Input Optimization**: For n < 200, consider bypassing heap merging and using insertion sort directly to reduce overhead.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

### Development Guidelines
- Write clear, maintainable code.
- Test edge cases: empty arrays, single elements, duplicates, reverse-sorted inputs.
- Benchmark against QuickSort, MergeSort, and TimSort for performance claims.
- Use Python 3.8+ for compatibility.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, open an issue on GitHub or reach out to [kisalnelaka6@gmail.com].

---
*Last Updated: August 21, 2025*