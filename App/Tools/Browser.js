const fs = require('fs');
const ini = require('ini');
const {
    app,
    BrowserWindow,
    Menu,
    ipcMain
} = require('electron');
const path = require('path');
const diretorioAtual = __dirname;
const diretorioPai = path.dirname(diretorioAtual);
const diretorioPaiDoPai = path.dirname(diretorioPai);

console.log(diretorioPaiDoPai);

const configFile = `${diretorioPaiDoPai}\\config.ini`;

let mainWindow;

try {
    const data = fs.readFileSync(configFile, 'utf-8');
    const config = ini.parse(data);

    app.whenReady().then(() => {
        mainWindow = new BrowserWindow({
            width: 1920,
            height: 1080,
            webPreferences: {
                nodeIntegration: true,
                preload: path.join(__dirname, 'Preload.js')
            },
        });

        mainWindow.setMenu(null);

        const template = [{
            label: 'angueraAdmin',
            submenu: [{
                    label: 'Sobre ',
                },
                {
                    type: 'separator'
                },
                {
                    label: 'Sair',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        }];

        const menu = Menu.buildFromTemplate(template);
        Menu.setApplicationMenu(menu);

        // Injetar CSS personalizado no menu
        mainWindow.webContents.on('dom-ready', () => {
            mainWindow.webContents.insertCSS(`
                .menubar {
                    background-color: #f0f0f0; /* Cor de fundo */
                    color: #333; /* Cor do texto */
                }
                .menu {
                    background-color: #f0f0f0; /* Cor de fundo */
                    color: #333; /* Cor do texto */
                }
                .menu > .menu-item {
                    background-color: #f0f0f0; /* Cor de fundo */
                    color: #333; /* Cor do texto */
                }
            `);
        });

        // Carrega o Google.com quando a janela estiver pronta
        mainWindow.loadURL(`http://${config.Panel.Host}:${config.Panel.Port}`);
    });
} catch (error) {
    console.error('Erro ao ler o arquivo de configuração:', error);
}

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('close', (event) => {
    if (window.isFullScreen()) {
        window.setFullScreen(false)
    }
    window.hide()
})

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

ipcMain.on('check-other-window', () => {
    mainWindow.webContents.send('check-other-window');
});
