def translate_text(txt, tokenizer, model):
    input_ids = tokenizer.encode(txt, return_tensors="pt")
    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded
