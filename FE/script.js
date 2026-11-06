
const API_URL = "http://127.0.0.1:8000/videos";

async function loadVideos() {
    const response = await fetch(API_URL);
    const videos = await response.json();

    const list = document.getElementById("videoList");
    list.innerHTML = "";

    videos.forEach(video => {
        const div = document.createElement("div");
        div.className = "video";

        const title = document.createElement("h3");
        title.textContent = video.title;

        const description = document.createElement("p");
        description.textContent = video.description || "";

        const editButton = document.createElement("button");
        editButton.textContent = "Sửa";
        editButton.onclick = () => editVideo(video);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Xóa";
        deleteButton.onclick = () => deleteVideo(video.id);

        div.append(title, description, editButton, deleteButton);
        list.appendChild(div);
    });
}

document.getElementById("videoForm").onsubmit = async function(event) {
    event.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    const response = await fetch(API_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, description})
    });

    if (!response.ok) {
        alert("Không thể thêm video");
        return;
    }

    this.reset();
    loadVideos();
};

async function editVideo(video) {
    const title = prompt("Tên video mới:", video.title);
    if (title === null || !title.trim()) return;

    const description = prompt("Mô tả mới:", video.description || "");
    if (description === null) return;

    const response = await fetch(`${API_URL}/${video.id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, description})
    });

    if (response.ok) loadVideos();
    else alert("Không thể sửa video");
}

async function deleteVideo(id) {
    if (!confirm("Bạn muốn xóa video này?")) return;

    const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    if (response.ok) loadVideos();
    else alert("Không thể xóa video");
}

loadVideos().catch(() => {
    alert("Không kết nối được Backend");
});
