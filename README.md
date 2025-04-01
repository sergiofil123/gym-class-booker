# Gym Class Booker

## Overview

A fully automated AWS Infrastructure as Code (IaC) solution to book gym classes on my behalf.

## Description

At my gym, some classes are in such high demand that spots fill up within minutes of registration opening (24 hours before each class). Every Sunday morning, I used to wake up early just to secure my spot.

Like any **DevOps Engineer** or tech enthusiast, I decided to automate the process. Now, my gym classes are booked automatically while I enjoy my well-deserved sleep.

## Implementation Details

This IaC is deployed in my personal AWS account. In a nutshell:

- **Amazon EventBridge Schedulers** trigger a **Python AWS Lambda function** at the right times.
- The Lambda function interacts with the **Gym's REST API** to book my classes automatically.

## Configuration: What You Need to Change

Before running the automation, update the **variables.tf** file to match your use case:

- **Gym account credentials**
- **User ID and class IDs**, which I retrieved by analyzing the Gym's REST API

## How to Run

I run this automation locally using **OpenTofu**, **AWS CLI**, and **IAM credentials**.

```sh
cd src
tofu init
tofu plan
tofu apply
```

## Future Improvements

There are several potential improvements for this project:

- **Security Enhancements**: Credentials should be stored in **AWS Secrets Manager** instead of plaintext variables. However, since I only use this password for my gym account, the worst thing someone could do is sign me up for Pilates classes. 😅
- **Failure Notifications**: Implementing a notification system via **Amazon SNS** could send alerts via email or SMS in case of booking failures.

Both are valid concerns that might be addressed in the future.

---

💪 **Automate your workouts, so you never miss a class!** 🚀

