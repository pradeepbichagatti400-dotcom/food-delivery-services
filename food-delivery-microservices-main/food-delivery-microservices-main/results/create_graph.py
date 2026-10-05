import matplotlib.pyplot as plt

# Official workload results
concurrency = [1, 2, 4, 8, 16]

response_time = [63.87, 116.14, 68.49, 146.21, 235.48]

throughput = [15.35, 16.43, 53.07, 47.59, 43.77]


# --------------------------------------------------
# Graph 1: Concurrency vs Average Response Time
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    concurrency,
    response_time,
    marker="o",
    linewidth=2
)

plt.xlabel("Concurrency")
plt.ylabel("Average Response Time (ms)")
plt.title("Concurrency vs Average Response Time")

plt.xticks(concurrency)
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "concurrency-vs-response-time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# --------------------------------------------------
# Graph 2: Concurrency vs Throughput
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    concurrency,
    throughput,
    marker="o",
    linewidth=2
)

plt.xlabel("Concurrency")
plt.ylabel("Throughput (requests/sec)")
plt.title("Concurrency vs Throughput")

plt.xticks(concurrency)
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "concurrency-vs-throughput.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()