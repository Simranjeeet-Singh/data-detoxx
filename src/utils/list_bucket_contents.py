#Write a python boto3 function to list all the contents of an s3 bucket and return filenames in a list

import boto3


def list_files_from_s3(bucket_name: str) -> list[str]:
    """
    Args : bucket_name as a `string` \n
    Returns : list of file names inside the bucket as `list` of `strings`
    """
    client=boto3.client('s3')
    response=client.list_objects(Bucket=bucket_name)   
    if 'Contents' not in response:
        return []
    return [item['Key'] for item in response['Contents']]
    

