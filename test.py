from transformers import AutoModelForCausalLM, AutoTokenizer

# Cargar el modelo y el tokenizador
model_name = "mbien/recipenlg"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, padding_side="right")
model = AutoModelForCausalLM.from_pretrained(model_name)

def generar_receta(ingredientes):
    # Crear el prompt con los ingredientes
    prompt = f"Ingredients: {', '.join(ingredientes)}\nInstructions:"

    # Asignar el token de padding al token de finalización
    tokenizer.pad_token = tokenizer.eos_token
    
    # Tokenizar con padding y truncamiento
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    
    outputs = model.generate(
        inputs['input_ids'], 
        attention_mask=inputs['attention_mask'],  
        max_length=300, 
        num_return_sequences=1, 
        do_sample=True, 
        temperature=0.7,  # Controla la aleatoriedad
        top_k=50,  # Limita a las 50 palabras más probables
        top_p=0.9,  # Usa nucleus sampling
        pad_token_id=tokenizer.eos_token_id
    )    
    receta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return receta


if __name__ == "__main__":
    # Lista de ingredientes
    ingredientes = ["chicken", "onion", "garlic", "tomato"]

    # Generar la receta
    receta = generar_receta(ingredientes)
    
    # Mostrar la receta generada
    print("Receta generada:")
    print(receta)
