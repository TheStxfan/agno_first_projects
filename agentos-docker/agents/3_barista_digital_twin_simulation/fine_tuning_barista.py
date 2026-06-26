from unsloth import FastLanguageModel
import os
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import torch

# --- 1. CONFIGURAZIONE ELEMENTI CHIAVE ---
max_seq_length = 2048  # Lunghezza massima del contesto di chat
DATASET_FILE = "agents/3_barista_digital_twin_simulation/barista_chat_dataset.jsonl"
OUTPUT_DIR = "agents/3_barista_digital_twin_simulation/outputs_barista"

# Scegliamo un modello di partenza leggero e potente (es. Llama-3 8B Instruct)
# Unsloth scaricherà automaticamente la versione ottimizzata per consumare meno VRAM
model_name = "unsloth/llama-3-8b-Instruct-bnb-4bit" 

print("Caricamento del modello e del tokenizer ottimizzati Unsloth...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    load_in_4bit=True, # Carica in 4-bit per risparmiare l'80% di memoria VRAM
    dtype=None,        # Rileva automaticamente se usare Float16 o Bfloat16
)

# --- 2. CONFIGURAZIONE LORA PER IL FINE-TUNING ---
# Prepariamo il modello per aggiornare solo i moduli di attenzione
model = FastLanguageModel.get_peft_model(
    model,
    r=16, # Rank di LoRA (valori tipici: 8, 16, 32, 64)
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0, 
    bias="none",    
    use_gradient_checkpointing="unsloth", # Riduce l'uso di VRAM per contesti lunghi
    random_state=3407,
    use_rslora=False,
    # loftq=None,
)

# --- 3. CARICAMENTO DEL DATASET JSONL LOCALE ---
print(f"Caricamento del dataset locale: {DATASET_FILE}...")
# Carichiamo il file generato da SQLite direttamente dal disco
dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

# Applichiamo il Chat Template standard al dataset.
# Questo dice al tokenizer come formattare i ruoli 'user' e 'assistant' nel prompt dell'LLM
def formatting_prompts_func(examples):
    convs = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convs]
    return { "text" : texts }

dataset = dataset.map(formatting_prompts_func, batched=True)

# --- 4. CONFIGURAZIONE PARAMETRI DI ADDESTRAMENTO ---
print("Configurazione del Trainer...")
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False, # False è ideale per dataset di conversazioni brevi (come al bar)
    args=TrainingArguments(
        per_device_train_batch_size=2, # Abbassa a 1 se vai fuori memoria (OOM)
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,                  # Numero di step di addestramento (regolalo in base al dataset)
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        output_dir=OUTPUT_DIR,
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
    ),
)

# --- 5. AVVIO FINE-TUNING ---
print("Avvio dell'addestramento locale in corso...")
trainer_stats = trainer.train()

# --- 6. SALVATAGGIO DEI PESI ---
print(f"Salvataggio dei pesi addestrati (LoRA Adapters) in {OUTPUT_DIR}...")
model.save_pretrained_merged(OUTPUT_DIR, tokenizer, save_method="lora")
print("Fatto! Il tuo barista AI locale è pronto.")