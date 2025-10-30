# release.py
# Este script automatiza o processo de criação de uma nova versão do addon TVSTREAMX.

import os
import zipfile
import shutil
import xml.etree.ElementTree as ET

# --- CONFIGURAÇÕES ---
ADDON_ID = 'plugin.video.tvstreamx'
ADDON_XML_FILE = os.path.join(ADDON_ID, 'addon.xml')
OUTPUT_DIR = '.' # Onde os arquivos (zip e version.txt) serão criados. '.' significa a pasta atual.
# ---------------------

# Classe para deixar as mensagens no terminal mais bonitas
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def get_addon_version(xml_path):
    """Lê o arquivo addon.xml e retorna a versão."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        version = root.get('version')
        if not version:
            print(f"{Colors.RED}ERRO: A tag 'version' não foi encontrada em {xml_path}{Colors.ENDC}")
            return None
        return version
    except FileNotFoundError:
        print(f"{Colors.RED}ERRO: Arquivo {xml_path} não encontrado!{Colors.ENDC}")
        return None
    except ET.ParseError:
        print(f"{Colors.RED}ERRO: Falha ao ler o arquivo XML {xml_path}. Verifique se ele está formatado corretamente.{Colors.ENDC}")
        return None

def create_addon_zip(addon_dir, output_path):
    """Cria um arquivo .zip contendo todos os arquivos do addon."""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(addon_dir):
            # Ignora arquivos e pastas desnecessários no .zip final
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]
            files = [f for f in files if not f.endswith('.pyo') and not f.endswith('.pyc')]
            
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, os.path.join(addon_dir, '..'))
                zipf.write(filepath, arcname)

def create_version_file(version, output_path):
    """Cria ou atualiza o arquivo version.txt."""
    # --- ESTA É A LINHA QUE FOI CORRIGIDA ---
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(version)

def main():
    """Função principal do script."""
    print(f"{Colors.BLUE}--- Iniciando processo de release para o addon {ADDON_ID} ---{Colors.ENDC}")

    # 1. Obter a versão do addon.xml
    version = get_addon_version(ADDON_XML_FILE)
    if not version:
        return # Encerra se não conseguir pegar a versão

    print(f"Versão detectada no addon.xml: {Colors.YELLOW}{version}{Colors.ENDC}")

    # 2. Definir nomes dos arquivos de saída
    zip_filename = f"{ADDON_ID}-{version}.zip"
    zip_filepath = os.path.join(OUTPUT_DIR, zip_filename)
    version_txt_filepath = os.path.join(OUTPUT_DIR, 'version.txt')
    
    # 3. Criar o arquivo .zip
    try:
        print(f"Criando arquivo zip: {zip_filename}...")
        create_addon_zip(ADDON_ID, zip_filepath)
        print(f"{Colors.GREEN}Arquivo .zip criado com sucesso!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}ERRO ao criar o arquivo .zip: {e}{Colors.ENDC}")
        return

    # 4. Criar o arquivo version.txt
    try:
        print(f"Criando arquivo: version.txt...")
        create_version_file(version, version_txt_filepath)
        print(f"{Colors.GREEN}Arquivo version.txt atualizado com sucesso!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}ERRO ao criar o version.txt: {e}{Colors.ENDC}")
        return
        
    print(f"\n{Colors.BLUE}--- Processo de release concluído ---{Colors.ENDC}")
    print("Os seguintes arquivos foram criados/atualizados:")
    print(f"- {Colors.YELLOW}{zip_filename}{Colors.ENDC}")
    print(f"- {Colors.YELLOW}version.txt{Colors.ENDC}")
    print("\nAgora, você só precisa enviar esses arquivos para o seu repositório no GitHub.")
    print("Use os comandos `git add`, `git commit` e `git push`.")

if __name__ == "__main__":
    main()