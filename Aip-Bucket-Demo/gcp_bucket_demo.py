import os
import json
import argparse # New import
from google.cloud import storage # New import for temporary client
from gcs_manager import GCSManager

def main():
    """Runs the GCP Storage demonstration based on a JSON plan."""
    print("--- Starting GCP Bucket Demonstration ---")
    
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Run GCP Storage bucket demonstration.")
    parser.add_argument(
        "--credentials",
        "-c",
        type=str,
        default=os.path.join('env', 'sodium-lodge-462105-a5-8bd3b06c45b2.json'),
        help="Path to the Google Cloud service account JSON key file."
    )
    parser.add_argument(
        "--bucket-suffix",
        "-s",
        type=str,
        default="-demo-bucket-aip",
        help="Suffix for the demonstration bucket name. The full name will be <project_id><suffix>."
    )
    parser.add_argument(
        "--demo-plan",
        "-p",
        type=str,
        default="demo_plan.json",
        help="Path to the JSON file containing the demonstration plan."
    )
    args = parser.parse_args()

    credentials_path = args.credentials
    demo_plan_path = args.demo_plan

    demo_plan_path = "demo_plan.json"
    local_file_to_upload = "demo_upload.txt"
    downloaded_file_name = "demo_downloaded.txt" # Needed for cleanup

    # --- Setup ---
    print("\n--- Preparing local files for Demo ---")
    # Ensure the local file for upload exists
    with open(local_file_to_upload, "w") as f:
        f.write("Hello, Google Cloud Storage!")
    print(f"Created local file: '{local_file_to_upload}'")
    print("-" * 30)

    try:
        # --- Initialization ---
        # Set GOOGLE_APPLICATION_CREDENTIALS for the temporary client to infer project_id
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        temp_client = storage.Client()
        project_id = temp_client.project
        bucket_name = f"{project_id}{args.bucket_suffix}"

        # Initialize GCSManager with the determined bucket name
        gcs_manager = GCSManager(credentials_path, bucket_name)

        # --- Load and Run Demonstration Plan ---
        print(f"--- Loading demonstration plan from '{demo_plan_path}' ---")
        with open(demo_plan_path, 'r') as f:
            plan = json.load(f)
        
        print("\n--- Executing demonstration plan ---")
        for i, step in enumerate(plan):
            action = step.get("action")
            params = step.get("params", {})
            
            print(f"\n--- Step {i+1}: {action} ---") # Added step indicator
            if not action:
                print(f"Skipping step {i+1}: No action defined.")
                continue

            try:
                method_to_call = getattr(gcs_manager, action)
                method_to_call(**params)
            except AttributeError:
                print(f"Error in step {i+1}: Action '{action}' not found in GCSManager.")
            except Exception as e:
                print(f"An error occurred during action '{action}': {e}")
                # For a demonstration, we continue on error. For production, you might want to stop.

        # --- Optional Cleanup on GCP ---
        # Uncomment the following line to delete the bucket and all its contents
        # gcs_manager.delete_bucket()

    except Exception as e:
        print(f"A critical error occurred during initialization or plan execution: {e}")
        # Provide more specific error messages for common issues
        if isinstance(e, FileNotFoundError):
            print(f"Please ensure the credentials file ('{credentials_path}') and demo plan file ('{demo_plan_path}') exist and paths are correct.")
        elif isinstance(e, json.JSONDecodeError):
            print(f"Could not parse demo plan JSON file '{demo_plan_path}'. Please check its format.")
    finally:
        # --- Local File Status ---
        print("\n--- Local File Cleanup Skipped ---")
        # The following lines are commented out to prevent local file deletion as requested.
        # if os.path.exists(local_file_to_upload): os.remove(local_file_to_upload)
        # if os.path.exists(downloaded_file_name): os.remove(downloaded_file_name)
        print("Local demo files have been preserved in the directory.")
        print("-" * 30)
        print("Demonstration complete.")

if __name__ == "__main__":
    main()
