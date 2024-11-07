import ray
import torch
import scipy
import numpy as np
from transformers import AutoTokenizer, VitsModel
from model_config import speech_model_id


@ray.remote
class AudioModelActor:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.speech_tokenizer = AutoTokenizer.from_pretrained(speech_model_id)
        self.speech_model = VitsModel.from_pretrained(speech_model_id).to(self.device)


    def generate_audio(self, text, path="Generated Files\\audio.wav"):
        inputs = self.speech_tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.speech_model(**inputs).waveform

        # Convert the tensor to a NumPy array
        waveform = output.squeeze().cpu().numpy()

        # Ensure the waveform is in the range [-1.0, 1.0]
        max_val = np.max(np.abs(waveform))
        if max_val > 1.0:
            waveform = waveform / max_val

        # Convert to 16-bit PCM format
        waveform_int16 = np.int16(waveform * 32767)

        # Write the WAV file
        scipy.io.wavfile.write(path, rate=self.speech_model.config.sampling_rate, data=waveform_int16)