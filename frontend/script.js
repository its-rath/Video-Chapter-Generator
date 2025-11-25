const API_URL = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const videoInput = document.getElementById('video-input');
    const uploadSection = document.getElementById('upload-section');
    const optionsSection = document.getElementById('options-section');
    const resultsSection = document.getElementById('results-section');
    const uploadStatus = document.getElementById('upload-status');
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    const generateBtn = document.getElementById('generate-btn');
    const chaptersList = document.getElementById('chapters-list');

    let selectedFile = null;

    // Drag & Drop Handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.transform = 'scale(1.02)';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.transform = 'scale(1)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.transform = 'scale(1)';
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type.startsWith('video/')) {
            handleFileSelect(files[0]);
        } else {
            alert('Please drop a valid video file!');
        }
    });

    dropZone.addEventListener('click', () => {
        videoInput.click();
    });

    videoInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        selectedFile = file;
        // Show options, hide upload prompt slightly or update text
        dropZone.querySelector('h2').textContent = file.name;
        dropZone.querySelector('p').textContent = `Ready to process (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        optionsSection.classList.remove('hidden');
        // Scroll to options
        optionsSection.scrollIntoView({ behavior: 'smooth' });
    }

    generateBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI Updates
        uploadStatus.classList.remove('hidden');
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        // Prepare Form Data
        const formData = new FormData();
        formData.append('video', selectedFile);
        formData.append('language', document.getElementById('language-select').value);
        formData.append('enable_scene_detection', document.getElementById('scene-detection').checked);
        // Default values for now
        formData.append('min_chapter_duration', 60);

        // Simulate progress (since fetch doesn't give upload progress easily without XHR)
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += 5;
                updateProgress(progress);
            }
        }, 500);

        try {
            const response = await fetch(`${API_URL}/generate-chapters`, {
                method: 'POST',
                body: formData
            });

            clearInterval(progressInterval);
            updateProgress(100);

            if (!response.ok) {
                throw new Error('Generation failed');
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during chapter generation. Please check the console.');
            updateProgress(0);
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Chapters';
        }
    });

    function updateProgress(percent) {
        progressText.textContent = `${percent}%`;
        progressFill.style.width = `${percent}%`;
    }

    function displayResults(data) {
        resultsSection.classList.remove('hidden');
        chaptersList.innerHTML = ''; // Clear previous

        if (data.chapters && data.chapters.length > 0) {
            data.chapters.forEach(chapter => {
                const div = document.createElement('div');
                div.className = 'chapter-item';
                div.innerHTML = `
                    <span class="chapter-time">${formatTime(chapter.start)}</span>
                    <span class="chapter-title">${chapter.title}</span>
                `;
                chaptersList.appendChild(div);
            });
        } else {
            chaptersList.innerHTML = '<p>No chapters generated.</p>';
        }

        // Setup Export Buttons
        document.querySelectorAll('.export-actions button').forEach(btn => {
            btn.onclick = () => {
                const format = btn.dataset.format;
                if (data.job_id) {
                    window.open(`${API_URL}/download/${data.job_id}/${format}`, '_blank');
                }
            };
        });

        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function formatTime(seconds) {
        const date = new Date(seconds * 1000);
        const hh = date.getUTCHours();
        const mm = date.getUTCMinutes();
        const ss = date.getUTCSeconds();
        if (hh > 0) {
            return `${hh.toString().padStart(2, '0')}:${mm.toString().padStart(2, '0')}:${ss.toString().padStart(2, '0')}`;
        }
        return `${mm.toString().padStart(2, '0')}:${ss.toString().padStart(2, '0')}`;
    }
});
