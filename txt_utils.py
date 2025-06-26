import json
import logging

def generate_pretty_txt(json_data_str, output_path="report.txt"):
    if not json_data_str:
        logging.error("Received empty or None as JSON data.")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Erro: Nenhum dado fornecido.")
        return
    
    try:
        # Attempt to parse JSON string into a Python object
        data = json.loads(json_data_str)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Erro: JSON inválido.")
        return

    # Prepare the lines for the report
    lines = []

    # Adding report title and exam date
    lines.append("Relatório Clínico\n")
    lines.append(f"Data do Exame: {data.get('data_exame', 'Não disponível')}")
    lines.append(f"Clínica: {data.get('clinica', 'Não especificado')}\n")

    # Handling the animal information
    animal = data.get("animal", {})
    lines.append("Animal:")
    if not animal:
        lines.append("Informações sobre o animal não fornecidas.")
    else:
        for k, v in animal.items():
            if v:
                lines.append(f"{k.capitalize()}: {v}")
    lines.append("")

    # Helper function to add sections to the report
    def add_section(title, content):
        lines.append(title)
        if isinstance(content, list):
            if content:
                lines.extend(f"- {item}" for item in content)
            else:
                lines.append("Nenhum item listado.")
        elif isinstance(content, dict):
            if content:
                lines.extend(f"{k.capitalize()}: {v}" for k, v in content.items())
            else:
                lines.append("Nenhum detalhe disponível.")
        elif content:
            lines.append(str(content))
        else:
            lines.append("Sem conteúdo.")
        lines.append("")

    # Adding various sections from the data
    add_section("Motivo da Consulta", data.get("motivo_consulta", "Não especificado"))
    add_section("Anamnese", data.get("anamnese", "Não fornecida"))
    add_section("Exame Estático", data.get("exame_estatico", {}).get("observacoes", []))
    add_section("Exame Dinâmico", data.get("exame_dinamico", {}).get("observacoes", []))

    # Handling complementary exams section
    exames = data.get("exames_complementares", {})
    if exames:
        lines.append("Exames Complementares:")
        for tipo, sub in exames.items():
            for nome, detalhe in sub.items():
                lines.append(f"{tipo.upper()} - {nome}")
                lines.append(f"Descrição: {detalhe.get('descricao', 'Não especificado')}")
                lines.extend(f"Projeção: {proj}" for proj in detalhe.get("projecoes", []))
                lines.extend(f"Achado: {achado}" for achado in detalhe.get("achados", []))
        lines.append("")
    else:
        lines.append("Nenhum exame complementar listado.")

    # Handling treatment section
    tratamento = data.get("tratamento", [])
    if tratamento:
        add_section("Tratamento", [f"{t['tipo']} - {t['medicamento']} ({t['dose']})" for t in tratamento])
    else:
        lines.append("Nenhum tratamento listado.")

    # Adding recommendations and ferragem sections
    add_section("Recomendações", data.get("recomendacoes", {}).get("observacoes_adicionais", []))
    add_section("Indicações de Ferragem", data.get("indicacoes_ferragem", {}))

    # Writing the report to the output file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logging.info("Relatório gerado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao escrever o relatório: {e}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Erro: Não foi possível gerar o relatório.")