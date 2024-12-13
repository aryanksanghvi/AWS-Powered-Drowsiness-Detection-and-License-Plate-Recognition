#All Libraries to Import
import boto3
import io
import uuid
import cv2
from PIL import Image
from IPython.display import display
from base64 import b64decode
from google.colab.output import eval_js
from datetime import datetime
import boto3
import easyocr
from PIL import Image
import gzip
import base64
from time import time

# Initialize boto3 client for S3
s3 = boto3.client(
    's3',
    aws_access_key_id='Your Access Key',
    aws_secret_access_key='Your Secret Key',
    region_name='Your AWS Region'
)

# Specify the S3 bucket name
bucket_name = 'Your S3 Bucket Name'

def upload_to_s3(image_frame):
    # Convert the image to JPEG format
    _, buffer = cv2.imencode('.jpg', image_frame)
    byte_array = buffer.tobytes()

    # Generate a unique file name for each image
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'captured_image_{current_time}.png'

    #file_name = f'drowsiness_images/{uuid.uuid4().hex}.jpg'

    # Upload to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=byte_array,
        ContentType='image/jpeg'
    )

    print(f"Image uploaded to S3: {file_name}")
def start_license():
   # Initialize the OCR reader for English
  reader = easyocr.Reader(['en'])

  aws_access_key_id = 'Your Access Key'
  aws_secret_access_key = 'Your Secret Key'

  # Initialize AWS clients for DynamoDB, SNS
  dynamodb = boto3.resource(
      'dynamodb',
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      region_name='Your AWS Region'
  )
  sns = boto3.client(
      'sns',
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      region_name='Your AWS Region'
  )

  # DynamoDB table name and SNS topic name
  TABLE_NAME = 'Your Table Name'
  SNS_TOPIC_NAME = 'Your SNS Topic Name'

  # Function to create an SNS topic
  def create_sns_topic():
      try:
          response = sns.create_topic(Name=SNS_TOPIC_NAME)
          topic_arn = response['TopicArn']
          print(f"SNS topic created with ARN: {topic_arn}")
          return topic_arn
      except Exception as e:
          print(f"Error creating SNS topic: {e}")
          return None

  # Function to fetch contact details from DynamoDB using license plate number
  def get_contact_details(license_plate):
      table = dynamodb.Table(TABLE_NAME)
      try:
          response = table.get_item(Key={'LicensePlateNo': license_plate})
          if 'Item' in response:
              contact_details = response['Item']
              print("Contact details found:\n", contact_details)
              return contact_details
          else:
              print("Contact details not found for the given license plate.")
              return None
      except Exception as e:
          print(f"Error fetching data from DynamoDB: {e}")
          return None

  # Function to subscribe contact details to the SNS topic
  def subscribe_to_sns(topic_arn, contact_details):
      email = contact_details.get('Email')
      phone_no = contact_details.get('PhoneNo')

      if email:
          try:
              sns.subscribe(
                  TopicArn='Your Topic ARN',
                  Protocol='email',
                  Endpoint=email
              )
              print(f"Subscribed email {email} to SNS topic.")
          except Exception as e:
              print(f"Failed to subscribe email: {e}")

      if phone_no:
          if not phone_no.startswith("+"):
              phone_no = f"+91{phone_no}"
          try:
              sns.subscribe(
                  TopicArn='arn:aws:sns:ap-south-1:529088285227:LicensePlateAlerts',
                  Protocol='sms',
                  Endpoint=phone_no
              )
              print(f"Subscribed phone number {phone_no} to SNS topic.")
          except Exception as e:
              print(f"Failed to subscribe phone number: {e}")

  # Function to send repeated alert notifications
  def send_alert(topic_arn, license_plate, repetitions=1):
      message = f"URGENT ALERT: CAR WITH LICENSE PLATE: {license_plate} IS IN DANGER, DRIVER IS DROWSY!!! TAKE NECESSARY ACTIONS IMMEDIATELY"

      for i in range(repetitions):
          try:
              response = sns.publish(
                  TopicArn=topic_arn,
                  Message=message,
                  Subject="Car in Danger!!! Car in Danger!!! Car in Danger!!!"
              )
              print(f"Alert {i+1} sent successfully to all subscribers!", response)
          except Exception as e:
              print(f"Failed to send alert {i+1}: {e}")

  # Function to extract license plate number from an image using EasyOCR
  def extract_license_plate_number(image_path):
      results = reader.readtext(image_path)
      if not results:
          print("No text found in the image.")
          return None
      license_plate_text = ''.join([text.replace(" ", "") for _, text, confidence in results if confidence > 0.5])
      if license_plate_text.startswith("IND"):
          license_plate_text = license_plate_text[3:].strip()
      print(f"Extracted License Plate Number: \n{license_plate_text}\n")
      return license_plate_text

  # Main Execution
  image_path = 'Your License Plate Image Path'
  license_plate = extract_license_plate_number(image_path)

  if license_plate:
      contact_details = get_contact_details(license_plate)
      if contact_details:
          topic_arn = create_sns_topic()
          if topic_arn:
              subscribe_to_sns(topic_arn, contact_details)
              send_alert(topic_arn, license_plate, repetitions=1)

def get_frame():
    data = eval_js("capture_frame()")
    binary = b64decode(data.split(",")[1])
    image = Image.open(io.BytesIO(binary))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Load the necessary cascades and model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
model = load_model('Model Training Path')  # Adjust path as needed
Score = 0

# Start video stream
video_stream()

try:
    while True:
        frame = get_frame()
        height, width = frame.shape[0:2]

        # Convert to grayscale for face and eye detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)

        # Draw black rectangle at bottom for text
        cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=3)

            # Detect eyes within the face region
            face_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=1)

            for (ex, ey, ew, eh) in eyes:
                eye = frame[y + ey:y + ey + eh, x + ex:x + ex + ew]
                eye = cv2.resize(eye, (80, 80)) / 255.0
                eye = np.expand_dims(eye, axis=0)  # Prepare for model input

                # Prediction
                prediction = model.predict(eye)

                # If eyes are closed
                if prediction[0][0] > 0.30:
                    cv2.putText(frame, 'closed', (10, height - 20), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
                    Score += 1
                    try:
                        upload_to_s3(frame)
                        # Upload the frame to S3
                    except Exception as e:
                        print(f"Error uploading image to S3: {e}")
                    if Score > 2:
                        print("Drowsy")
                        start_license()
                        break

                # If eyes are open
                else:
                    cv2.putText(frame, 'open', (10, height - 20), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
                    Score -= 1
                    Score = max(0, Score)  # Ensure score doesn't go below zero

                # Display Score
                cv2.putText(frame, 'Score: ' + str(Score), (100, height - 20), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

        # Display the frame
        _, im_buf_arr = cv2.imencode('.jpg', frame)
        display_img = im_buf_arr.tobytes()

        # Display result
        display(Image.open(io.BytesIO(display_img)))
except KeyboardInterrupt:
    print("Stopped.")
