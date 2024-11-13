import json
import os
import mysql.connector
from mysql.connector import Error
import base64
from datetime import datetime

# Environment variables for RDS credentials
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

# Connect to the RDS MySQL database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL", e)
        return None

def lambda_handler(event, context):
    http_method = event.get("httpMethod")
    
    if http_method == "POST":
        return add_data(event)
    elif http_method == "GET":
        return get_data(event)
    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method Not Allowed"})
        }

def add_data(event):
    body = json.loads(event["body"])
    user_id = body.get("user_id")
    config = body.get("config")
    result = body.get("result")
    image_base64 = body.get("image_base64")
    
    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "user_id is required"})
        }

    connection = get_db_connection()
    if not connection:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Database connection failed"})
        }
    
    try:
        cursor = connection.cursor()
        
        # Insert the new record
        cursor.execute("""
            INSERT INTO user_data (user_id, config, result, image_base64) 
            VALUES (%s, %s, %s, %s)
        """, (user_id, config, result, image_base64))
        
        connection.commit()
        
        # Count existing records for the user
        cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id = %s", (user_id,))
        record_count = cursor.fetchone()[0]  # Get the total count of records for this user

        # Delete oldest records if count exceeds the limit (24 records)
        if record_count > 24:
            # Calculate how many excess records to delete
            excess_records = record_count - 24  # Fixed limit of 24
            
            # Delete the oldest records, keeping only the latest 24
            cursor.execute("""
                DELETE FROM user_data 
                WHERE user_id = %s 
                ORDER BY timestamp ASC  -- Oldest records first
                LIMIT %s
            """, (user_id, excess_records))
            connection.commit()  # Commit the deletion
        
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Data added successfully"})
        }
    
    except Error as e:
        print("Error inserting data", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to add data"})
        }
    
    finally:
        cursor.close()
        connection.close()

def get_data(event):
    user_id = event["pathParameters"]["user_id"]

    connection = get_db_connection()
    if not connection:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Database connection failed"})
        }
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Retrieve the latest 24 records for the user
        cursor.execute("""
            SELECT * FROM user_data 
            WHERE user_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 24
        """, (user_id,))
        
        records = cursor.fetchall()
        return {
            "statusCode": 200,
            "body": json.dumps(records, default=str)
        }
    
    except Error as e:
        print("Error retrieving data", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to retrieve data"})
        }
    
    finally:
        cursor.close()
        connection.close()
