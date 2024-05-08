const {
    ipcRenderer
} = require('electron');

window.addEventListener('DOMContentLoaded', () => {
    ipcRenderer.on('check-other-window', () => {
        const otherWindow = require('electron').remote.BrowserWindow.getAllWindows().find(win => win !== window);
        if (otherWindow) {
            otherWindow.close();
        }
    });
});
