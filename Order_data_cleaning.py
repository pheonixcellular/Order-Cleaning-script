import pyforest as py
import dropbox
from io import BytesIO
import requests

# Replace 'YOUR_ACCESS_TOKEN' with your actual access token
ACCESS_TOKEN = 'sl.Bvv0II--mLihFYNpOfxlzey6GWEtnRtWiIU01AY2NBTZTn6b5nfcoJjjX0j8egGYvChTGcM_RCwiGWHRXasGEn4Xz4kbxCj0vNSp8hA96qcXXi_6vdLUvvPqflkbp5uYp1d8yodYvoRJGN33ZmjV'

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Path to the file you want to download
folder = '/B2C orders/'




response = dbx.files_list_folder(folder)

# Get the latest file by modification time
latest_file = max((entry for entry in response.entries if isinstance(entry, dropbox.files.FileMetadata)), key=lambda x: x.client_modified)

# Download the latest file
metadata, response = dbx.files_download(latest_file.path_display)


csv_content = BytesIO(response.content)

df1 = pd.read_csv(csv_content)
df1['IMEI'] = df1['IMEI'].astype(str)
df1['IMEI'] = df1['IMEI'].str.split(' ').str[0]
df1['IMEI'] = df1['IMEI'].replace('nan','')
df1 = df1[~df1['SKU'].str.startswith('UK')]
df1['SKU'] = df1['SKU'].str.replace('GR8_','')



csv_content = df1.to_csv(index=False)
latest_file_name = latest_file.name

# Path to save the file on Dropbox (same folder)
upload_file_path = '/B2C Orders/Processed_orders/'+latest_file_name

# Upload the file to Dropbox
with BytesIO(csv_content.encode()) as file_content:
    file_size = len(csv_content)
    try:
        dbx.files_upload(file_content.read(), upload_file_path, mode=dropbox.files.WriteMode("overwrite"))
        print("File uploaded successfully to Dropbox.")
    except Exception as e:
        print("Error uploading file to Dropbox:", e)   