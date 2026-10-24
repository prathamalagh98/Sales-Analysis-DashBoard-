# Sales Analysis Dashboard

A Python-based project developed according to Units I, II, and III of the syllabus.

**Technologies:** Python, NumPy, Pandas, Matplotlib, Seaborn, Tkinter

## How to Run

1. Make sure Python 3.9 or later is installed. (Tkinter is included with Python on Windows.)
2. Open a terminal in the project folder and run:

   ```bash
   pip install -r requirements.txt
   python app.py
   ```

   The `data/sales_data.csv` file is automatically generated the first time the application runs.

   To generate the sample data separately, run:

   ```bash
   python generate_data.py
   ```

## Project Files

| File | Description | Syllabus Unit |
|---|---|---|
| `generate_data.py` | Generates random sales data using NumPy, including missing values. | Unit II (NumPy) |
| `analyzer.py` | Contains the `SalesAnalyzer` class for loading and cleaning data (using median imputation), filtering, statistical analysis, and operations using `lambda`, `map()`, `filter()`, and `reduce()`. | Units I and II |
| `charts.py` | Creates line charts, area charts, bar charts, pie charts, histograms, and Seaborn heatmaps. | Units II and III |
| `app.py` | Implements the Tkinter GUI with menus, popup menus, buttons, dropdowns, keyboard shortcuts, and embedded charts. | Unit III |

## Features

- **Welcome Screen:** Start the application using the Start button or the Enter key.
- **Student Details:** Update `STUDENT_NAME` and `STUDENT_UID` at the top of `app.py`.
- **File Menu:**
  - Open CSV: `Ctrl + O`
  - Generate Sample Data
  - Save Chart as PNG: `Ctrl + S`
  - Exit: `Ctrl + Q`
- **Data Filtering:** Filter sales data by category or region. All statistics and charts update according to the selected filters.
- **Charts:** View trend (line), area, bar (category/region), pie (segment/category), histogram, and heatmap visualizations.
- **Context Menu:** Right-click on a chart to access the popup menu.
- **Tkinter Layouts:** Uses all three geometry managers: `pack`, `grid`, and `place`.

## Using Your Own CSV File

To use your own sales dataset, ensure that it contains the following columns:

`Date, Category, Region, Segment, Quantity, Revenue`
