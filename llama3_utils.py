import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def build_prompt(fewshot_examples, test_transcription):
    prompt = ""
    for ex in fewshot_examples:
        prompt += f"Transcrição: {ex['transcript']}\nRelatório JSON: {ex['report']}\n\n"
    prompt += f"Transcrição: {test_transcription}\nRelatório JSON:"
    return prompt.strip()


def load_fewshot_examples(jsonl_path, num_shots=3):
    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]
    sampled = random.sample(lines, num_shots)
    return [
        {
            "transcript": ex["prompt"].replace("Transcrição: ", "").split("\nGere o relatório")[0].strip(),
            "report": ex["completion"]
        }
        for ex in sampled
    ]


def extract_json(text):
    start = text.find('{')
    if start == -1:
        return None

    open_braces = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            open_braces += 1
        elif text[i] == '}':
            open_braces -= 1
            if open_braces == 0:
                try:
                    candidate = text[start:i+1]
                    json.loads(candidate)
                    return candidate
                except json.JSONDecodeError:
                    break
    return None


def generate_report(
    transcription,
    jsonl_path,
    model_name="MBZUAI/LaMini-Flan-T5-248M",  # ✅ Small, fast, no-auth
    num_shots=3,
    max_new_tokens=512
):
    print("🔍 Generating report for input transcription...")
    fewshots = load_fewshot_examples(jsonl_path, num_shots)
    prompt = build_prompt(fewshots, transcription)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids.to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.pad_token_id,
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    json_report = extract_json(decoded)

    if json_report:
        print("\n✅ Generated JSON Report:\n")
        print(json_report)
        with open("generated_report.json", "w", encoding="utf-8") as f:
            f.write(json_report)
    else:
        print("⚠️ Could not extract valid JSON from the model output.")
        with open("generated_report.json", "w", encoding="utf-8") as f:
            f.write("")

    return json_report


# Optional local test
if __name__ == "__main__":
    transcription_text = "Transcrição: ... (your input here)"
    fewshot_jsonl_path = "few_shot_learning_data.jsonl"
    generate_report(transcription_text, fewshot_jsonl_path)
