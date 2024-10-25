## Detection of europan cycloids and other surface features. (WIP)

### Canny Edge Detection

(Europa-Canny-Tuning.py)
![Canny Edge Detection Example](static/canny-example.png)

Bottom Left: Input image
Bottom Right: Preprocessing
Top Right: filters
Top Left: Canny edge detection

In total, these are all the filters applied:
- CLAHE
- Gaussian Blur
- Considered but removed: Erosion & Dilation morphological filters.
- Unsharpen
- Canny edge detection w/ variable thresholds

### Next steps:
- Edge annotation,
- Curvatures after canny edge detection
- Variable image size
