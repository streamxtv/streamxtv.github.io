// Arquivo: updater.js

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Configurações ---
    const githubUser = 'streamxtv';
    const githubRepo = 'streamxtv.github.io';
    const addonPrefix = 'plugin.video.tvstreamx-';
    const addonSuffix = '.zip';

    // URL da API do GitHub para listar os arquivos do repositório
    const apiUrl = `https://api.github.com/repos/${githubUser}/${githubRepo}/contents/`;

    // --- Seletores dos Elementos ---
    const filenameDisplay = document.getElementById('addon-filename-display');
    const downloadLink = document.getElementById('addon-download-link');

    if (!filenameDisplay || !downloadLink) {
        console.error("Elementos de atualização do addon não encontrados na página.");
        return;
    }

    // --- Lógica de Atualização ---
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Falha ao buscar a lista de arquivos do repositório.');
            }
            return response.json();
        })
        .then(files => {
            // 1. Filtra a lista para encontrar apenas os arquivos .zip do addon
            const addonFiles = files
                .map(file => file.name)
                .filter(name => name.startsWith(addonPrefix) && name.endsWith(addonSuffix));

            if (addonFiles.length === 0) {
                console.warn("Nenhum arquivo .zip do addon encontrado no repositório.");
                filenameDisplay.textContent = "Nenhuma versão encontrada.";
                return;
            }

            // 2. Ordena os arquivos para encontrar a versão mais recente
            // O 'numeric: true' ajuda a ordenar "2.2.10" corretamente em vez de "2.2.9"
            addonFiles.sort((a, b) => b.localeCompare(a, undefined, { numeric: true, sensitivity: 'base' }));
            
            // 3. O primeiro item da lista ordenada é o mais recente
            const latestFilename = addonFiles[0];

            // 4. Atualiza os elementos na página
            filenameDisplay.textContent = latestFilename;
            downloadLink.textContent = latestFilename;
            downloadLink.href = latestFilename;
            
            console.log(`Página atualizada para o addon: ${latestFilename}`);
        })
        .catch(error => {
            console.error("Erro ao buscar a versão mais recente do addon:", error);
            filenameDisplay.textContent = "Erro ao buscar versão. Tente novamente.";
        });
});