import boto3
import datetime
import os

ec2 = boto3.client('ec2')
sns = boto3.client('sns')
s3 = boto3.client('s3')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:536697250289:IdleResourceAlerts'
S3_BUCKET = 'smart-cost-analyzer-report'

def lambda_handler(event, context):
    now = datetime.datetime.utcnow()
    report_lines = []
    alert_lines = []

    # 🖥️ Check for EC2 instances in stopped state
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
    )['Reservations']

    for res in instances:
        for instance in res['Instances']:
            instance_id = instance['InstanceId']
            launch_time = instance['LaunchTime'].replace(tzinfo=None)
            age_minutes = (now - launch_time).total_seconds() / 60

            if age_minutes > 5:
                line = f"🖥️ EC2 Idle Instance: {instance_id}, Age: {int(age_minutes)} min"
                report_lines.append(line)
                alert_lines.append(line)

    # 💽 Check for unattached (available) EBS volumes
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']

    for volume in volumes:
        vol_id = volume['VolumeId']
        create_time = volume['CreateTime'].replace(tzinfo=None)
        age_minutes = (now - create_time).total_seconds() / 60

        if age_minutes > 5:
            line = f"💽 Unattached EBS Volume: {vol_id}, Size: {volume['Size']} GB, Age: {int(age_minutes)} min"
            report_lines.append(line)
            alert_lines.append(line)

    # 📝 Save report to S3
    timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
    report_key = f"reports/idle-report-{timestamp}.txt"
    report_body = "\n".join(report_lines) or "✅ No idle EC2 or EBS resources found."

    s3.put_object(Bucket=S3_BUCKET, Key=report_key, Body=report_body)
    print(f"✅ Report saved to s3://{S3_BUCKET}/{report_key}")

    # 📧 Send SNS alert if needed
    if alert_lines:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="🚨 Idle AWS Resources Detected",
            Message="\n".join(alert_lines)
        )
        print("📢 SNS alert sent.")
    else:
        print("👍 No idle resources found. Nothing to alert.")

    return {"statusCode": 200}
