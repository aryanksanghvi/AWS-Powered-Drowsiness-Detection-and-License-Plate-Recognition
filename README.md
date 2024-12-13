# AWS-Powered-Drowsiness-Detection-and-License-Plate-Recognition
Using AWS to integrate Drowsiness Detection and License Plate Recognition
Use this google drive link to download the trained model https://drive.google.com/file/d/1JzDVxTpeeNdpAFOwvgz6YQc-rRVubUYW/view?usp=sharing

Camera is used to capture the live feed. The model then analyzes each frame to detect if the person is drowsy or not.
These images are stored in AWS S3.
If the person is detected as drowsy, the license plate recognition system works. 
It extracts the license plate details from the image using OCR
The vehicle owner contact details are stored in Amazon DynamoDB. It gets extracted and then SNS notifications are sent as Email and Phone.
Python is the language used.

Screenshots:
1. Person detected as drowsy:

![image](https://github.com/user-attachments/assets/9dacde25-266f-44a0-86b0-fb35ad132d2b)

2. Image uploaded to AWS S3

![image](https://github.com/user-attachments/assets/a577a746-a9b5-441f-b78d-a9e5479afdbb)

3. License plate details extracted
   
![image](https://github.com/user-attachments/assets/5786be4d-4ec0-4764-82d4-75c68fb9dbb4)

4. Contact details found in AWS DynamoDB

![image](https://github.com/user-attachments/assets/e17bf5cc-76c2-489f-b52b-ebeae4782759)

![image](https://github.com/user-attachments/assets/2d010390-73d7-4765-b9ed-16df9f98a95b)

5. Alert notification sent via AWS SNS

![image](https://github.com/user-attachments/assets/354c8510-849b-42a5-b9d6-a3eeb46b437e)

![image](https://github.com/user-attachments/assets/261b3c84-a00c-46e4-b3df-900189d9d3d4)

![image](https://github.com/user-attachments/assets/08cebbe6-df0d-42f5-a683-84cc4fe035cb)
