import json
def generate_pretty_txt(json_data_str, output_path="report.txt"):
    try:
        data = json.loads(json_data_str)
    except json.JSONDecodeError:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Erro: JSON inválido.")
        return

    lines = []

    lines.append("Relatório Clínico\n")
    lines.append(f"Data do Exame: {data.get('data_exame', '')}")
    lines.append(f"Clínica: {data.get('clinica', '')}\n")

    animal = data.get("animal", {})
    lines.append("Animal:")
    for k, v in animal.items():
        if v:
            lines.append(f"{k.capitalize()}: {v}")
    lines.append("")

    def add_section(title, content):
        lines.append(title)
        if isinstance(content, list):
            lines.extend(f"- {item}" for item in content)
        elif isinstance(content, dict):
            lines.extend(f"{k.capitalize()}: {v}" for k, v in content.items())
        elif content:
            lines.append(str(content))
        lines.append("")

    add_section("Motivo da Consulta", data.get("motivo_consulta", ""))
    add_section("Anamnese", data.get("anamnese", ""))
    add_section("Exame Estático", data.get("exame_estatico", {}).get("observacoes", []))
    add_section("Exame Dinâmico", data.get("exame_dinamico", {}).get("observacoes", []))

    exames = data.get("exames_complementares", {})
    if exames:
        lines.append("Exames Complementares:")
        for tipo, sub in exames.items():
            for nome, detalhe in sub.items():
                lines.append(f"{tipo.upper()} - {nome}")
                lines.append(f"Descrição: {detalhe.get('descricao', '')}")
                lines.extend(f"Projeção: {proj}" for proj in detalhe.get("projecoes", []))
                lines.extend(f"Achado: {achado}" for achado in detalhe.get("achados", []))
        lines.append("")

    tratamento = data.get("tratamento", [])
    if tratamento:
        add_section("Tratamento", [f"{t['tipo']} - {t['medicamento']} ({t['dose']})" for t in tratamento])

    add_section("Recomendações", data.get("recomendacoes", {}).get("observacoes_adicionais", []))
    add_section("Indicações de Ferragem", data.get("indicacoes_ferragem", {}))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
