import time
import requests
import concurrent.futures
import statistics
from typing import List, Dict, Any

class BenchmarkResults:
    def __init__(self):
        self.latencies: List[float] = []
        self.operations_per_second = 0
        self.success_rate = 0.0
        self.total_operations = 0
        self.failed_operations = 0

    def add_latency(self, latency: float):
        self.latencies.append(latency)

    def calculate_statistics(self) -> Dict[str, Any]:
        return {
            'min_latency': min(self.latencies) if self.latencies else 0,
            'max_latency': max(self.latencies) if self.latencies else 0,
            'avg_latency': statistics.mean(self.latencies) if self.latencies else 0,
            'median_latency': statistics.median(self.latencies) if self.latencies else 0,
            'p95_latency': statistics.quantiles(self.latencies, n=20)[18] if self.latencies else 0,
            'operations_per_second': self.operations_per_second,
            'success_rate': self.success_rate,
            'total_operations': self.total_operations,
            'failed_operations': self.failed_operations
        }

class KeyValueStoreBenchmark:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = BenchmarkResults()

    def run_single_operation(self, operation: str, key: str, value: str = None) -> float:
        start_time = time.time()
        try:
            if operation == "PUT":
                response = requests.put(
                    f"{self.base_url}/kv/{key}",
                    json={"value": value}
                )
            elif operation == "GET":
                response = requests.get(f"{self.base_url}/kv/{key}")
            elif operation == "DELETE":
                response = requests.delete(f"{self.base_url}/kv/{key}")
            else:
                raise ValueError(f"Unknown operation: {operation}")

            if response.status_code not in [200, 201]:
                self.results.failed_operations += 1
                return 0

            return time.time() - start_time
        except Exception:
            self.results.failed_operations += 1
            return 0

    def run_concurrent_operations(self, num_operations: int, num_threads: int = 10):
        start_time = time.time()
        self.results = BenchmarkResults()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_operations):
                key = f"key_{i}"
                value = f"value_{i}"
                
                # Create operations
                futures.append(
                    executor.submit(self.run_single_operation, "PUT", key, value)
                )
                # Read operations
                futures.append(
                    executor.submit(self.run_single_operation, "GET", key)
                )
                # Delete operations
                futures.append(
                    executor.submit(self.run_single_operation, "DELETE", key)
                )

            for future in concurrent.futures.as_completed(futures):
                latency = future.result()
                if latency > 0:
                    self.results.add_latency(latency)

        total_time = time.time() - start_time
        self.results.total_operations = num_operations * 3  # 3 operations per key
        self.results.operations_per_second = self.results.total_operations / total_time
        self.results.success_rate = (self.results.total_operations - self.results.failed_operations) / self.results.total_operations * 100

        return self.results.calculate_statistics()

if __name__ == "__main__":
    benchmark = KeyValueStoreBenchmark()
    results = benchmark.run_concurrent_operations(1000)  # Run 1000 sets of operations
    print("Benchmark Results:")
    for key, value in results.items():
        if 'latency' in key:
            print(f"{key}: {value:.3f} seconds")
        else:
            print(f"{key}: {value:.2f}")