import pandas as pd

# Sample data
data = {
    'Column1': [1, 2, 3, 4, 5],
    'Column2': ['A', 'B', 'C', 'D', 'E']
}
df = pd.DataFrame(data)

# Export to Excel
df.to_excel('output.xlsx', engine='openpyxl', index=False)
