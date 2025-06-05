# 🧭 PathfindingPlayground

A real-time visualizer for classic pathfinding algorithms built using Python and Pygame. Designed to simulate and understand how different algorithms explore space, adapt to weights, and find optimal paths.

---

## ✨ Features

- 🔄 **Multiple Algorithms**  
  Visualize A*, Dijkstra’s, Breadth-First Search, and Bellman-Ford with live updates.

- 🔁 **Negative Weight Zones**  
  Toggle negative weight mode for Bellman-Ford using the `N` key. Click cells to set them as "easier paths."

- 🧠 **Interactive UI**  
  Click to place Start, End, Barriers, or Negative Cells. Press keys 1-5 to switch algorithms instantly.

- 🧱 **Grid-Based Visual Feedback**  
  Colored cells represent open, closed, barriers, paths, start/end, and negative-weight nodes.

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| `1` | A* Algorithm |
| `2` | Dijkstra’s Algorithm |
| `3` | Breadth-First Search |
| `4` | Floyd-Warshall (placeholder) |
| `5` | Bellman-Ford Algorithm |
| `N` | Toggle negative weight mode (Bellman-Ford) |
| `SPACE` | Run selected algorithm |
| `C` | Clear board |

🖱 **Mouse Clicks**:
- Left Click: Place Start, End, Barrier, or Negative-weight cell (when toggled)
- Right Click: Erase cell

---

## 🛠️ Tech Stack

- **Python 3**
- **Pygame**

---

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/pathfinding-visualizer.git
   cd pathfinding-visualizer
