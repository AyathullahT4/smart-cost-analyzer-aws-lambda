# smart-cost-analyzer-aws-lambda
AWS Lambda tool to detect and report idle EC2 and EBS resources, save reports to S3, and send alerts via SNS to reduce cloud costs.

🧠 Smart Cost Analyzer for Idle AWS Resources
A serverless AWS Lambda tool that automatically identifies idle EC2 instances and unattached EBS volumes, then:

📤 Uploads a detailed report to S3

📧 Sends alert emails via SNS

🚀 Use Case
This tool helps teams:

Detect unused cloud resources
Automate cost-saving recommendations
Integrate alerts into their DevOps workflow

📁 Project Structure

smart-cost-analyzer-aws-lambda/
├── lambda_function.py       # Lambda function code
├── iam-policy.json          # Inline IAM policy for Lambda execution role
├── README.md                # Documentation and usage guide

⚙️ How It Works
Every 5 minutes:

The Lambda function scans:
  EC2 instances in stopped state
  EBS volumes in available state
Filters resources older than 5 minutes
Saves a time-stamped report in your S3 bucket
Publishes alert email via SNS (only if idle resources are found)

🛠️ Technologies Used

AWS Lambda
Amazon EC2 & EBS
Amazon S3
Amazon SNS
IAM Role + CloudWatch Schedule

🔐 IAM Permissions (iam-policy.json)

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "sns:Publish",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
Attach this inline policy to your Lambda role.

🚧 Deployment Steps

✅ Create an S3 bucket named: smart-cost-analyzer-report

✅ Create an SNS topic, subscribe your email

✅ Create an IAM Role for Lambda using iam-policy.json

✅ Deploy lambda_function.py in AWS Lambda (Python 3.12)

✅ Set up CloudWatch Scheduled Rule to run Lambda every 5 minutes

📬 Sample Alert (Email)
![image](https://github.com/user-attachments/assets/6ac82485-5ba8-4efe-b6c4-9f04670bfe24)

🚨 Idle AWS Resources Detected

🖥️ EC2 Idle Instance: i-0893a16f3dxxxxxxx, Age: 47 min
💽 Unattached EBS Volume: vol-03b3xxxxx6da4e, Size: 8 GB, Age: 123 min

📄 Example Report (in S3)
Filename: reports/idle-report-2025-07-07T18-05-00.txt

🖥️ EC2 Idle Instance: i-0abc1234def567890, Age: 85 min
💽 Unattached EBS Volume: vol-0123456789abcdef0, Size: 20 GB, Age: 152 min
📌 Notes
Age threshold is currently hardcoded as 5 minutes for testing. Can be modify this.


Logic can be extended to cover RDS, Load Balancers, Elastic IPs, etc.
