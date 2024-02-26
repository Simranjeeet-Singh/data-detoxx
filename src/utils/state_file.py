import boto3
import json


def write_state_file(save_file_path: str, counter_table_dict: dict) -> None:

    json_string = json.dumps(counter_table_dict)
    with open(save_file_path, "w") as f:
        json.dump(json_string, f)
    print(f"JSON file saved to {save_file_path}")


if __name__ == "__main__":
    bucket_name = "data-detox-ingestion-bucket"
    file_name = "state_file.json"
    # Create an S3 client
    s3 = boto3.client("s3")

    # Example JSON data
    data = {"key1": "value1", "key2": "value2"}

    # Convert JSON data to string
    json_string = json.dumps(data)

    # Upload the JSON string to S3
    s3.put_object(Body=json_string, Bucket=bucket_name, Key=file_name)
    print("JSON file uploaded to S3 successfully!")
    write_state_file("tmp/state_file.json", {"key": "value"})
