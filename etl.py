import json
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from ftp_downloader import download_ftp_file

# Load environment variables from .env file
load_dotenv(dotenv_path='./ddbb.env')

# Database connection parameters
CONN_PARAMS = {
    'dbname': os.getenv("DDBB_NAME"),
    'user': os.getenv("DDBB_USER"),
    'password': os.getenv("DDBB_PASSWORD"),
    'host': os.getenv("DDBB_HOST"),
    'port': os.getenv("DDBB_PORT"),
    'client_encoding': 'UTF8'
}

def main(): 
    # Entry point of the program
    data = raw_data_extractor()
    raw_data_transformer(data)

def raw_data_extractor():
    # Extracts raw data from an FTP server
    try:
        print("Downloading new data...")
        download_ftp_file()  
        print("Data downloaded successfully!")
    except Exception as e:
        print(f"Data download failed: {e}")
        raise 
    try:
        products = pd.read_json('products.json')
    except Exception as e:
        print(f"Failed to load JSON data: {e}")
    return products

def raw_data_transformer(products):
    # Transforms the raw data and loads it into the database
    products = raw_data_extractor()
    
    products = products[[
        "idProducto", "clave", "categoria", "descripcion_corta",
        "existencia", "precio", "moneda", "tipoCambio", "imagen"
    ]]

    products = products.rename(columns={
        "idProducto": "id_producto",
        "clave": "clave",
        "categoria": "categoria",
        "descripcion_corta": "descripcion_corta",
        "existencia": "existencia",
        "precio": "precio",
        "moneda": "moneda",
        "tipoCambio": "tipo_cambio",
        "imagen": "imagen_url"
    })

    products['existencia'] = products['existencia'].apply(lambda x: json.dumps(x))

    my_products = data_loader("select")

    # Find the products that do not match between the two dataframes (new_products)
    new_products_to_insert = products[~products['id_producto'].isin(my_products['id_producto'])]

    # See the products that have the same id_producto but different values
    old_products_to_update = products.groupby('id_producto').filter(lambda x: len(x) > 1)

    # Find the duplicates where some column (besides id_producto) has different values
    old_products_to_update = old_products_to_update.drop_duplicates(subset=['id_producto'], keep=False)

    if new_products_to_insert.empty:
        print("No new products to insert.")
    else:
        data_loader("insert", new_products_to_insert)
    
    if old_products_to_update.empty:
        print("No products to update.")
    else:
        data_loader("update", old_products_to_update)

def data_loader(action,data=None):
    # Loads data into the database
    try:
        conn = psycopg2.connect(**CONN_PARAMS)
        cursor = conn.cursor()

        if action not in ['insert', 'update'] or action is "select":
            query = """SELECT * FROM products;"""
            # Execute the select query
            cursor.execute(query)

            # Fetch all the rows
            rows = cursor.fetchall()
            # Save all the rows in a pandas dataframe
            data = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
            data.drop(columns=['id'], inplace=True)
            answer = data


        # Prepare the SQL insert or update query
        products = data
        values = [
            (
                row['id_producto'], row['clave'], row['categoria'], 
                row['descripcion_corta'], row['existencia'], row['precio'], 
                row['moneda'], row['tipo_cambio'], row['imagen_url']
            ) 
            for _, row in products.iterrows()
        ]

        if action == 'insert':
            # Prepare the SQL insert query
            query = """
            INSERT INTO products 
            (id_producto, clave, categoria, descripcion_corta, existencia, precio, moneda, tipo_cambio, imagen_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            message = "New data inserted successfully!"
        
        elif action == 'update':
            # Prepare the SQL update query
            privot_values = values.copy()
            values = [
                (
                    v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[0]
                ) 
                for v in privot_values
            ]

            query = """
            UPDATE products
            SET clave = %s, categoria = %s, descripcion_corta = %s, existencia = %s, precio = %s, moneda = %s, tipo_cambio = %s, imagen_url = %s
            WHERE id_producto = %s;
            """
            message = "Data updated successfully!"
        
        cursor.executemany(query, values)
        conn.commit()
        print(message)
        answer = True

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()  # Rollback the transaction on error

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the cursor and connection are properly closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return answer
