from numpy import empty
import openai
import pytesseract
import cv2
import requests



# Set up OpenAI API credentials
#openai.api_key = "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"


api_url = 'https://api.openai.com/v1/engines'

# Loop until a valid API key is provided
def check_api():
    while True:
        api_key = input('Enter your OpenAI API key: ')

    # Make a GET request to the OpenAI API engines endpoint with the user's API key
        response = requests.get(api_url, headers={'Authorization': 'Bearer ' + api_key})

    # Check the response status code
        if response.status_code == 200:
            print('API key is valid')
            return api_key
            break
        else:
            print('Invalid API key. Please try again.')
 

key=check_api()

openai.api_key = key



# Define function to get prompt from user
def get_prompt():
    prompt = input("Enter your prompt: ")
    return prompt

# Define function to get image from user
def get_image():
    # Load the image
    image_path = input("Enter path to image: ")
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read image file")
        exit()

    # Make a copy of the image for display purposes
    clone = image.copy()

    # Define the ROI coordinates
    x, y, w, h = 0, 0, 0, 0

    # Define the mouse event callback function
    def select_roi(event, x_pos, y_pos, flags, param):
        nonlocal x, y, w, h, clone

        if event == cv2.EVENT_LBUTTONDOWN:
            x, y = x_pos, y_pos

        elif event == cv2.EVENT_LBUTTONUP:
            w, h = x_pos - x, y_pos - y
            cv2.rectangle(clone, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", select_roi)

    while True:
        cv2.imshow("image", clone)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            # Reset the ROI selection
            clone = image.copy()
            x, y, w, h = 0, 0, 0, 0

        elif key == ord("c"):
            # Crop the ROI and apply OCR
            roi = image[y:y+h, x:x+w]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 3)
            text = pytesseract.image_to_string(gray, lang='eng')
            print(text)
            return text

        elif key == 27:
            # Exit the program on ESC
            break

    cv2.destroyAllWindows()

# Ask the user how they want to input the prompt
prompt_option = input("Do you want to enter the prompt manually or select an image to extract text from? Enter 'manual' or 'image': ")

if prompt_option == "manual":
    prompt = get_prompt()
elif prompt_option == "image":
    prompt = get_image()
else:
    print("Invalid option")
    exit()

# Use OpenAI API to get response for the selected text
response=openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[

{"role": "user", "content": prompt},
       
        ]
                                     )


print(response['choices'][0]['message']['content'])
