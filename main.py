import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
import smtplib
import random
from faker import Faker
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def voice_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Now:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return None

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def detect_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Face Detected! Press 'q' key to start the interview.", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('Face Detection', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') and len(faces) > 0:  # Check if 'q' is pressed and faces are detected
            cv2.imwrite('detected_face.jpg', frame)

            # Email configuration
            sender_email = "bhargav3516@gmail.com"
            receiver_email = "bhargav3516@gmail.com"
            subject = "face of the person"
            body = "Body of the email"

            # Create a MIME object
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Attach text to the email
            message.attach(MIMEText(body, "plain"))

            # Attach image to the email
            with open("detected_face.jpg", "rb") as image_file:
                image = MIMEImage(image_file.read())
                message.attach(image)

            # Connect to the SMTP server
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "bhargav3516@gmail.com"
            smtp_password = "ggzu uhds kzbs dcyd"

            # Start the SMTP session
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)

                # Send the email
                server.sendmail(sender_email, receiver_email, message.as_string())

            print("\nDetection is completed and processed")
            speak_text("Detection is completed and processed")

            cap.release()
            cv2.destroyAllWindows()
            return True
        
def get_name():
    print("\nFace detection starting...")
    speak_text("Face detection starting...")
    face_detected = detect_face()

    if face_detected:
        print("\nFace detected! Starting the interview.")
        speak_text("Face detected! Starting the interview.")
        print("\nBefore we begin, may I know your name?")
        speak_text("Before we begin, may I know your name?")

        print("Please type your name and press Enter:")
        name = input().strip()

        if name:
            print("Hello, {}! Let's start the interview.".format(name))
            speak_text(f"Hello, {name}! Let's start the interview.")
            return name.lower()
        else:
            print("No name provided.")
    return None

def generate_random_username():
    fake = Faker()
    random_username = fake.user_name()
    return random_username

def generate_random_password():
    # Generate a random password
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_password = ''.join(random.choice(characters) for i in range(8))
    return  random_password

def interviewer_login():

    correct_username = generate_random_username() 
    correct_password = generate_random_password()
    # Email Sending
    speak_text("Enter your email address")
    recipient_email = input("Enter your email address: ")

    # Set your email and password
    sender_email = "bhargav3516@gmail.com"
    sender_password = "ggzu uhds kzbs dcyd"

    # Set up the MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Interview PassKey"

    # Add the email body
    body = f"Dear Interviewee \n\nHere is your username and password for the interview: \n\nUsername:{correct_username}\nPassword:{correct_password} \nGood Luck on your interview."
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Start TLS for security
        server.starttls()

        # Login to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

    print(f"\nInterview PassKey is sent to {recipient_email} successfully.")
    speak_text(f"Interview PassKey is sent to {recipient_email} successfully.")

    print("Interviewer, please login:")
    speak_text("Interviewer, please login:")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == correct_username and password == correct_password:
        print("Login successful! You  now will attend the interview.")
        speak_text("Login successful! You  now will attend the interview.")
        return True
    else:
        print("Login failed. Exiting program.")
        speak_text("Login failed. Exiting program.")
        return False


def quiz(stage_questions, stage_name):
    score = 0

    for i, question in enumerate(stage_questions, start=1):
        print(f"\n{stage_name} - Question {i}: {question['question']}")
        speak_text(f"{stage_name}, question {i}: {question['question']}")

        user_answer = voice_to_text()

        if user_answer:
            speak_text(f"You said: {user_answer}")

            if user_answer == question['answer']:
                speak_text("Correct!")
                score += 1
            else:
                speak_text(f"Wrong! The correct answer is: {question['answer']}")

    print(f"\n{stage_name} completed.")
    speak_text(f"{stage_name} completed.")

    return score

if __name__ == "__main__":
    interviewer_logged_in = interviewer_login()

    if interviewer_logged_in:
        name = get_name()

        if name:
            # First Stage
            print(f"\n{name}, let's move to the first stage of the interview.")
            speak_text(f"{name}, let's move to the first stage of the interview.")

            questions_stage1 = [
                {"question": "Flow of electrons is generally termed as ?", "answer": "electric current"},
                {"question": "R-C oscillators are usually used in which range of frequency?", "answer": "audio frequency"},
                {"question": "The ripple factor of a half-wave rectifier is ?", "answer": "1.21"},
                {"question": "What is the wave used in optical fibre ?", "answer": "Light"},
                {"question": "What is full form of IP ?", "answer": "internet protocol"},
            ]

            score_stage1 = quiz(questions_stage1, "Stage 1")

            if score_stage1 > 2:
                # Second Stage
                print("\nCongratulations! You have qualified for the second stage of the interview.")
                speak_text("Congratulations! You have qualified for the second stage of the interview.")
                print(f"\n{name}, let's move to the second stage of the interview.")
                speak_text(f"{name}, let's move to the second stage of the interview.")
                questions_stage2 = [
                    {"question": "Which language is the backbone of a webpage ?", "answer": "html"},
                    {"question": "Javascript is which type of language?", "answer": "high end"},
                    {"question": "What does SDLC stands for?", "answer": "software development life cycle"},
                ]

                score_stage2 = quiz(questions_stage2, "Stage 2")

                if score_stage2 > 1:
                    print("\nCongratulations! You have successfully completed stages for the HR round, further information will be sent to your mail.")
                    speak_text("Congratulations! You have successfully completed stages for the HR round, further information will be sent to your mail.")

                    # Email Sending
                    speak_text("Enter your email address")
                    recipient_email = input("Enter your email address: ")

                    # Set your email and password
                    sender_email = "bhargav3516@gmail.com"
                    sender_password = "ggzu uhds kzbs dcyd"

                    # Set up the MIME object
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = recipient_email
                    message["Subject"] = "Interview Details"

                    # Add the email body
                    body = f"Dear {name},\n\nCongratulations on successfully completing A.I interview stages! \nYou have been selected for the HR round and we are glad to confirm Google Meet Interview with you. \n\nDate: 19^th FEB 2024 \nTime: 4:00 PM - 4:40 PM. \n\nHere is the meeting link : https://meet.google.com/dby-vmdj-xwa"
                    message.attach(MIMEText(body, "plain"))

                    # Connect to the SMTP server
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        # Start TLS for security
                        server.starttls()

                        # Login to the email account
                        server.login(sender_email, sender_password)

                        # Send the email
                        server.sendmail(sender_email, recipient_email, message.as_string())

                    print(f"\nInterview details sent to {recipient_email} successfully.")
                    speak_text(f"Interview details sent to {recipient_email} successfully.")
                else:
                    print("\nSorry, you did not qualify for the job. Better luck next time!")
                    speak_text("Sorry, you did not qualify for the job. Better luck next time!")
            else:
                print("\nSorry, you did not qualify for the job. Better luck next time!")
                speak_text("Sorry, you did not qualify for the job. Better luck next time!")