import boto3
import json


def write_state_file(save_file_path: str, counter_table_dict: dict) -> None:

    json_string = json.dumps(counter_table_dict)
    with open(save_file_path, "w") as f:
        json.dump(json_string, f)
    print(f"JSON file saved to {save_file_path}")


def read_state_file_from_s3(bucket_name: str) -> dict:

    s3 = boto3.resource("s3")
    try:
        obj = s3.Object(bucket_name, "state_file.json")
        json_data = json.loads(json.load(obj.get()["Body"]))
        return json_data
    except Exception as e:
        print(f"Error reading JSON file from S3: {e}")
        return None


if __name__ == "__main__":
    bucket_name = "data-detox-ingestion-bucket"
    file_name = "state_file.json"
    s3 = boto3.client("s3")
    data = {"key1": "value1", "key2": "value2"}
    json_string = json.dumps(data)
    # s3.put_object(Body=json_string, Bucket=bucket_name, Key=file_name)
    # write_state_file("tmp/state_file.json", {"key": "value"})
    state_file = read_state_file_from_s3(bucket_name)
    print(state_file, type(state_file))
