import os


inverse_hex_table = {hex(i)[2:]: hex(15 - i)[2:] for i in range(16)}

CHUNK_SIZE = 1024  #  1kb


def inverter_bits(path, mode):
    if mode in ("encode, decode"):
        filename = os.path.basename(path)
        output_path = os.path.abspath(f"saida/{mode}/{filename}")
        size = os.path.getsize(path)
        orig_file = open(path, "rb")
        output_file = open(output_path, "wb")
        total_chunks = size // CHUNK_SIZE
        for progress in range(total_chunks):
            orig_chunk = orig_file.read(CHUNK_SIZE).hex()
            output_chunk = bytes.fromhex(
                "".join(map(lambda hex_digit: inverse_hex_table[hex_digit], orig_chunk))
            )
            output_file.write(output_chunk)
            print(f"  chunk {progress:,} of {total_chunks:,}, file: {filename}", end="\r")

        # Last chunk
        if (last_chunk := size % CHUNK_SIZE) > 0:
            orig_chunk = orig_file.read(last_chunk).hex()
            output_chunk = bytes.fromhex(
                "".join(map(lambda hex_digit: inverse_hex_table[hex_digit], orig_chunk))
            )
            output_file.write(output_chunk)
        print(100*" ", end="\r")
        orig_file.close()
        output_file.close()


# Eu sei que existe o match case na versão 3.10,
# mas eu costumo usar a 3.8 por questões de
# compatibilidade com Windows 7 no meu dia a dia
match_case_improvisado = {"1": inverter_bits}


def main():
    while True:
        pasta = ""
        print("1. Encode")
        print("2. Decode")
        print("")
        resposta = input("Escolha o objetivo -> ")
        if resposta == "1":
            pasta = "encode"
        elif resposta == "2":
            pasta = "decode"
        elif resposta == ".":
            break
        if pasta in ("encode", "decode"):
            while True:
                if os.path.exists(
                    caminho := os.path.abspath(input("Qual o caminho para o arquivo?  "))
                ):
                    if not (os.path.exists(caminho_saida := os.path.abspath("saida/"))):
                        os.mkdir(caminho_saida)
                    if not (
                        os.path.exists(caminho_saida := os.path.abspath(f"saida/{pasta}"))
                    ):
                        os.mkdir(caminho_saida)
                    if os.path.isfile(caminho):
                        inverter_bits(caminho, pasta)
                    elif os.path.isdir(caminho):
                        for top, _, files in os.walk(caminho):
                            # if not os.path.exists(top)
                            for file in files:
                                inverter_bits(os.path.join(caminho, file), pasta)

                    break


if __name__ == "__main__":
    main()
