from flask import Flask, request, jsonify,send_file
import requests
from user_agent import generate_user_agent
app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    
    # تحقق من أن الوصلة تحتوي على الرابط الصحيح للفيديو في Instagram
    if 'instagram.com/reel' not in url:
        return jsonify({'error': 'Invalid Instagram reel URL'})
    
    try:
        # استدعاء الرابط الفعلي للفيديو
        headers = {
'authority': 'reelsaver.net',
'accept': '*/*',
'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'origin': 'https://reelsaver.net',
'referer': 'https://reelsaver.net/download-reel-instagram',
'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
'sec-ch-ua-mobile': '?1',
'sec-ch-ua-platform': '"Android"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': generate_user_agent(),
'x-requested-with': 'XMLHttpRequest',
}#@Crrazy_8 & @BRoK8
        data = {
    'via': 'form',
    'ref': 'download-reel-instagram',
    'url': url,}
        respons = requests.post('https://reelsaver.net/api/instagram', headers=headers, data=data).json()
        video_url= respons["data"]['medias'][0]['src']
    	
        response = requests.get(video_url, stream=True)
        
        # حفظ الفيديو على القرص المحلي بواسطة Flask
        with open('video.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        return jsonify({'url':video_url})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()