import pandas as pd

# Read the file
with open('data.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Initialize variables
data_list = []
current_quality = ''
current_row = []

# Process each line
i = 0
while i < len(lines):
    line = lines[i].strip()
    
    if not line:
        i += 1
        continue
    
    if 'Higher quality' in line:
        current_quality = 'Higher'
    elif 'Average quality' in line:
        current_quality = 'Average'
    elif 'Lower quality' in line:
        current_quality = 'Lower'
    elif line.startswith('Name:'):
        if current_row:
            data_list.append(current_row)
        current_row = [line]  # conv1
        if i + 1 < len(lines):
            current_row.append(lines[i + 1].strip())  # conv2
        if i + 2 < len(lines):
            current_row.append(lines[i + 2].strip())  # conv3
        if i + 3 < len(lines):
            current_row.append(lines[i + 3].strip())  # conv4
        current_row.append(current_quality)  # quality
        i += 3  # Skip the next 3 lines as they are already processed
    
    i += 1

# Add the last row if exists
if current_row:
    data_list.append(current_row)

# Create DataFrame
df = pd.DataFrame(data_list, columns=['conv1', 'conv2', 'conv3', 'conv4', 'quality'])

# Save to Excel
df.to_excel('output.xlsx', index=False)