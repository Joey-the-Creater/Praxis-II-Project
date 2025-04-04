import requests
import json
import time
def get_brickognize_data(image_path):
    res = requests.post(
        'https://api.brickognize.com/predict/',
        headers={'accept': 'application/json'},
        files={'query_image': ('test.jpg', open(r'Image/test.jpg','rb'), 'image/jpg')},
    )
    try:
        response_data = json.loads(res.content)
    except json.JSONDecodeError:
        response_data = None
        print("Empty response received.")
        return

    def print_first_item(data):
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            name = item.get('name', 'N/A')
            category = item.get('category', 'N/A')
            type_ = item.get('type', 'N/A')
            score = item.get('score', 'N/A')
            print(f"Name: {name}, Category: {category}, Type: {type_}, Score: {score}")
            with open('Image/response.txt', 'w') as f:
                f.write(f"Name: {name}, Category: {category}, Type: {type_}")
            f.close()
        else:
            #print("No items found")
            with open('Image/response.txt', 'w') as f:
                f.write("LEGO not detected")            
            f.close()
    print_first_item(response_data)

if __name__=='__main__':
    t=0
    for i in range(100):
        start_time=time.time()
        get_brickognize_data('Image/test.jpg')
        end_time=time.time()
        t+=(end_time-start_time)
    print("Average time taken for each request: ",t/50)