import requests
import json
def get_brickognize_data(image_path):
    res = requests.post(
        'https://api.brickognize.com/predict/',
        headers={'accept': 'application/json'},
        files={'query_image': ('test.jpg', open(r'c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/test.jpg','rb'), 'image/jpg')},
    )
    response_data = json.loads(res.content)

    def print_first_item(data):
        if 'items' in data and len(data['items']) > 0:
            print(json.dumps(data['items'][0], indent=4))
        else:
            print("No items found")

    print_first_item(response_data)

