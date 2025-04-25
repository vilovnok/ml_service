from transformers import AutoTokenizer, T5ForConditionalGeneration

chat_checkpoint = 'r1char9/T5_chat'
chat_model = T5ForConditionalGeneration.from_pretrained(chat_checkpoint)
chat_tokenizer = AutoTokenizer.from_pretrained(chat_checkpoint)

text='Что самое главное в человеке ?'

def chat_fun(text: str):
    tokenized_sentence = chat_tokenizer(text, return_tensors='pt', truncation=True)
    res = chat_model.generate(**tokenized_sentence, num_beams=2, max_length=100)            
    return chat_tokenizer.decode(res[0], skip_special_tokens=True)
    

text = chat_fun(text=text)
print(text)