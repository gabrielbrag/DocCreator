import os
from dotenv import load_dotenv
import PySimpleGUI as pySimplegui
from lib.keyPackage import keyPackage
from lib.docManager import docManager

load_dotenv()

class windowManager:
    def __init__(self) -> None:        
        self.gui            = pySimplegui
        self.gui.theme(os.environ.get('APP_THEME'))
        
        self.keyPack        = keyPackage().getKeys()
        self.inputValues    = []
        self.page           = 0
        self.mountPageLayout()
    
    def mountPageLayout(self):
        pageLayout = []
        inputSize = 30
        labelSize = 20
        
        pageLayout.append([self.gui.Stretch(), self.gui.Image("custom/logo.png", size=(300, 130)), self.gui.Stretch()])
        
        if self.page <= (len(self.keyPack) - 1):     
            keyGroup = self.keyPack[self.page]
            
            for key in keyGroup:
                field = [self.gui.Text(key, labelSize)]
                
                defaultText = keyGroup[key]["defaultValue"] if "defaultValue" in keyGroup[key] else ""
                
                if "largeField" in keyGroup[key] and keyGroup[key]["largeField"] == True:
                    field.append(self.gui.Multiline(defaultText, size=(inputSize, 5), key=key, no_scrollbar=True))
                else:
                    field.append(self.gui.InputText(defaultText, inputSize, key=key))
                pageLayout.append(field)
            pageLayout.append(([(self.gui.Button('Anterior') if self.page > 0 else ()), self.gui.Stretch(), self.gui.Button('Próximo')]))
        else:
            pageLayout.append([self.gui.Text("Nome do documento", labelSize, pad=(5, 10)), self.gui.InputText(size=inputSize, pad=(5, 5))])
            pageLayout.append([self.gui.Button('Concluir')])
        
        #Nome da aplicação deve ser variavel de ambiente
        self.window = self.gui.Window(os.environ.get('APP_NAME'), pageLayout, icon='custom/logo.ico')


    def openWindow(self):
        while True:
            event, values = self.window.read()
            
            if event == self.gui.WIN_CLOSED or event == 'Cancelar': 
                self.window.close()
                break
            
            if event == 'Próximo':
                keyGroup = self.keyPack[self.page]
                for key in keyGroup:
                    keyGroup[key]["value"] = values[key]
                self.window.close()
                self.page += 1
                self.mountPageLayout()
                self.openWindow()
                break
            
            if event == 'Anterior':
                self.window.close()
                self.page -= 1
                self.mountPageLayout()
                self.openWindow()
            
            if event == "Concluir":
                self.docManager = docManager()
                
                for index in values:
                    self.docManager.setDocumentName(values[index])
                self.createDocument()
    
    def createDocument(self):
        self.docManager.replaceKeys(self.keyPack)
        self.docManager.saveDocument()
        self.gui.popup("Documento Salvo", icon='custom/logo.ico')
        