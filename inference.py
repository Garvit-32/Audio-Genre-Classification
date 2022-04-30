import librosa
import torchaudio


import numpy as np
import torch
from transformers import Wav2Vec2FeatureExtractor
# from transformers import AutoConfig, Wav2Vec2FeatureExtractor
from model import Wav2Vec2ForSpeechClassification


import os


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "6"


# file_path = 'Data/genres_original/pop/pop.00048.wav'


model_name_or_path = "saved_data/wav2vec2-base-100k-voxpopuli-gtzan-music/checkpoint-7900"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# config = AutoConfig.from_pretrained(model_name_or_path)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
    model_name_or_path)
# sampling_rate = feature_extractor.sampling_rate
model = Wav2Vec2ForSpeechClassification.from_pretrained(
    model_name_or_path).to(device)


label_dict = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco',
              4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}
label_names = list(label_dict.values())


def predict(file_path):
    target_sr = feature_extractor.sampling_rate
    speech_array, sampling_rate = torchaudio.load(file_path)
    speech_array = speech_array.squeeze().numpy()
    speech_array = librosa.resample(np.asarray(
        speech_array), orig_sr=sampling_rate, target_sr=target_sr)
    features = feature_extractor(
        speech_array, sampling_rate=target_sr, return_tensors="pt", padding=True)
    input_values = features.input_values.to(device)

    with torch.no_grad():
        logits = model(input_values).logits

    pred_ids = torch.argmax(logits, dim=-1).detach().cpu().numpy()
    genre = label_names[pred_ids[0]]

    return genre


# label_names = [config.id2label[i] for i in range(config.num_labels)]

# label_names = [config.id2label[i] for i in range(config.num_labels)]


# y_true = [config.label2id[name] for name in result["label"]]
# y_pred = result["predicted"]

# print(y_true[:5])
# print(y_pred[:5])
