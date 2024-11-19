import pymysql
import json

# Hardcoded database connection details
RDS_HOST = "mysql-rds-g09.cbk2ewumyiw9.ap-southeast-1.rds.amazonaws.com"  # Replace with your actual RDS endpoint
DB_USERNAME = "admin"  # Replace with your actual database username
DB_PASSWORD = "group9login"  # Replace with your actual database password
DB_NAME = "new_schema"  # Replace with your actual database name

def lambda_handler(event, context):
    try:
        print("Connecting to RDS instance...")
        connection = pymysql.connect(
            host=RDS_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            connect_timeout=5
        )
        print("Connection established.")

        # Sample query to test the connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'Connection successful!'")
            result = cursor.fetchone()
        
        # Close the connection
        connection.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps(result[0])
        }
    
    except pymysql.MySQLError as e:
        print("ERROR: Could not connect to MySQL instance.")
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps("Database connection failed")
        }
