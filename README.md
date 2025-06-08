# 💎 Advanced Expense Tracker

A multi-user, serverless expense tracker built using AWS services. Users can sign up, sign in, and manage personal expenses with receipt uploads and analytics dashboards. This project extends the foundational serverless architecture by adding authentication, S3 storage, CloudFront delivery, and QuickSight insights.

---

## 🛠 Tech Stack

- ☁️ **AWS Lambda**  
- 🌐 **Amazon API Gateway**  
- 📦 **Amazon DynamoDB**  
- 🛡️ **Amazon Cognito**  
- ☁️ **Amazon S3**  
- 🌍 **Amazon CloudFront**  
- 📊 **Amazon QuickSight (Optional)**  
- 🖥️ **HTML / JavaScript** (frontend)  
- 🐍 **Python** (Lambda functions)  

*Tip: Each item above reflects a core technology used. Feel free to extend as your project evolves!*

---

## 🚀 Features

- Built using AWS services within the Free Tier (Lambda, API Gateway, DynamoDB).  
- Lambda functions add, retrieve, and export expense data per user.  
- Secure multi-user authentication via Amazon Cognito.  
- Receipt image upload and storage in an S3 bucket.  
- Hosted frontend assets on CloudFront for low-latency global delivery.  

---

## 🏗️ Project Architecture
This project follows a serverless architecture using AWS managed services for scalability and cost-efficiency.
![architecture-diagram](assets/architecture-diagram.png)

---

## 🌐 Live Demo
Try it here: [Expense Tracker Web App](https://d1kwramx1iu2rs.cloudfront.net/)

---

## 📂 Project Structure

```
advanced-expense-tracker/
│
├── assets/
│   ├── api-gateway-authorizer.png
│   ├── cognito-user-pool.png
│   ├── dynamodb-table.png
│   ├── lambda-iam-policy.png
│   └── tracker-screenshot-placeholder.png
│
├── backend/
│ ├── AddExpenseFunction.py # Lambda to add a new expense and save to S3
│ ├── GetExpenseFunction.py # Lambda to retrieve expenses from DynamoDB
│ └── ExportExpenseFunction.py # Lambda to export expenses as CSV
│
├── frontend/
│ ├── login.html # Login / Sign-Up page using Cognito
│ └── tracker.html # Dashboard page to add/view expenses
│
├── infrastructure/
│ └── ExpenseTracker_API-prod-oas30.yaml # Exported API Gateway OpenAPI YAML
│
└── README.md # Project overview and instructions

```

---

## ☁️ Infrastructure

- The `infrastructure/ExpenseTracker_API-prod-oas30.yaml` file contains the exported OpenAPI (YAML) configuration for API Gateway. Import this into any AWS account/region to recreate the same endpoints.  
- Amazon Cognito User Pool and App Client handle sign-up, sign-in, and JWT issuance.  
- An S3 bucket (e.g., `expense-tracker-data-ope`) stores JSON expense files and uploaded receipt images.  
- CloudFront distribution serves static frontend assets from S3 with HTTPS and caching.

---

## 🚀 How to Run & Deploy

### 🖥️ Local Testing

1. Open `frontend/login.html` in a modern browser.  
2. Sign up or sign in using an existing Cognito user.  
3. Upon successful login, you will be redirected to `tracker.html`.  
4. On `tracker.html`, enter **User ID**, **Amount**, **Category**, and **Description**, then click **Add Expense**.  
5. Click **View My Expenses** to fetch all items for the provided user ID.

> **Note:** For local testing without AWS resources, some buttons will not work. You can still confirm UI layout and form validation.

---

### 🛠️ Deploy Backend

### 1. **Create DynamoDB Table**

* **Table name:** `Expenses`
* **Partition key:** `userId` (String)
* **Sort key:** `timestamp` (String)

---

### 2. **Deploy Lambda Functions**

Create three AWS Lambda functions using **Python 3.x runtime**:

* `AddExpenseFunction` → handles POST requests
* `GetExpenseFunction` → handles GET requests
* `ExportExpenseFunction` → exports expense data to S3

All function code can be found in the `backend/` folder.

#### ✅ IAM Role

Create a role called `Full_DynamoDB_S3_Access` with the following managed policies:

* `AmazonDynamoDBFullAccess`
* `AmazonS3FullAccess`

⚠️ **Note:** This approach does *not* follow the principle of least privilege but simplifies setup for learning/demo purposes.

---

### 3. **Set Up Amazon Cognito**

* Create a **User Pool** (configure required attributes like `email`)
* Create an **App Client** (no client secret)
* Note your **User Pool ID** and **App Client ID**

In your Lambda functions, extract `userId` from the **JWT token** provided by Cognito.

---

### 4. **Configure API Gateway**

* Create a new **REST API**
* Import the OpenAPI spec from:
  `infrastructure/ExpenseTracker_API-prod-oas30.yaml`

#### 🔧 Setup:

* Enable **CORS** for all methods (`POST /expenses`, `GET /expenses`, `GET /export-expenses`)

* Set **Authorization** for endpoints:

  * Use **Cognito User Pool Authorizer**
  * Set **Token Source** to `Authorization` header

* **Throttling:**

  * Configure **Stage-level throttling** to limit request rates (recommended defaults: 100 RPS, 200 burst)

* Deploy the API to a stage (e.g., `prod`)

* Note your **Invoke URL**

---

### 5. **Create S3 Buckets**

#### 🔹 `user-expense-tracker-data`

* Used to store JSON data exported by Lambda
* **No public access**
* Provide permissions to:

  * Allow Lambda to put objects
  * Allow Amazon QuickSight to read objects
* ✅ Apply an appropriate bucket policy with `quicksight.amazonaws.com` as the principal
* 🔐 Make sure to set `aws:SourceAccount` to your AWS account ID

#### 🔹 `user-expense-tracker-frontend`

* Stores static files (`login.html`, `tracker.html`)
* **Public read access** to allow browsers to fetch assets
* (Optional) Enable **versioning** to maintain access to previous HTML versions

---

### 6. **Set Up CloudFront**

* Create a CloudFront distribution pointing to the `user-expense-tracker-frontend` S3 bucket
* Set origin to **static website hosting endpoint** or use **Origin Access Identity (OAI)**
* Configure the following:

  * **Redirect HTTP to HTTPS**
  * **Public access** (no WAF)
  * **Restrict geo-location** to **North America and Europe** to stay within AWS free tier

---

### 7. **Configure QuickSight (Optional)**

* Create a new dataset using **S3 as source**
* Point to the `user-expense-tracker-data` bucket or a specific folder prefix
* Build dashboards to visualize:

  * Spending over time
  * Category-based breakdowns
  * CSV/JSON exports

---

## 💡 Host Frontend

1. Upload `login.html` and `tracker.html` to your S3 bucket under a folder (e.g., `public/`).  
2. If using CloudFront, set the bucket’s **static website hosting** or configure an Origin Path to serve these HTML files.  
3. Ensure CORS settings on S3 allow your API’s domain to be called from these pages.  
4. Update the JavaScript in both HTML files to point `fetch` calls to your API Gateway Invoke URL.  

---

### 🧪 Local UI Preview

Here’s a snapshot of the Tracker Dashboard when viewing expenses:

![Tracker Dashboard Screenshot](assets/tracker-screenshot-placeholder.png)

---

## 📬 Contact

Ope – Aspiring Cloud Support Specialist  
[LinkedIn](https://linkedin.com/in/oshinyemio) | [oshinyemio@gmail.com](mailto:oshinyemio@gmail.com)

---

## 📜 License

This project is licensed under the MIT License.
