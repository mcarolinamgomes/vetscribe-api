import json

def generate_pretty_txt(json_data_str, output_path="generated_report.txt"):
    try:
        data = json.loads(json_data_str)
    except json.JSONDecodeError:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Relatório Clínico\n")
            f.write("Erro: JSON inválido.\n")
        return

    lines = []
    lines.append("Relatório Clínico")
    lines.append("=" * 40)

    def add_section(title, content):
        lines.append(f"\n{title.upper()}")
        lines.append("-" * len(title))
        if isinstance(content, list):
            for item in content:
                lines.append(f"- {item}")
        elif isinstance(content, dict):
            for k, v in content.items():
                lines.append(f"{k.capitalize()}: {v}")
        elif content:
            lines.append(str(content))

    lines.append(f"\nData do Exame: {data.get('data_exame', '')}")
    lines.append(f"Clínica: {data.get('clinica', '')}")

    animal = data.get("animal", {})
    lines.append("\nANIMAL")
    lines.append("-" * 10)
    for k, v in animal.items():
        if v:
            lines.append(f"{k.capitalize()}: {v}")

    add_section("Motivo da Consulta", data.get("motivo_consulta", ""))
    add_section("Anamnese", data.get("anamnese", ""))
    add_section("Exame Estático", data.get("exame_estatico", {}).get("observacoes", []))
    add_section("Exame Dinâmico", data.get("exame_dinamico", {}).get("observacoes", []))

    exames = data.get("exames_complementares", {})
    if exames:
        lines.append("\nEXAMES COMPLEMENTARES")
        lines.append("-" * 24)
        for tipo, sub in exames.items():
            for nome, detalhe in sub.items():
                lines.append(f"{tipo.upper()} - {nome}")
                lines.append(f"Descrição: {detalhe.get('descricao', '')}")
                for proj in detalhe.get("projecoes", []):
                    lines.append(f"Projeção: {proj}")
                for achado in detalhe.get("achados", []):
                    lines.append(f"Achado: {achado}")

    tratamento = data.get("tratamento", [])
    if tratamento:
        formatted = [f"{t['tipo']} - {t['medicamento']} ({t['dose']})" for t in tratamento]
        add_section("Tratamento", formatted)

    add_section("Recomendações", data.get("recomendacoes", {}).get("observacoes_adicionais", []))
    add_section("Indicações de Ferragem", data.get("indicacoes_ferragem", {}))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
