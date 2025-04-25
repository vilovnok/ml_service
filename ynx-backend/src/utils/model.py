from transformers import AutoTokenizer, T5ForConditionalGeneration, AutoModelForSequenceClassification, pipeline
from huggingface_hub import login

from config import MODEL_ID_CHAT, MODEL_ID_CLS


login(token='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')

chat_model = T5ForConditionalGeneration.from_pretrained(MODEL_ID_CHAT)
chat_tokenizer = AutoTokenizer.from_pretrained(MODEL_ID_CHAT)    

cls_tokenizer = AutoTokenizer.from_pretrained(MODEL_ID_CLS)
cls_model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID_CLS)
new_labels = {0: 'не убедил', 1: 'убедил'}
cls_model.config.id2label = new_labels
cls_model.config.label2id = {v: k for k, v in new_labels.items()}


def chat_fun(message: str):
    tokenized_sentence = chat_tokenizer(message, return_tensors='pt', truncation=True)
    res = chat_model.generate(**tokenized_sentence, num_beams=2, max_length=100)  
    return chat_tokenizer.decode(res[0], skip_special_tokens=True)

def topUp_fun(message: str):      
    pipe = pipeline('text-classification', model=cls_model, tokenizer=cls_tokenizer, device='cpu')
    return pipe(message)
