async function loadArchive(){
    const response = await fetch('/me');
    const data = await response.json();

    const archiveDiv = document.getElementById('archive');

    archiveDiv.innerHTML = "";
    for (const category in data) {
        const categoryDiv = document.createElement("div");
        categoryDiv.className = "category";
        categoryDiv.innerHTML = `<h3>${category}</h3>`;
        
        data[category].forEach(item => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "item";
            itemDiv.innerHTML = `
                <span>${item}</span>
                <button onclick="deleteItem(${getItemId(category, item)})">Delete</button>
            `;
            categoryDiv.appendChild(itemDiv);
        });
        
        archiveDiv.appendChild(categoryDiv);
    }
}

async function addItem(){
    const category = document.getElementById('category').value;
    const item = document.getElementById('item').value;

    if (!category || !item) {
        alert("Please fill in both fields.");
        return;
    }

    const response = await fetch('/category',{
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({category, item})
    })

    if (response.ok){
        document.getElementById("category").value = "";
        document.getElementById("item").value = "";
        loadArchive();
    }

}

async function deleteItem(id){
    const response = await fetch(`/item/${id}`, {
        method: 'DELETE'
    });

    if (response.ok){
        loadArchive();
    }
}

function getItemId(category, item) {
    // Placeholder — we'll update this
    return 1;
}


loadArchive();
