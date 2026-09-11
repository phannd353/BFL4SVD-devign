from pathlib import Path

import pandas as pd
import torch


def check_data(inputPath: str):
    xs = []
    ys = []
    counts = []
    edge_counts = []

    for path in sorted(Path(inputPath).glob("*.pkl")):
        df = pd.read_pickle(path)

        for i, row in df.iterrows():
            graph = row["input"]
            print(torch.unique(graph.x))
            xs.append(graph.x)
            ys.append(int(row["target"]))
            x = row["input"].x
            counts.append(int((x.abs().sum(dim=1) != 0).sum()))
            edge_counts.append(row["input"].edge_index.shape[1])

    x = torch.stack(xs)
    y = torch.tensor(ys)

    print("=" * 25 + " DATA FEATURES " + "=" * 25)

    print("x shape:", tuple(x.shape))
    print("labels:", torch.bincount(y))
    print("global min:", x.min().item())
    print("global max:", x.max().item())
    print("global mean:", x.mean().item())
    print("global std:", x.std().item())
    print("zero fraction:", (x == 0).float().mean().item())
    print("non-finite values:", (~torch.isfinite(x)).sum().item())

    for label in [0, 1]:
        label_x = x[y == label]
        print(
            f"class {label}:",
            "count =",
            len(label_x),
            "mean =",
            label_x.mean().item(),
            "std =",
            label_x.std().item(),
        )

    print("=" * 25 + " NON-PADDING NODES " + "=" * 25)

    print("graphs:", len(counts))
    print("min real nodes:", min(counts))
    print("max real nodes:", max(counts))
    print("average real nodes:", sum(counts) / len(counts))
    print("empty graphs:", sum(n == 0 for n in counts))

    print("=" * 25 + " EDEGS " + "=" * 25)

    print("min edges:", min(edge_counts))
    print("max edges:", max(edge_counts))
    print("average edges:", sum(edge_counts) / len(edge_counts))
    print("graphs without edges:", sum(n == 0 for n in edge_counts))
