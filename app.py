import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Record

load_dotenv()
app = Flask(__name__)

# Load Twilio credentials
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route("/")
def index():
    return "Twilio Transcription Server Running!"

# Call webhook
@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say("Hi. Please answer the following question.")
    response.record(
        max_length=30,
        transcribe=True,
        transcribe_callback="/transcription"
    )
    return str(response)

# Transcription results webhook
@app.route("/transcription", methods=["POST"])
def transcription():
    transcript = request.form.get("TranscriptionText")
    recording_url = request.form.get("RecordingUrl")
    print("📄 Transcript:", transcript)
    print("🔗 Recording:", recording_url)
    return "", 200

# Trigger the call
@app.route("/makecall")
def make_call():
    to_number = "+918008162349"  # Replace with verified number
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        url="http://<your-server-url>/voice"  # use ngrok or Render URL
    )
    return f"Call initiated: {call.sid}"

if __name__ == "__main__":
    app.run(debug=True)
