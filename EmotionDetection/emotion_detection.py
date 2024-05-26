import json
import requests

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyse } }
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(url, json = myobj, headers=headers)

    try:
        response = requests.post(url, json=myobj, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        formatted_response = json.loads(response.text)
        if response.status_code == 200:
            anger = formatted_response['emotionPredictions'][0]['emotion']['anger']
            disgust = formatted_response['emotionPredictions'][0]['emotion']['disgust']
            fear = formatted_response['emotionPredictions'][0]['emotion']['fear']
            joy = formatted_response['emotionPredictions'][0]['emotion']['joy']
            sadness = formatted_response['emotionPredictions'][0]['emotion']['sadness']
            emotion_scores = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            emotion_scores.update({'dominant_emotion' : dominant_emotion})
            return emotion_scores

        elif response.status_code == 500:
            anger = None
            disgust = None
            fear = None
            joy = None
            sadness = None
            dominant_emotion = None
            return {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'dominant_emotion': dominant_emotion
            }
    
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    except json.JSONDecodeError:
        return {'error': 'Error decoding the JSON response'}
    except KeyError:
        return {'error': 'Unexpected response structure'}
    return response.text
