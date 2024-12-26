# Inscribed Rectangle Problem Visualization

Interactive visualization tool for exploring the Inscribed Rectangle Problem - a mathematical conjecture about rectangle inscribability in Jordan curves.

## Features
- Interactive closed loop with draggable points
- Color-coded vertices: yellow/magenta and sandybrown/palevioletred
- Cyan connection lines between vertex pairs
- Teal midpoint indicators
- Springgreen intersection point
- Dark background with turquoise grid and white center axes
- Real-time coordinate tracking (0.0-1.0)

## Mathematical Context
The inscribed rectangle problem is a fundamental question in geometry, asking whether every Jordan curve contains the vertices of a rectangle [1]. While the inscribed square problem remains open for general curves [2], recent work by Cole and Shiu has made significant progress on inscribed rectangles using geometric foliation theory [3]. This visualization tool helps explore possible rectangle configurations, inspired by Haraguchi's topological approach [4] and recent breakthroughs in the field [5].

## Requirements
- Python 3.x
- NumPy
- Matplotlib

## Usage
```python
python main.py
```

## Example Screenshots
![alt text](example_screenshots/parallel.png)
![alt text](example_screenshots/intersection.png)

## References
[1] Schwartz, R. E. "The Rectangle-Inscribing Problem." Quanta Magazine (2020). Available: https://www.quantamagazine.org/new-geometric-perspective-cracks-old-problem-about-rectangles-20200625/

[2] Matschke, B. "A survey on the square peg problem." Notices of the AMS 61.4 (2014): 346-352.
Available: https://en.wikipedia.org/wiki/Inscribed_square_problem

[3] Cole, H. and Shiu, T. "Inscribed Rectangles," Topology Proceedings, 31 (2007), 107-114.
Available: https://topology.nipissingu.ca/tp/reprints/v06/tp06107.pdf

[4] Hugelmeyer, C. "Every smooth Jordan curve has an inscribed rectangle with aspect ratio equal to √3." arXiv:2005.09193 (2020).
Available: https://arxiv.org/pdf/2005.09193

[5] 3Blue1Brown. "Why every circle has an inscribed rectangle," YouTube (2022).
Available: https://www.youtube.com/watch?v=IQqtsm-bBRU