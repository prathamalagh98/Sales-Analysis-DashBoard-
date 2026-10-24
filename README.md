# Sales Analysis Dashboard

Python project based on Unit I, II, III.
Tech: Python, NumPy, Pandas, Matplotlib, Seaborn, Tkinter.

## Run kaise kare
1. Python 3.9+ install hona chahiye (Tkinter Windows me saath aata hai).
2. Terminal is folder me kholo:
       pip install -r requirements.txt
       python app.py
   (Pehli baar data/sales_data.csv apne aap ban jati hai.
    Alag se banane ke liye: python generate_data.py)

## Files
| File | Kaam | Syllabus |
|------|------|----------|
| generate_data.py | NumPy se random sales data, missing values ke saath | Unit 2 (NumPy) |
| analyzer.py | SalesAnalyzer class: load, clean (median fill), filter, stats, lambda/map/filter/reduce | Unit 1 + 2 |
| charts.py | Line, area, bar, pie, histogram, Seaborn heatmap | Unit 2 + 3 |
| app.py | Tkinter GUI: menu, popup menu, buttons, dropdown, key bindings, chart embed | Unit 3 |

## Features
- Welcome screen (Start button ya Enter key). Apna naam/UID app.py ke upar STUDENT_NAME aur STUDENT_UID me badlo
- File menu: Open CSV (Ctrl+O), Generate Sample Data, Save Chart PNG (Ctrl+S), Exit (Ctrl+Q)
- Category / Region filter, sab stats aur chart us filter ke hisaab se update hote hain
- Charts menu / buttons: Trend (line), Area, Bar (category/region), Pie (segment/category), Histogram, Heatmap
- Chart par right-click: popup menu
- pack, grid aur place teeno geometry managers use hue hain

## Apna CSV use karna ho to columns ye hone chahiye
Date, Category, Region, Segment, Quantity, Revenue
