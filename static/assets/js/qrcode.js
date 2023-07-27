const wrapper = document.querySelector(".wrapper"),
form = document.getElementById('form'),
// document.querySelector("form"),

fileInp = document.getElementById('qrcode'),
// form.querySelector("input"),
infoText = form.querySelector("p");


function fetchRequest(file, formData) {
    // infoText.innerText = "Scanning QR Code...";
    fetch("http://api.qrserver.com/v1/read-qr-code/", {
        method: 'POST', body: formData
    }).then(res => res.json()).then(result => {
        result = result[0].symbol[0].data;
        // infoText.innerText = result ? "Upload QR Code to Scan" : "Couldn't scan QR Code";
        if(!result) return;


        let value1 = "FLU";
        let value2 = "FLF";

        if (result.substring(0, 3) == value1 || result.substring(0, 3) == value2){
        // code to run if the first three letters of both values are equal
        console.log("First three letters are correct");
        document.getElementById('qrreader').value = result;
        } else {
        // code to run if the first three letters of both values are not equal
        console.log("First three letters are incorrect");
        document.getElementById('qrreader').value = "";
        }
        
        // document.querySelector("textarea").innerText = result;
        // form.querySelector("img").src = URL.createObjectURL(file);
        wrapper.classList.add("active");
    })
    // .catch(() => {
    //     infoText.innerText = "Couldn't scan QR Code";
    // });
}

fileInp.addEventListener("change", async e => {
    let file = e.target.files[0];
    if(!file) return;
    let formData = new FormData();
    formData.append('file', file);
    fetchRequest(file, formData);
});

// copyBtn.addEventListener("click", () => {
//     let text = document.querySelector("textarea").textContent;
//     navigator.clipboard.writeText(text);
// });

form.addEventListener("click", () => fileInp.click());
// closeBtn.addEventListener("click", () => wrapper.classList.remove("active"));