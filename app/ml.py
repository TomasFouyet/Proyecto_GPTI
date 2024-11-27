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
    

    def generate_recipe(self, ingredients: list, max_length: int = 150) -> str:
        # Tokenizar entrada con padding y truncado
        print(ingredients)
        ingredients_formatted = "<INPUT_START> " + " <NEXT_INPUT> ".join(ingredients) + " <INPUT_END>"
        print(ingredients_formatted)
        inputs = self.tokenizer.encode(ingredients_formatted, return_tensors="pt")
        print(inputs)
        # Generar receta
        outputs = self.model.generate(
            inputs,
            num_return_sequences=1,
            max_length=300,
            pad_token_id=self.tokenizer.pad_token_id,
            no_repeat_ngram_size=3,
            num_beams=6,
            temperature=1,
            do_sample=True
        )
        recipe_text = self.tokenizer.decode(outputs[0])
           # Truncar después del primer <TITLE_END>
        print(recipe_text)
        if "<TITLE_END>" in recipe_text:
            recipe_text = recipe_text.split("<TITLE_END>")[0] + "<TITLE_END>"
        # Remover todos los tokens
        lista_tokens = ["<RECIPE_START>", "<INPUT_START>", "<NEXT_INPUT>", "<INPUT_END>", "<TITLE_START>", "<TITLE_END>", "<INGR_START>", "<NEXT_INGR>", "<INGR_END>", "<INSTR_START>", "<NEXT_INSTR>", "<INSTR_END>", "<RECIPE_END>", "\t", "\n"]
        for token in lista_tokens:
            recipe_text = recipe_text.replace(token, "")
        # Remover espacios duplicados
        
        
        
        return recipe_text.strip()
