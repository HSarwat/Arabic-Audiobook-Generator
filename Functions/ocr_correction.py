import ray
import torch
from model_config import text_model_id, system_prompt
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig



@ray.remote
class TextModelActor:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        self.text_tokenizer = AutoTokenizer.from_pretrained(text_model_id)
        self.text_model = AutoModelForCausalLM.from_pretrained(text_model_id, quantization_config=quantization_config).to(self.device)


    def correct_text(self, text):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        # Prepare inputs for the model
        input_ids = self.text_tokenizer.apply_chat_template(messages, return_tensors="pt", return_dict=True).to(self.device)

        # Generate the assistant's response
        outputs = self.text_model.generate(**input_ids, max_new_tokens=256)

        # Decode the generated tokens
        corrected_text = self.text_tokenizer.decode(outputs[0], skip_special_tokens=True).split("model")[-1]
        print(corrected_text)
        return corrected_text