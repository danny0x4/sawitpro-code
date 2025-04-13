import requests
import json

ES_URL = "https://elastic.sallystore.my.id"  
INDEX_NAME = "parsed-logs"

USERNAME = "elastic"
PASSWORD = "admin123"

def push_logs(file_path):
    count_success = 0
    count_error = 0
    
    try:
        # read all file as one JSON array
        with open(file_path, 'r') as f:
            logs_array = json.load(f)
            
            # make sure that are read is an array
            if not isinstance(logs_array, list):
                print("Error: File tidak berisi array JSON")
                return
                
            print(f"Membaca {len(logs_array)} log entries dari file")
            
            # process every item in array
            for i, log_entry in enumerate(logs_array):
                try:
                    res = requests.post(
                        f"{ES_URL}/{INDEX_NAME}/_doc",
                        headers={"Content-Type": "application/json"},
                        auth=(USERNAME, PASSWORD),
                        data=json.dumps(log_entry)
                    )
                    
                    if res.status_code >= 200 and res.status_code < 300:
                        print(f"Berhasil mengindeks entry #{i+1}: {res.status_code} {res.reason}")
                        count_success += 1
                    else:
                        print(f"Gagal mengindeks entry #{i+1}: {res.status_code} {res.reason}")
                        print(f"Response: {res.text}")
                        count_error += 1
                        
                except Exception as e:
                    print(f"Error pada entry #{i+1}: {e}")
                    count_error += 1
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON dari file: {e}")
        return
    except FileNotFoundError:
        print(f"File tidak ditemukan: {file_path}")
        return
        
    print(f"\nTotal: {count_success} berhasil, {count_error} gagal")

if __name__ == "__main__":
    push_logs("parsed_logs.json")
