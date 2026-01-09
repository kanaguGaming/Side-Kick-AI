import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    const provider = new SidekickChatProvider(context.extensionUri);

    // Register the provider immediately
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(SidekickChatProvider.viewType, provider)
    );
}

class SidekickChatProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'sidekick.chatView';
    private _view?: vscode.WebviewView;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        // Set the HTML immediately to stop the "Loading..." state
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Listen for messages from the sidebar
        webviewView.webview.onDidReceiveMessage(async (data) => {
            if (data.type === 'askTA') {
                const editor = vscode.window.activeTextEditor;
                const studentCode = editor ? editor.document.getText() : "No code open.";

                try {
                    // Call your FastAPI backend
                    const response = await axios.post('http://localhost:8000/api/ask-ta', {
                        student_id: "student_01",
                        code: studentCode,
                        hypothesis: data.value
                    });

                    this._view?.webview.postMessage({ 
                        type: 'addResponse', 
                        value: response.data.reply 
                    });
                } catch (err) {
                    this._view?.webview.postMessage({ 
                        type: 'addResponse', 
                        value: "Error: TA brain is offline. Check if run.py is active." 
                    });
                }
            }
        });
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        return `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <style>
                    body { 
                        font-family: var(--vscode-font-family); 
                        padding: 10px; 
                        color: var(--vscode-foreground); 
                        display: flex; 
                        flex-direction: column; 
                        height: 96vh; 
                    }
                    #chat { flex: 1; overflow-y: auto; padding-right: 5px; }
                    
                    /* Base message styling */
                    .msg { 
                        margin-bottom: 20px; 
                        padding: 8px 12px; 
                        line-height: 1.5;
                    }
                    
                    .role-header {
                        font-weight: bold;
                        display: block;
                        margin-bottom: 4px;
                        font-size: 0.9em;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }

                    /* Student (You) - Blue left border */
                    .user { 
                        border-left: 4px solid #007acc; 
                        background: rgba(0, 122, 204, 0.05);
                    }
                    
                    /* SideKick AI - Grey left border */
                    .ta { 
                        border-left: 4px solid #858585; 
                        background: rgba(133, 133, 133, 0.05);
                    }

                    .input-container { 
                        padding: 10px 0;
                        border-top: 1px solid var(--vscode-widget-border);
                    }
                    
                    input { 
                        width: 100%; 
                        padding: 10px; 
                        background: var(--vscode-input-background); 
                        color: var(--vscode-input-foreground); 
                        border: 1px solid var(--vscode-input-border);
                        outline: none;
                    }
                    input:focus { border-color: var(--vscode-focusBorder); }
                </style>
            </head>
            <body>
                <div id="chat">
                    <div class="msg ta">
                        <span class="role-header">SideKick AI</span>
                        Hello! I'm ready to help with your lab. Explain your logic below.
                    </div>
                </div>
                <div class="input-container">
                    <input type="text" id="prompt" placeholder="Message SideKick AI..." autocomplete="off" />
                </div>
                
                <script>
                    const vscode = acquireVsCodeApi();
                    const prompt = document.getElementById('prompt');
                    const chat = document.getElementById('chat');

                    prompt.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' && prompt.value.trim()) {
                            const val = prompt.value;
                            append('user', val);
                            vscode.postMessage({ type: 'askTA', value: val });
                            prompt.value = '';
                        }
                    });

                    window.addEventListener('message', event => {
                        if (event.data.type === 'addResponse') {
                            append('ta', event.data.value);
                        }
                    });

                    function append(role, text) {
                        const div = document.createElement('div');
                        div.className = 'msg ' + role;
                        
                        const name = role === 'ta' ? 'SideKick AI' : 'You';
                        div.innerHTML = '<span class="role-header">' + name + '</span>' + text;
                        
                        chat.appendChild(div);
                        chat.scrollTop = chat.scrollHeight;
                    }
                </script>
            </body>
            </html>`;
    }
}