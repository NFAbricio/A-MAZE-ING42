import sys
from dataclasses import dataclass

# Conjunto com as chaves obrigatórias do arquivo de configuração
REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


@dataclass
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def parse_coordinate(value: str) -> tuple[int, int]:
    try:
        parts = value.split(",")
        if len(parts) != 2:
            raise ValueError(
                "Deve conter exatamente duas coordenadas separadas por vírgula."
            )

        x = int(parts[0].strip())
        y = int(parts[1].strip())
        return (x, y)
    except ValueError as e:
        print(f"Erro ao processar coordenada '{value}': {e}", file=sys.stderr)
        sys.exit(1)


def parse_bool(value: str) -> bool:
    cleaned = value.strip().lower()
    if cleaned == "true":
        return True
    elif cleaned == "false":
        return False
    else:
        print(
            f"Valor booleano inválido: '{value}'. Esperado 'True' ou 'False'.",
            file=sys.stderr,
        )
        sys.exit(1)


def load_config(config_path: str) -> MazeConfig:
    # 1. Leitura do arquivo
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Erro ao abrir arquivo de configuração: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Extração dos pares chave-valor
    raw_data: dict[str, str] = {}
    for line in lines:
        clean_line = line.strip()
        # Ignora linhas em branco ou comentários
        if not clean_line or clean_line.startswith("#"):
            continue

        # Normaliza possíveis sinais duplicados e divide
        clean_line = clean_line.replace("==", "=")
        if "=" not in clean_line:
            continue

        chave, valor = clean_line.split("=", 1)
        raw_data[chave.strip()] = valor.strip()

    # 3. Validação das chaves obrigatórias
    missing_keys = REQUIRED_KEYS - raw_data.keys()
    if missing_keys:
        print(
            f"Erro: Chaves ausentes no arquivo de configuração: {', '.join(missing_keys)}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 4. Conversão e criação do objeto MazeConfig
    try:
        return MazeConfig(
            width=int(raw_data["WIDTH"]),
            height=int(raw_data["HEIGHT"]),
            entry=parse_coordinate(raw_data["ENTRY"]),
            exit=parse_coordinate(raw_data["EXIT"]),
            output_file=raw_data["OUTPUT_FILE"],
            perfect=parse_bool(raw_data["PERFECT"]),
        )
    except ValueError as e:
        print(f"Erro ao converter valores de configuração: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    # Validação do argumento de linha de comando
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config = load_config(sys.argv[1])
    print(f"Configuração carregada com sucesso: {config}")


if __name__ == "__main__":
    main()