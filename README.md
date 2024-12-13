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
![image](https://github.com/user-attachments/assets/465e8e9f-3a5f-43fc-af83-0e0f9af6fc06)

3. License plate details extracted
![image](https://github.com/user-attachments/assets/406bb28c-08b9-4149-bf40-6163d67d5d62)

4. Contact details found in AWS DynamoDB
![image](https://github.com/user-attachments/assets/d4da112e-ea3f-4eb1-91a1-727f5be54deb)
![image](https://github.com/user-attachments/assets/919182f3-14a9-4e4f-8176-0ad3b945bba8)

5. Alert notification sent via AWS SNS
![image](https://github.com/user-attachments/assets/206fadf0-6fcb-4b88-abdc-18d4fa206fb5)
![image](https://github.com/user-attachments/assets/e6d9810e-4ac4-4b4a-a722-0d74362fa3fb)
![image](https://github.com/user-attachments/assets/08cebbe6-df0d-42f5-a683-84cc4fe035cb)
