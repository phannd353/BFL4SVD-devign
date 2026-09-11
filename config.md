# Default Config

`data.x: torch.Size([3280, 101])`

`GNN out_channels: 200`

```json
{
  "gated_graph_conv_args": {
    "out_channels": 200,
    "num_layers": 6
  },
  "conv_args": {
    "conv1d_1": {
      "in_channels": 205,
      "out_channels": 50
    },
    "conv1d_2": {
      "in_channels": 50,
      "out_channels": 20
    }
  },
  "emb_size": 101
}
```

```json
{
  "create": {
    "slice_size": 100
  }
}
```

```json
{
  "embed": {
    "nodes_dim": 205,
    "word2vec_args": {
      "vector_size": 100
    }
  }
}
```
