navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream) {
    document.getElementById('video').srcObject = stream;
})
.catch(function(err) {
    console.error("Camera error: " + err);
});

navigator.geolocation.getCurrentPosition(function(position) {
    document.getElementById('latitude').value = position.coords.latitude;
    document.getElementById('longitude').value = position.coords.longitude;
});

function capturePhoto() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const dataURL = canvas.toDataURL('image/png');
    document.getElementById('image').value = dataURL;
}
