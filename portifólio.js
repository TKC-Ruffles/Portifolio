// Upload de Arquivos
const fileUpload = document.getElementById('fileUpload');
const uploadArea = document.querySelector('.upload-area');

fileUpload.addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (file.type !== 'application/pdf' && !file.type.startsWith('image/')) {
    showNotification('Apenas PDF e imagens são permitidos!', 'error');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    const preview = document.createElement('div');
    preview.className = 'upload-preview';
    preview.innerHTML = `
      <div class="preview-content">
        <i class="fas fa-file-alt"></i>
        <p>${file.name}</p>
      </div>
      <button class="remove-file"><i class="fas fa-times"></i></button>
    `;
    
    uploadArea.parentNode.insertBefore(preview, uploadArea.nextSibling);
    addFileActions(preview);
  };
  reader.readAsDataURL(file);
});

function addFileActions(preview) {
  preview.querySelector('.remove-file').addEventListener('click', () => {
    preview.remove();
  });
}