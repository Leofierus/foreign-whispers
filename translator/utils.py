from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration
import os

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")


def translate_text(text, target):
    inputs = tokenizer("translate English to " + target + ": " + text, return_tensors="pt", padding=True)
    translation_ids = model.generate(inputs.input_ids, num_beams=4, max_length=50, early_stopping=True)
    translated_text = tokenizer.decode(translation_ids[0], skip_special_tokens=True)
    return translated_text


def translate_file(file_path, target):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_name = f"{base_name}_{target}.txt"
    output_path = os.path.join("media", output_file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if '##' in line:
            new_lines.append(line)
        elif line == '\n':
            new_lines.append(line + '\n')
        else:
            translation = translate_text(line, target)
            new_lines.append(translation)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

    return output_path
