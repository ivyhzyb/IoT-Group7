import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def send_email_with_images(to_email, image_paths):
    # Email configuration
    from_email = "iot5506group7@gmail.com"
    password = "wtpc sziq upnn jcsp"
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Create a MIMEMultipart object to represent the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "IOT Warning, " + formatted_time

    # Email body
    body = "[[IOT Warning]] We suspect your room has been accessed, please look at the following pictures."
    msg.attach(MIMEText(body, 'plain'))

    # Attach images
    for image_path in image_paths:
        with open(image_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {image_path.split('/')[-1]}")
            msg.attach(part)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail SMTP, can be changed if needed
        server.starttls()  # Secure connection
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


# Check the state
should_send_email = True
user_email_address_list = [
    "24079194@student.uwa.edu.au",
    "22478026@student.uwa.edu.au",
    "23687599@student.uwa.edu.au",
    "23740033@student.uwa.edu.au",
    "757434182@qq.com"
]

# image paths
image_set = {"./picture1.jpg", "./picture2.jpg"}

if should_send_email:
    for user_email in user_email_address_list:
        print("Sending email to " + user_email)
        send_email_with_images(user_email, image_set)
        print("Email sent to " + user_email)
