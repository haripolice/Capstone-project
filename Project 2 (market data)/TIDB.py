import pandas as pd
import os

folder_path = "OneDrive_1_3-18-2025"
output_file_name = "combined_data.xlsx" 
all_data = []
all_files = os.listdir(folder_path)
 
for file in all_files:
    if file.endswith((".csv", ".xlsx")):  
        file_path = os.path.join(folder_path, file)
        try:
            if file.endswith(".csv"):
                df = pd.read_csv(file_path)  
            elif file.endswith(".xlsx"):
                df = pd.read_excel(file_path)  
 
            df['Source File'] = file
            all_data.append(df)
        except Exception as e:
            print(f"Error reading file: {file} - {e}")
 
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    try:
        combined_df.to_excel(output_file_name, index=False)
        print(f"Successfully combined data from all CSV and Excel files into '{output_file_name}'") 
    except Exception as e:
        print(f"Error writing to the output file: {e}")
else:
    print("No CSV or Excel files found in the specified folder.")