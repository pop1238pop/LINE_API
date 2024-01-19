from uvicorn import Server, Config
from fastapi import FastAPI, Request, Depends
from starlette.middleware.cors import CORSMiddleware
import os
from fastapi.responses import JSONResponse
from yolofastapi.routers import yolo
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
app = FastAPI()

# Replace YOUR_CHANNEL_ACCESS_TOKEN and YOUR_CHANNEL_SECRET with your actual Line Bot credentials
CHANNEL_ACCESS_TOKEN = "NXPZK6DUO2XBHZ50aea7aOuXyZeGSxMjo2/OoDQ8unQL3jpsEGOjkq12PFurLHC3U7O1q/vqtxzETOIo0ptBZPp3m7qjtNVkYoZ+3+kZfFfV91HazW/m1mYEV/pgehSJouDtQZc4cWqNrT9mUTyYeQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "224ef83e27180960722019da70d1faf9"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yolo.router)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    # Validate the signature
    hash = hmac.new(channel_secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature_calculated = base64.b64encode(hash).decode('utf-8')
    if signature_calculated != signature:
        print('Invalid signature')
        abort(401)

    events = json.loads(request.data)['events']

    try:
        # Process each event
        for event in events:
            handle_event(event)

        # Send success response
        return 'OK'
    except Exception as e:
        print('Error in webhook processing:', e)
        abort(500)
#53
def handle_event(event):
    try:
        print('Handling event:', event)

        if event['type'] == 'message' and event['message']['type'] == 'image':
            print('Processing image message')
            image_url = get_image_url(event['message']['id'])
            species = predict_species(image_url)

            # Replace 'YOUR_REPLY_TOKEN' with the actual reply token
            reply_token = event['replyToken']
            reply_message(reply_token, f'The predicted species is: {species}')
        else:
            print('Unsupported event type or message type')
            reply_message(event['replyToken'], 'Sorry, I can only process image messages.')
    except Exception as e:
        print('Error handling event:', e)
        reply_message(event['replyToken'], f'An error occurred while processing the message: {str(e)}')

def get_image_url(message_id):
    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'https://api.line.me/v2/bot/message/{message_id}/content', headers=headers)
        
        image_path = 'uploads/image.jpg'
        with open(image_path, 'wb') as f:
            f.write(response.content)

        print('Image saved at:', image_path)

        return image_path
    except Exception as e:
        print('Error getting image URL:', e)
        raise e

def predict_species(image_url):
    try:
        print('Predicting species for image:', image_url)

        # Perform species prediction logic here using image_url

        # Replace the following line with your actual logic
        return 'Sample Species'
    except Exception as e:
        print('Error predicting species:', e)
        raise e

def reply_message(reply_token, text):
    # Implement your reply logic here using the LINE Messaging API
    pass


if __name__ == "__main__":
    port = int(os.getenv("PORT", 80))
    uvicorn_params = {"host": "0.0.0.0", "port": port}
    uvicorn_cmd = f"uvicorn {__name__.split('.')[0]}:app {' '.join([f'--{key}={value}' for key, value in uvicorn_params.items()])}"
    os.system(uvicorn_cmd)