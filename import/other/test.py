import re

def parse_syntax(text, keywords):
    try:
        # Define el patrón de búsqueda para los campos entre comillas dobles
        pattern = r'"([^"]+)"|(\b\w+\b)'
        # Busca todas las coincidencias en el texto
        matches = re.findall(pattern, text)
        
        # Encuentra las posiciones de las keywords en los matches
        keyword_indices = []
        for keyword in keywords:
            for i, match in enumerate(matches):
                if match[1] == keyword:
                    keyword_indices.append(i)
                    break

        # Verifica que las keywords estén en el orden especificado
        if keyword_indices != sorted(keyword_indices): raise SyntaxError

        # Divide las coincidencias antes y después de las keywords
        parsed_groups = []
        start_index = 0
        for index in keyword_indices:
            before_keyword = [match[0] for match in matches[start_index:index] if match[0]]
            parsed_groups.append(before_keyword)
            start_index = index + 1

        # Agrega las coincidencias después de la última keyword
        after_last_keyword = [match[0] for match in matches[start_index:] if match[0]]
        parsed_groups.append(after_last_keyword)

        return parsed_groups
    
    except: raise SyntaxError

# Ejemplo de uso
texto = '"valor1" "valor2" keyword1 "keyword2" "valor3" keyword2 "valor4" "valor5"'
keywords = ["keyword1", "keyword2"]

resultado = parse_syntax(texto, keywords)
for i, group in enumerate(resultado):
    print(f"Grupo {i + 1}: {group}")
