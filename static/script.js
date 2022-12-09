const cupcakeGrid = document.querySelector(".cupcake_grid");







function newCupcakeMachine(imgURL, flavor, size, rating) {
    const newCupcake = document.createElement("div");
    newCupcake.className = "cupcake";
    const newImg = document.createElement("img");
    const flavorP = document.createElement("p");
    const sizeP = document.createElement("p");
    const ratingP = document.createElement("p");

    newImg.src = imgURL;
    flavorP.innerText = flavor;
    sizeP.innerText = `Size: ${size}`;
    ratingP.innerText = `Rating: ${rating}`;

    newCupcake.append(newImg, flavorP, sizeP, ratingP)
    cupcakeGrid.append(newCupcake)

}


async function getData() {
    const response = await axios.get(" http://127.0.0.1:5000/api/cupcakes");
    console.log(response.data)

    for (let data of response.data) {
        newCupcakeMachine(data['image'], data['flavor'], data['size'], data['rating'])
    }



}

getData()












