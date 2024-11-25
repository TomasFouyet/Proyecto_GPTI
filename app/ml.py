import spacy
from transformers import AutoTokenizer, AutoModelForCausalLM

class RecipeModel:
    def __init__(self):
        # Cargar modelo y tokenizador preentrenado
        self.tokenizer = AutoTokenizer.from_pretrained("mbien/recipenlg")
        self.model = AutoModelForCausalLM.from_pretrained("mbien/recipenlg")

        # Agregar token de padding si no existe
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        # Ajustar dimensiones del modelo para incluir el nuevo token
        self.model.resize_token_embeddings(len(self.tokenizer), mean_resizing=False)

    def generate_recipe(self, ingredients: str, max_length: int = 150) -> str:
        # Tokenizar entrada con padding y truncado
        inputs = self.tokenizer.encode(ingredients, return_tensors="pt")

        # Generar receta
        outputs = self.model.generate(
            inputs,
            num_return_sequences=1,
            max_length=150,
            pad_token_id=self.tokenizer.pad_token_id,
            no_repeat_ngram_size=3,
            num_beams=10,
            temperature=0.3,
            do_sample=False
        )

        recipe_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return recipe_text.strip()