import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def send_email_with_images(to_email, image_paths):
    # 邮箱配置
    from_email = "iot5506group7@gmail.com"
    password = "wtpc sziq upnn jcsp"
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # 创建一个MIMEMultipart对象来表示电子邮件
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "IOT Warning, " + formatted_time

    # 邮件正文
    body = "[[IOT Warning]] We suspect your room has been accessed, please look at the following pictures."
    msg.attach(MIMEText(body, 'plain'))

    # 附加图片
    for image_path in image_paths:
        with open(image_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {image_path.split('/')[-1]}")
            msg.attach(part)

    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # 使用gmail SMTP，可以根据需要更改
        server.starttls()  # 安全连接
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


# check the state
should_send_email = True
user_email_address_list = ["24079194@student.uwa.edu.au"
    , "22478026@student.uwa.edu.au"
    , "23687599@student.uwa.edu.au"
    , "23740033@student.uwa.edu.au"
    , "757434182@qq.com"
                           ]
# image_set = {"image1.jpg", "image2.jpg"}
image_set = {"./picture1.jpg", "./picture2.jpg"}

if should_send_email:
    for user_email in user_email_address_list:
        send_email_with_images(user_email, image_set)
