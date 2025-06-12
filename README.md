# escrowai-api-sample

Example scripts for usage of the EscrowAI API by algorithm owner and data steward users.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Python**: Version 3.x installed.
2.  **pip**: Python package installer (usually comes with Python).
3.  **Git**: For cloning this repository.
4.  **EscrowAI Account**:
    *   An active account on the BeeKeeperAI EscrowAI platform.
    *   A Project created within EscrowAI. You will need the **Project ID**.
    *   An RSA public key uploaded to your EscrowAI user profile. The scripts will use the corresponding private key for authentication.
5.  **RSA Private Key**: The private RSA key (in PEM format) corresponding to the public key uploaded to EscrowAI.

## Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/BeeKeeperAI/escrowai-api-sample # Replace <repository_url> with the actual URL
    cd escrowai-api-sample
    ```

2.  **Create and Activate a Virtual Environment (Recommended)**:
    To avoid conflicts with your global Python packages, it's highly recommended to use a virtual environment.

    *   **Create the environment (e.g., named `.venv`)**:
        ```bash
        python3 -m venv .venv
        ```

    *   **Activate the environment**:
        *   On macOS and Linux:
            ```bash
            source .venv/bin/activate
            ```
        *   On Windows (Git Bash or similar):
            ```bash
            source .venv/Scripts/activate
            ```
        *   On Windows (Command Prompt or PowerShell):
            ```bash
            .venv\Scripts\activate.bat  # For Command Prompt
            .venv\Scripts\Activate.ps1 # For PowerShell (you might need to set execution policy)
            ```
        You should see the virtual environment's name (e.g., `(.venv)`) prefixed to your shell prompt.

3.  **Install Dependencies**:
    Once your virtual environment is activated, install the necessary Python packages using the provided `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variable**:
    The scripts require your RSA private key to be available in an environment variable named `ESCROW_PRIVATE_KEY`.
    ```bash
    export ESCROW_PRIVATE_KEY='-----BEGIN RSA PRIVATE KEY-----
    MIIE...
    -----END RSA PRIVATE KEY-----'
    ```
    Alternatively, you can load it from a file within the script, but you'll need to modify the script's `os.environ.get('ESCROW_PRIVATE_KEY')` line.

5.  **Create Directories**:
    The scripts expect certain directories to exist for storing downloaded files and input files:
    ```bash
    mkdir downloads
    mkdir files
    ```

6.  **Prepare Input Files**:
    You will need to provide certain files and place them in the `files/` directory. The exact filenames you use should replace the placeholders in the scripts.

    *   **For `algorithm-owner.py`**:
        *   `files/{data_specification}.pdf`: Your data specification document.
        *   `files/{validation_criteria}.json`: Your validation criteria document.
        *   `files/{algorithm}`: Your algorithm file(s) (e.g., `my_model.py`, `model.tar.gz`). The script will zip this if it's a single file/directory, or you can pre-zip it and adjust the script.

    *   **For `data-steward.py`**:
        *   `files/{data_attestation}.pdf`: Your data attestation document.
        *   `files/{dataset}`: Your dataset file(s) (e.g., `dataset.csv`, `images/`). The `encrypt_upload_dataset` function will handle packaging.

7.  **Update Script Placeholders**:
    **This is a critical step.** The Python scripts (`algorithm-owner.py` and `data-steward.py`) are templates and contain numerous placeholder strings enclosed in curly braces (e.g., `{project_id}`, `{email_address}`, `{name}`, `{cek}.key`, etc.).

    **You must manually edit both `algorithm-owner.py` and `data-steward.py` and replace ALL these placeholder strings with your actual values before running the scripts.**

    Key placeholders to look for and replace:

    *   **Constants at the top of each script**:
        *   `PROJECT_ID = '{project_id}'`: Replace `{project_id}` with your EscrowAI Project ID.
        *   `EMAIL_ADDRESS = '{email_address}'`: Replace `{email_address}` with the email address associated with your EscrowAI account.

    *   **Filenames in `open(...)` calls, `files=` parameters, and encryption function arguments**:
        *   Examples: `'downloads/{cek}.key'`, `'files/{data_specification}.pdf'`, `'downloads/{wkey}.bkenc'`, `'files/{algorithm}'`, `'files/{encrypted_algorithm}.zip'`, `'files/{dataset}'`.
        *   You need to decide on actual filenames and use those consistently. For example, instead of `'{cek}.key'`, you might use `'my_content_encryption_key.key'`.

    *   **Metadata in API request `data` payloads**:
        *   `'name': '{name}'`
        *   `'description': '{description}'`
        *   `'version_description': '{version_description}'`
        *   `'version_tag': '{version_tag}'`
        *   `'{validation_criteria_version_tag}'`
        *   `'{data_attestation_version_tag}'`
        *   `'{algorithm_version_tag}'`
        *   `'{dataset_version_tag}'`
        *   `'{machine}'` (e.g., `'cpu-standard-4'`)
        *   `'{tags}'` (for datasets)
        *   `'{dataset_uri}'` (SAS URL for dataset upload in `data-steward.py`, this is usually returned by `encrypt_upload_dataset` function)
        *   `'{sas_url}'` (placeholder for the Azure SAS URL used by `encrypt_upload_dataset`)

    *   **URL parameters for GET requests**:
        *   `run_number` in report download calls.
        *   `algorithm_version_tag` and `dataset_version_tag` in initiate run and report download calls.

    **Treat these placeholders as values you need to define and hardcode into the script for your specific use case, or refactor the scripts to use variables that you define at the top.**

## Running the Scripts

Ensure all placeholders in the scripts have been replaced with your actual values.

1.  **Algorithm Owner Script**:
    The `algorithm-owner.py` script performs operations typical for an algorithm provider, such as uploading algorithms, data specifications, and validation criteria, and managing runs.
    ```bash
    python algorithm-owner.py
    ```

2.  **Data Steward Script**:
    The `data-steward.py` script performs operations typical for a data provider, such as uploading datasets, data attestations, and managing runs.
    ```bash
    python data-steward.py
    ```

## API Documentation

Full API documentation can be found at https://docs.escrow.beekeeperai.com/prodapi/escrowai-public-apis.