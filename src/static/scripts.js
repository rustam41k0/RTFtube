function getVideos() {
    fetch('/videos')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('data-list');
            list.innerHTML = '';
            let html = '';
            data.forEach(video => {
                // const li = document.createElement('li');
                // li.innerText = item;
                // list.appendChild(li);
                html += '<div class="video">${video.title}</div>'
            });
        })
        .catch(error => console.error(error));
}

function main() {
    console.log('Hello')
}