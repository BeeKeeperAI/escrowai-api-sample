# EscrowAI API Usage
# for Algorithm Owner
# Copyright 2025 BeeKeeperAI(r)
# Last updated: 2025-01-30

# Import dependencies
import datetime
import os
import jwt
import requests

# Import encryption tool
from bk_encryption.encryption import (
    generate_content_encryption_key,
    generate_wrapped_content_encryption_key,
    encrypt_algorithm,
)

# EscrowAI API base URL
BASE_URL = 'https://frontoffice.escrow.beekeeperai.com/api/v1'

# Set constants
PROJECT_ID = '{project_id}' # project ID, which can be found in the Project Settings page under Metadata
EMAIL_ADDRESS = '{email_address}' # your email address used to log in to EscrowAI

# Generate authentication payload
auth_payload = {
    'iss': 'EscrowAI-API',
    'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
    'aud': 'frontoffice.beekeeperai',
    'sub': PROJECT_ID,
    'user': EMAIL_ADDRESS
}

# Create bearer-compatible JWT using generated payload and private RSA key retrieved from environment as ESCROW_PRIVATE_KEY
# Requirement: have uploaded corresponding public key to EscrowAI
token = jwt.encode(auth_payload, os.environ.get('ESCROW_PRIVATE_KEY'), algorithm="RS256")

# Generate headers used for authentication
headers = {
    'Authorization': f'Bearer {token}',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15"
}

# Generate Content Encryption Key
generate_content_encryption_key(filename = 'downloads/{cek}.key')

# Download Key Encryption Key
response = requests.get(f'{BASE_URL}/key-encryption-key-download/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID
    },
    timeout = 10
)

print(response.json())

# Download KEK text using response
if response.status_code == 200:
    with open('downloads/{kek}.der', 'w') as kek:
        kek.write(response.json().get('key content'))

# Generate Wrapped Content Encryption Key
generate_wrapped_content_encryption_key('downloads/{cek}.key', 'downloads/{kek}.der', filename = 'downloads/{wkey}.bkenc')

# Upload Wrapped Content Encryption Key
# Requirement: have created a WCEK using the project KEK and a generated CEK
response = requests.post(f'{BASE_URL}/wrapped-content-encryption-key/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'name': '{name}',
        'description': '{description}',
        'version_description': '{version_description}',
        'version_tag': '{version_tag}'
    },
    files = [
        ('file_name', ('downloads/{wkey}.bkenc', open('downloads/{wkey}.bkenc', 'rb')))
    ],
    timeout = 10
)

print(response.json())

# Upload Data Specification
response = requests.post(f'{BASE_URL}/data-specification/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'name': '{name}',
        'description': '{description}',
        'version_description': '{version_description}',
        'version_tag': '{version_tag}'
    },
    files = [
        ('file_name', ('files/{data_specification}.pdf', open('files/{data_specification}.pdf', 'rb')))
    ],
    timeout = 10
)

print(response.json())

# Upload Validation Criteria
response = requests.post(f'{BASE_URL}/validation-criteria/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'name': '{name}',
        'description': '{description}',
        'version_description': '{version_description}',
        'version_tag': '{version_tag}'
    },
    files = [
        ('file_name', ('files/{validation_criteria}.json', open('files/{validation_criteria}.json', 'rb')))
    ],
    timeout = 10
)

print(response.json)

# Encrypt Algorithm
encrypt_algorithm('files/{algorithm}', 'downloads/{cek}.key', filename = 'files/{encrypted_algorithm}.zip')

# Upload Algorithm
# Requirement: an uploaded WCEK, Data Attestation and, if a validation algorithm, Validation Criteria
response = requests.post(f'{BASE_URL}/algorithm/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'name': '{name}',
        'description': '{description}',
        'version_description': '{version_description}',
        'version_tag': '{version_tag}',
        'algorithm_type': 'validation' | 'training',
        'validation_criteria_version': '{validation_criteria_version_tag}',
        'data_attestation_version': '{data_attestation_version_tag}',
        'upload_type': 'Upload Zip',
        'upload_file_name': '{encrypted_algorithm}.zip'
    },
    files = [
        ('file_name', ('files/{encrypted_algorithm}.zip', open('files/{encrypted_algorithm}.zip', 'rb')))
    ],
    timeout = 60
)

print(response.json())

# Create Run Configuration
# Requirement: an uploaded Algorithm and Dataset
response = requests.post(f'{BASE_URL}/run-configuration/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'name': '{name}',
        'algorithm_version': '{algorithm_version_tag}',
        'dataset_version': '{dataset_version_tag}',
        'description': '{description}',
        'run_type': 'validation' | 'training'
    },
    timeout = 10
)

print(response.json())

# Request Run Initiation
# Requirement: an active run configuration
response = requests.post(f'{BASE_URL}/run-request/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'algorithm_version': '{algorithm_version_tag}',
        'dataset_version': '{dataset_version_tag}',
        'machine_type': '{machine}'
    },
    timeout = 10
)

print(response.json())

# Initiate Run
# Requirement: permission for algorithm owner to initiate runs, active run configuration
response = requests.get(f'{BASE_URL}/initiate-run/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'algorithm_version': '{algorithm_version_tag}',
        'dataset_version': '{dataset_version_tag}'
    },
    timeout = 30
)

print(response.json())

# Download Report
# Requirement: a completed run, algorithm owner access to run output
response = requests.get(f'{BASE_URL}/report-download/',
    headers = headers,
    data = {
        'project_id': PROJECT_ID,
        'algorithm_version': '{algorithm_version_tag}',
        'dataset_version': '{dataset_version_tag}'
    },
    timeout = 10
)

print(response.json())

# Download Report text using response
if response.status_code == 200:
    with open('downloads/report.txt', 'w') as report:
        report.write(response.json().get('report content'))
