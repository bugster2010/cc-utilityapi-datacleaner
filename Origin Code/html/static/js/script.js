function uploadFile() {
    const fileInput = document.getElementById('csvFileInput');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('csvFile', file);
  
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.fileUrl) {
          const downloadButton = createDownloadButton(data.fileUrl);
          appendDownloadButton(downloadButton);
        }
      })
      .catch(error => {
        console.error(error);
      });
  }
  
  function createDownloadButton(fileUrl) {
    const downloadButton = document.createElement('button');
    downloadButton.textContent = 'Download Processed CSV';
    downloadButton.addEventListener('click', () => {
      window.location.href = fileUrl;
    });
  
    return downloadButton;
  }
  
  function appendDownloadButton(downloadButton) {
    const downloadContainer = document.getElementById('downloadContainer');
    downloadContainer.appendChild(downloadButton);
  }
  