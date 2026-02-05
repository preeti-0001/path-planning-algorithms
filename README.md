# Robot Path Planning Lab

A modular robot path planning simulator built for experimentation, visualization, and algorithm comparison.

Phase 1 uses Python + Pygame.
Phase 2 will support ROS + RViz.

---

## Features (Phase 1)

* Multiple saved maps
* Interactive 2D grid map builder
* Start & goal point editing
* Bug2 path planning algorithm
* Animated robot motion
* Replay slider
* Algorithm side panel (extensible)
* Modular architecture for future planners

---

## Project Structure

core/
Simulation engine and environment logic

algorithms/
Path planning algorithm plugins

ui_pygame/
Graphical interface using Pygame

maps/
Saved grid environments

ros_bridge/
Future ROS + RViz interface

---

## Installation

```bash
git clone 
cd robot-path-lab
pip install -r requirements.txt
python main.py
```

---

## Controls

Home Screen:

* Select a map
* Click + to create new map

Map Editor:

* Left click → toggle obstacle
* S key → set start
* G key → set goal
* Save → store map

Map Viewer:

* Start → run Bug2 algorithm
* Drag slider → replay path
* Change goal → replan dynamically

---

## Algorithm Interface

All planners follow:

```python
class Planner:
    def step(self):
        pass

    def run(self):
        pass

    def reset(self, start, goal):
        pass
```

New algorithms can be dropped into the algorithms folder.

---

## Roadmap

Phase 2:

* ROS node integration
* RViz visualization
* real-time sensor updates
* multi-algorithm comparison

Phase 3:

* dynamic obstacles
* RRT / A* / D* Lite
* experiment metrics dashboard

---

## Purpose

This is a reusable robotics path planning lab, not just an assignment.

Designed for:

* learning
* benchmarking
* visualization
* research prototyping

---

Author: Preeti Dudi
