from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

# Configurações
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Função para verificar extensões permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota de upload de arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        # Verifica se o nome do arquivo é válido
        if file.filename == '':
            return jsonify({'error': 'Nome de arquivo inválido'}), 400
        
        # Verifica se o arquivo é permitido
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Salva o arquivo
            file.save(file_path)
            
            # Retorna sucesso
            return jsonify({
                'message': 'Arquivo enviado com sucesso',
                'filename': filename,
                'file_url': f'/download/{filename}'
            }), 200
        
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
    
    except RequestEntityTooLarge:
        return jsonify({'error': 'Arquivo muito grande. O tamanho máximo permitido é 16MB.'}), 413
    except Exception as e:
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

# Rota para download de arquivos
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

# Gerenciamento de erros personalizado
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Página não encontrada'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# Inicialização do servidor
if __name__ == '__main__':
    # Cria a pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Executa o servidor
    app.run(debug=True)