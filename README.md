# PharmaPlus Project

Welcome to the **PharmaPlus** project! 🌿💊 This application is designed to efficiently manage medicine data, providing a user-friendly interface for adding, updating, and deleting medicine information. Below, you’ll find an overview of the AWS services used to develop this full-stack application.

## ☁️ AWS Services Utilized

1. **DynamoDB (Database)**:
   - **Purpose**: Stores medicine data such as Medicine ID, Name, use, expiry date etc.
   - **Functionality**: The Lambda function accesses this table to perform read (Scan) and write (PutItem) operations.

2. **Lambda (Serverless Backend)**:
   - **Purpose**: Contains the logic to interact with DynamoDB, allowing the addition and retrieval of medicine details.
   - **Functionality**: Lambda functions are invoked by API Gateway to perform these operations based on HTTP requests.

3. **API Gateway (REST API)**:
   - **Purpose**: Provides a REST API to access Lambda functions through various HTTP methods (POST, GET).
   - **Functionality**: Acts as an interface between the front-end (HTML/JavaScript) and the Lambda function, relaying user requests to Lambda.

4. **IAM (Access Control)**:
   - **Purpose**: Manages permissions and access control for AWS resources.
   - **Functionality**: IAM roles and policies grant the Lambda function the necessary permissions to read and write data in DynamoDB.

5. **AWS Amplify (Web Hosting)**:
   - **Purpose**: Hosts and deploys the front-end (HTML/JavaScript) of the PharmaPlus application.
   - **Functionality**: Amplify serves the front-end, which interacts with API Gateway to make requests that trigger Lambda functions.

## 📂 Repository Contents

Here’s a quick overview of the files in this repository:

- **index.html**: The main HTML file that serves as the frontend for the PharmaPlus application.
- **lambdafunction.py**: The serverless backend logic that interacts with DynamoDB to manage medicine data.
- **AWS_22BAI1471_APP.pdf**: Documentation related to the AWS setup for this project.
- **Pharmawebsite.pdf**: Additional documentation or reports regarding the PharmaPlus project.


## 💡 Notes for GitHub Users

- Feel free to explore the repository, and if you have any questions or suggestions, don't hesitate to reach out!
- Thank you for checking out the PharmaPlus project! Happy coding! 🚀
