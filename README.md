# PythonJigsaw01 🎯

A simple jigsaw puzzle game built with Python, PyQt5, and Pillow.  
Load any image (below a certain size), split it into pieces, and manually assemble them - pieces snap together and cluster when placed near each other.

---

## Features

- Load a custom image and divide it into a configurable number of pieces.  
- Pieces are shuffled randomly on the canvas.  
- Drag and drop pieces with the mouse.  
- Pieces “snap” to neighbors when aligned - forming clusters that move together.  
- Settings persist via a JSON config (e.g., background color, puzzle size).  
- Supports different image & puzzle sizes (within reasonable limits).  

---

## Demo / Screenshots

<img width="1920" height="1030" alt="Screenshot 2025-12-06 164542" src="https://github.com/user-attachments/assets/776d23d7-77e0-46ac-8dad-a9fcd2506984" />

---

## Requirements

- Python 3.x  
- [PyQt5](https://pypi.org/project/PyQt5/)  
- [Pillow (PIL)](https://pypi.org/project/Pillow/)  

---

## Installation

```bash
git clone https://github.com/serialexperiments0815/PythonJigsaw01.git
cd PythonJigsaw01
pip install PyQt5 Pillow
```

## Usage
```bash
python main.py
```
---
