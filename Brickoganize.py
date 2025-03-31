import requests
import json
import time
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

if __name__=='__main__':
    t=0
    for i in range(100):
        start_time=time.time()
        get_brickognize_data('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/test.jpg')
        end_time=time.time()
        t+=(end_time-start_time)
    print("Average time taken for each request: ",t/50)