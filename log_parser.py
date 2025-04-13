import json

# Function for parsing log
def parse_log_line_simple(line):
    parts = line.strip().split()

    if len(parts) < 7:
        return None

    timestamp = parts[0] + ' ' + parts[1]
    service_name = parts[2]
    status_code = int(parts[3])
    response_time_ms = int(parts[4].replace('ms', ''))
    user_id = parts[5]
    transaction_id = parts[6]
    additional_info = ' '.join(parts[7:])

    return {
        "timestamp": timestamp,
        "service_name": service_name,
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        "user_id": user_id,
        "transaction_id": transaction_id,
        "additional_info": additional_info
    }

# Main fuction for process all log file
def parse_log_file(file_path):
    parsed_logs = []
    total_response_time = 0
    total_transactions = 0
    total_errors = 0

    with open(file_path, 'r') as file:
        for line in file:
            parsed = parse_log_line_simple(line)
            if parsed:
                parsed_logs.append(parsed)
                total_transactions += 1
                total_response_time += parsed["response_time_ms"]
                if 400 <= parsed["status_code"] < 600:
                    total_errors += 1

    # Calculate average response time
    average_response_time = total_response_time / total_transactions if total_transactions > 0 else 0
    error_rate = (total_errors / total_transactions * 100) if total_transactions > 0 else 0

    print("Total Transaction:", total_transactions)
    print("Total Error (400/500):", total_errors)
    print("Average Response Time (ms):", round(average_response_time, 2))
    print("Error Rate: {:.2f}%".format(error_rate))

    # save result parsing to json
    with open("parsed_logs.json", "w") as out_file:
        json.dump(parsed_logs, out_file, indent=4)

    print("parsing saved to parsed_logs.json")

# run program
if __name__ == "__main__":
    file_path = "sample.log"  # rename this file based the log.
    parse_log_file(file_path)
