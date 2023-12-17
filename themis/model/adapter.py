import torch
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load LoRA adapter and merge

kwargs = {"device_map": "balanced", "torch_dtype": torch.float16}
max_memory = {"cpu": "20GB"}

base_model = AutoModelForCausalLM.from_pretrained(
    "teknium/OpenHermes-2.5-Mistral-7B",
    return_dict=True,
    torch_dtype=torch.float16,
    # device_map="auto",
    device_map="cpu",
    max_memory=max_memory,
)

tokenizer = AutoTokenizer.from_pretrained("teknium/OpenHermes-2.5-Mistral-7B")
model = PeftModel.from_pretrained(base_model, "gsoaresbaptista/out", offload_folder='./offload')
model = model.merge_and_unload()

model.save_pretrained("OpenHermes-finetuned", safe_serialization=True, max_shard_size='4GB')
tokenizer.save_pretrained("OpenHermes-finetuned")
