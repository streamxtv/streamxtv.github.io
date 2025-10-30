# release.py (VERSÃO FINAL E CORRIGIDA)
# Automatiza a criação da release e atualiza o index.html.

import os
import zipfile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# --- CONFIGURAÇÕES ---
ADDON_ID = 'plugin.video.tvstreamx'
ADDON_XML_FILE = os.path.join(ADDON_ID, 'addon.xml')
INDEX_HTML_FILE = 'index.html' # O arquivo do site que será atualizado
OUTPUT_DIR = '.' 
# ---------------------

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
        return root.get('version')
    except Exception as e:
        print(f"{Colors.RED}ERRO ao ler a versão do {xml_path}: {e}{Colors.ENDC}")
        return None

def create_addon_zip(addon_dir, output_path):
    """Cria um arquivo .zip do addon."""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(addon_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]
            files = [f for f in files if not f.endswith(('.pyo', '.pyc'))]
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, os.path.join(addon_dir, '..'))
                zipf.write(filepath, arcname)

def create_version_file(version, output_path):
    """Cria o arquivo version.txt."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(version)

def update_index_html(html_path, new_filename):
    """Encontra os links no index.html e os atualiza com o novo nome de arquivo."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        link_display = soup.find(id='addon-filename-display')
        download_link = soup.find(id='addon-download-link')

        if not link_display or not download_link:
            print(f"{Colors.RED}ERRO: IDs 'addon-filename-display' ou 'addon-download-link' não encontrados no {html_path}{Colors.ENDC}")
            return False

        link_display.string = new_filename
        download_link['href'] = new_filename
        download_link.string = new_filename
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
            
        return True
    except Exception as e:
        print(f"{Colors.RED}ERRO ao atualizar o {html_path}: {e}{Colors.ENDC}")
        return False

def main():
    print(f"{Colors.BLUE}--- Iniciando processo de release para {ADDON_ID} ---{Colors.ENDC}")

    version = get_addon_version(ADDON_XML_FILE)
    if not version: return

    print(f"Versão detectada: {Colors.YELLOW}{version}{Colors.ENDC}")

    zip_filename = f"{ADDON_ID}-{version}.zip"
    zip_filepath = os.path.join(OUTPUT_DIR, zip_filename)
    version_txt_filepath = os.path.join(OUTPUT_DIR, 'version.txt')
    
    print(f"Criando arquivo zip: {zip_filename}...")
    create_addon_zip(ADDON_ID, zip_filepath)
    print(f"{Colors.GREEN}Arquivo .zip criado com sucesso!{Colors.ENDC}")

    print(f"Criando arquivo: version.txt...")
    create_version_file(version, version_txt_filepath)
    print(f"{Colors.GREEN}Arquivo version.txt criado com sucesso!{Colors.ENDC}")

    print(f"Atualizando o arquivo: {INDEX_HTML_FILE}...")
    if update_index_html(INDEX_HTML_FILE, zip_filename):
        print(f"{Colors.GREEN}Arquivo {INDEX_HTML_FILE} atualizado com sucesso!{Colors.ENDC}")
    else:
        return

    print(f"\n{Colors.BLUE}--- Processo de release concluído ---{Colors.ENDC}")
    print("Arquivos criados/atualizados:")
    print(f"- {Colors.YELLOW}{zip_filename}{Colors.ENDC}")
    print(f"- {Colors.YELLOW}version.txt{Colors.ENDC}")
    print(f"- {Colors.YELLOW}{INDEX_HTML_FILE}{Colors.ENDC}")
    print("\nEnvie os arquivos atualizados para o seu repositório no GitHub.")

if __name__ == "__main__":
    main()