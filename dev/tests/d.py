import os

def list_files_and_folders(path, indent=""):
    items = os.listdir(path)
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(f"{indent}📁 {item}")
            list_files_and_folders(item_path, indent + "    ")
        else:
            print(f"{indent}📄 {item}")

def main():
    path = input("Digite o caminho do diretório: ")
    if os.path.exists(path) and os.path.isdir(path):
        print(f"Árvore de diretórios e arquivos para '{path}':")
        list_files_and_folders(path)
    else:
        print("O caminho fornecido não é válido ou não é um diretório.")

if __name__ == "__main__":
    main()
