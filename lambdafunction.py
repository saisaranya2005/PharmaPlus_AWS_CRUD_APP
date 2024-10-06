import json
import boto3
import time
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PharmaPlus')

# Custom JSON encoder to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("Received event: ", event)  # Log the received event for debugging
    try:
        # Check for operation and set default to getMedicines
        operation = event.get('operation', 'getMedicines')  # Default to getMedicines if not present

        if operation == 'addMedicine':
            return saveMedicine(event)
        elif operation == 'deleteMedicine':
            return deleteMedicine(event)
        elif operation == 'updateMedicine':
            return updateMedicine(event)  # Handle update operation
        elif operation == 'getMedicines':  # Explicitly check for getMedicines
            return getMedicines()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Unsupported operation: {operation}')
            }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing parameter: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

# Function to get all medicines
def getMedicines():
    try:
        response = table.scan()  # Scanning the DynamoDB table
        items = response.get('Items', [])  # Fetching the Items array
        return {
            'statusCode': 200,
            'body': json.dumps(items, cls=DecimalEncoder),  # Use the custom encoder
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving medicines: {str(e)}")
        }

# Function to save a new medicine
def saveMedicine(event):
    gmt_time = time.gmtime()
    now = time.strftime('%a %d %b %Y %H:%M:%S', gmt_time)

    try:
        expiry_date = datetime.strptime(event['expiryDate'], '%Y-%m-%d')  # Parse expiry date
        present_date = datetime.now()  # Get current date

        # Calculate days left until expiry
        days_left = (expiry_date - present_date).days

        table.put_item(
            Item={
                'medicineid': event['medicineid'],  # Use medicineid as the partition key
                'medicineName': event['medicineName'],
                'use': event['use'],
                'expiryDate': event['expiryDate'],
                'daysLeft': days_left,  # Store calculated days left
                'createdAt': now
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'Medicine with ID: {event["medicineid"]} created at {now}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error adding medicine: {str(e)}')
        }

# Function to delete a medicine
def deleteMedicine(event):
    medicine_id = event['medicineid']
    
    try:
        response = table.delete_item(
            Key={
                'medicineid': medicine_id  # Use medicineid as the key
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'Medicine with ID: {medicine_id} deleted successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting medicine: {str(e)}')
        }

# Function to update a medicine's details
# Function to update a medicine's details
def updateMedicine(event):
    medicine_id = event['medicineid']
    new_use = event.get('newUse', None)  # Optional parameter for updating use
    new_expiry_date = event.get('newExpiryDate', None)  # Optional parameter for updating expiry date

    update_expression = 'SET'
    expression_attribute_values = {}
    expression_attribute_names = {}

    if new_use is not None:
        update_expression += ' #u = :newUse,'  # Use placeholder for reserved keyword
        expression_attribute_names['#u'] = 'use'  # Map placeholder to actual attribute name
        expression_attribute_values[':newUse'] = new_use  # Define the new use value

    if new_expiry_date is not None:
        update_expression += ' expiryDate = :newExpiryDate,'  # No issue with expiryDate
        expression_attribute_values[':newExpiryDate'] = new_expiry_date

        # Calculate days left for the new expiry date
        expiry_date = datetime.strptime(new_expiry_date, '%Y-%m-%d')  # Parse new expiry date
        present_date = datetime.now()  # Get current date
        days_left = (expiry_date - present_date).days
        expression_attribute_values[':newDaysLeft'] = days_left
        update_expression += ' daysLeft = :newDaysLeft,'

    # Remove the trailing comma
    update_expression = update_expression.rstrip(',')

    try:
        table.update_item(
            Key={
                'medicineid': medicine_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names  # Include the placeholder mapping
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'Medicine with ID: {medicine_id} updated successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error updating medicine: {str(e)}')
        }
