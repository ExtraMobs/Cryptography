import math
import os
import time

CHUNK_SIZE = 1048576 * 32 # 1MB x 32


def inverter_bits(path, mode):
    if mode in ("encode, decode"):
        t = time.time()
        filename = os.path.basename(path)
        output_path = os.path.abspath(f"saida/{mode}/{filename}")
        size = os.path.getsize(path)
        orig_file = open(path, "rb")
        output_file = open(output_path, "ab")
        total_chunks = math.ceil(size / CHUNK_SIZE)
        for progress in range(total_chunks):
            orig_chunk = bytearray(orig_file.read(CHUNK_SIZE))
            for index, byte in enumerate(orig_chunk):
                orig_chunk[index] = 255 - byte
            output_file.write(orig_chunk)
            p = progress / total_chunks * 100
            print(f"  chunk {progress:,} of {total_chunks:,} ( {p:.2f}% ), file: {filename}", end="\r")
        print()
        print(100*" ", end="\r")
        print()
        orig_file.close()
        output_file.close()
        t = time.time() - t
        print(f"{t:.2f}", filename)


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
                                print(os.path.join(top, file))
                                inverter_bits(os.path.join(caminho, file), pasta)

                    break


if __name__ == "__main__":
    main()
