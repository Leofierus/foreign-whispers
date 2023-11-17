from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration
import os

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def translate_text(text):

    inputs = tokenizer("translate English to French: " + text, return_tensors="pt", padding=True)
    translation_ids = model.generate(inputs.input_ids, num_beams=4, max_length=50, early_stopping=True)
    translated_text = tokenizer.decode(translation_ids[0], skip_special_tokens=True)
    return translated_text

def translate_file(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_name = f"entofr_{base_name}.txt"
    output_path = os.path.join("/Users/rubengarcia/foreign-whispers/translations", output_file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                translation = translate_text(parts[1])
                new_line = parts[0] + ": " + translation + "\n"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

#test the function to prove it works
# example: translate_file("/Users/rubengarcia/foreign-whispers/translations/entofr_test.txt")

