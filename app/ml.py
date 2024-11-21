import spacy
from transformers import AutoTokenizer, AutoModelForCausalLM

class RecipeModel:
    def __init__(self):
        # Cargar el modelo RecipeNLG desde Hugging Face
        self.tokenizer = AutoTokenizer.from_pretrained("mbien/recipenlg")
        self.model = AutoModelForCausalLM.from_pretrained("mbien/recipenlg")

        # Agregar un token especial de padding si no existe
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})

    def generate_recipe(self, ingredients: str, max_length: int = 300) -> str:
        # Aumentar max_length a 300 para generar recetas más largas
        inputs = self.tokenizer(ingredients, return_tensors="pt", padding=True)
        attention_mask = inputs['attention_mask']
        
        # Generar la receta utilizando RecipeNLG con parámetros adicionales
        outputs = self.model.generate(
            inputs['input_ids'],
            attention_mask=attention_mask,
            max_length=max_length,
            pad_token_id=self.tokenizer.pad_token_id,
            no_repeat_ngram_size=3,  # Evita repeticiones
            num_beams=3,             # Aumenta la calidad de generación
            temperature=0.7,         # Controla la aleatoriedad
            top_p=0.9,               # Usa nucleus sampling
            do_sample=True
        )
        
        recipe_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return recipe_text.strip()

