import os
from google.cloud import storage
from google.api_core.exceptions import NotFound, Conflict

class GCSManager:
    """
    A class to manage Google Cloud Storage operations for a specific bucket.
    """
    def __init__(self, credentials_path, bucket_name, location="US"):
        """
        Initializes the GCSManager, authenticates, and ensures the bucket exists.

        Args:
            credentials_path (str): Path to the service account JSON key file.
            bucket_name (str): The name of the GCS bucket to manage.
            location (str, optional): The location to create the bucket in if it doesn't exist.
                                     Defaults to "US".
        """
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                f"Service account key not found at '{credentials_path}'. "
                "Please ensure the file exists."
            )
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(self.bucket_name)

        # Check if bucket exists, create if not
        if not self.bucket.exists():
            print(f"Bucket '{self.bucket_name}' does not exist. Creating it...")
            try:
                self.client.create_bucket(self.bucket, location=location)
                print(f"Bucket '{self.bucket_name}' created.")
            except Conflict:
                print(f"Bucket '{self.bucket_name}' was created by another process. Continuing.")
            except Exception as e:
                print(f"Could not create bucket: {e}")
                raise  # Re-raise the exception to halt execution if bucket creation fails
        else:
            print(f"Bucket '{self.bucket_name}' already exists.")

    def list_all_project_buckets(self):
        """Lists all buckets in the authenticated project."""
        print("--> Listing all buckets for the project:")
        try:
            buckets = self.client.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]
            if bucket_names:
                for name in bucket_names:
                    print(f"  - {name}")
            else:
                print("  No buckets found in this project.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def upload_file(self, source_file_path, destination_blob_name):
        """Uploads a file to the bucket."""
        print(f"--> Uploading '{source_file_path}' to bucket '{self.bucket_name}' as '{destination_blob_name}':")
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
            print("  File uploaded successfully.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def list_files(self):
        """Lists all the files (blobs) in the bucket."""
        print(f"--> Listing all files in bucket '{self.bucket_name}':")
        try:
            blobs = self.client.list_blobs(self.bucket_name)
            file_names = [blob.name for blob in blobs]
            if file_names:
                for name in file_names:
                    print(f"  - {name}")
            else:
                print("  Bucket is empty.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def view_file(self, blob_name):
        """Prints the content of a file directly from the bucket."""
        print(f"--> Viewing content of '{blob_name}':")
        try:
            blob = self.bucket.blob(blob_name)
            content = blob.download_as_text()
            print("  --- File Content ---")
            print(content)
            print("  --- End of Content ---")
        except NotFound:
            print(f"  File '{blob_name}' not found in bucket '{self.bucket_name}'.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def download_file(self, source_blob_name, destination_file_path):
        """Downloads a file from the bucket to the local filesystem."""
        print(f"--> Downloading '{source_blob_name}' to '{destination_file_path}':")
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_path)
            print(f"  File downloaded successfully to '{destination_file_path}'.")
        except NotFound:
            print(f"  File '{source_blob_name}' not found in bucket '{self.bucket_name}'.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def edit_file(self, blob_name, new_content):
        """'Edits' a file in the bucket by uploading new content to it."""
        print(f"--> Editing file '{blob_name}' with new content:")
        try:
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(new_content)
            print("  File edited successfully.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def create_folder(self, folder_name):
        """Creates a 'folder' by creating an empty object with a trailing '/'."""
        if not folder_name.endswith('/'):
            folder_name += '/'
        print(f"--> Creating folder '{folder_name}':")
        try:
            blob = self.bucket.blob(folder_name)
            blob.upload_from_string('')
            print("  Folder created successfully.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def list_directories(self):
        """Lists 'directories' at the root of the bucket."""
        print(f"--> Listing directories in bucket '{self.bucket_name}':")
        try:
            iterator = self.client.list_blobs(self.bucket_name, delimiter='/')
            # The response contains prefixes, which represent the 'subdirectories'.
            response = next(iterator.pages)
            if 'prefixes' in response:
                print("  Found directories:")
                for prefix in response['prefixes']:
                    print(f"  - {prefix}")
            else:
                print("  No directories found at the root level.")
        except Exception as e:
            print(f"  An error occurred: {e}")
        print("-" * 30)

    def delete_bucket(self):
        """Deletes the bucket and all its contents. This is a destructive action."""
        print(f"\n--- Deleting bucket '{self.bucket_name}' and all its contents ---")
        try:
            # The 'force=True' parameter deletes all objects in the bucket first.
            self.bucket.delete(force=True)
            print(f"Bucket '{self.bucket_name}' deleted successfully.")
        except NotFound:
            print(f"Bucket '{self.bucket_name}' not found.")
        except Exception as e:
            print(f"An error occurred while deleting the bucket: {e}")
        print("-" * 30)