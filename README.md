# Systemup Shopify Update

## Description
Systemup Shopify Update is a system designed to automatically update information from Shopify using an external API (CT ONLINE).

## Requirements

- **Database**: PostgreSQL:Latest
- **Python**: 3.12

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd systemup-shopify-update
   ```

2. **Install the required dependencies**: Run the following command to install all the dependencies specified in the **requirements.txt** file:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables**: Complete the .env file located in the environment folder with your specific configuration details (such as API keys, database connection strings, etc.).


## Running the Application
To start the application, run the following command:

   ```bash
   python app.py
   ```

## Notes
- Make sure that your PostgreSQL database is set up and running before launching the application.
- Ensure that the external API (CT ONLINE) is accessible and that the API keys are correctly set in the .env file.
