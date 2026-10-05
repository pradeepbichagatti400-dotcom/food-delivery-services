import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://localhost:5002/orders"

# Change this value for each workload test
CONCURRENCY = 1

def send_request(customer_id):
    body = {
        "restaurant_id": 101,
        "items": [
            {
                "item_id": 2,
                "quantity": 1
            }
        ],
        "customer_id": customer_id
    }

    start = time.perf_counter()

    try:
        response = requests.post(
            URL,
            json=body,
            timeout=10
        )

        end = time.perf_counter()

        return {
            "success": response.status_code == 201,
            "response_time_ms": (end - start) * 1000,
            "status_code": response.status_code
        }

    except requests.RequestException:
        end = time.perf_counter()

        return {
            "success": False,
            "response_time_ms": (end - start) * 1000,
            "status_code": "ERROR"
        }


def run_test():
    print("=" * 50)
    print("FOOD DELIVERY MICROSERVICES WORKLOAD TEST")
    print("=" * 50)

    print(f"Concurrency       : {CONCURRENCY}")
    print(f"Total Requests    : {CONCURRENCY}")
    print()

    start_all = time.perf_counter()

    results = []

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:

        futures = [
            executor.submit(send_request, 100 + i)
            for i in range(CONCURRENCY)
        ]

        for future in as_completed(futures):
            results.append(future.result())

    end_all = time.perf_counter()

    total_time = end_all - start_all

    successful = sum(
        1 for result in results
        if result["success"]
    )

    failed = len(results) - successful

    average_response = sum(
        result["response_time_ms"]
        for result in results
    ) / len(results)

    throughput = len(results) / total_time

    print(f"Successful Requests: {successful}")
    print(f"Failed Requests    : {failed}")
    print(f"Average Response   : {average_response:.2f} ms")
    print(f"Total Test Time    : {total_time:.4f} s")
    print(f"Throughput         : {throughput:.2f} requests/sec")

    print()
    print("Individual Results:")
    
    for i, result in enumerate(results, start=1):
        print(
            f"Request {i}: "
            f"{result['response_time_ms']:.2f} ms | "
            f"Status: {result['status_code']} | "
            f"{'SUCCESS' if result['success'] else 'FAILED'}"
        )

    # Save result to CSV
    csv_file = "results/workload-results.csv"

    with open(csv_file, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            CONCURRENCY,
            len(results),
            successful,
            failed,
            round(average_response, 2),
            round(throughput, 2)
        ])

    print()
    print(f"Result saved to: {csv_file}")


if __name__ == "__main__":
    run_test()