import math
import os
import time
from multiprocessing import Process

CHUNK_SIZE = 1048576 * 32 # 1MB x 32

def process_bytes(index, scale, orig_path, out_path):
    start = index*scale
    end = (start+scale)-1
    
    orig_file = open(orig_path, "rb")
    out_file = open(out_path, "rb+")
    orig_file.seek(start)
    out_file.seek(start)
    list_bytes = bytearray(orig_file.read(scale))
    for index, byte in enumerate(list_bytes[start:end]):
        list_bytes[start+index] = 255 - byte
    out_file.seek(start)
    out_file.write(list_bytes)
    
    orig_file.close()
    out_file.close()


def inverter_bits(path, mode):
    if mode in ("encode, decode"):
        filename = os.path.basename(path)
        output_path = os.path.abspath(f"saida/{mode}/{filename}")
        t = time.time()
        size = os.path.getsize(path)
        total_chunks = math.ceil(size / CHUNK_SIZE)
        num_workers = 4 if size >= CHUNK_SIZE else 1
        work_scale = CHUNK_SIZE//num_workers
        output_file = open(output_path, "wb")
        orig_file = open(path, "rb")
        for progress in range(total_chunks):
            workers = []
            output_file.write(orig_file.read(CHUNK_SIZE))
            output_file.flush()
            for i in range(num_workers):
                workers.append(Process(target=process_bytes, args=(progress*work_scale+i, work_scale, path, output_path)))
                workers[i].start()
            for worker in workers:
                worker.join()
            p = progress / total_chunks * 100
            print(f"  chunk {progress+1:,} of {total_chunks:,} ( {p:.2f}% ), file: {filename}", end="\r")
        print(100*" ", end="\r")
        t = time.time() - t
        print()
        print(f"{t:.2f} segundos, arquivo", filename)
        print()


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
