const weatherForm = document.querySelector(".weatherForm");
const cityInput = document.querySelector(".cityInput");
const card = document.querySelector(".card");
const apiKey = "571e0934ec0fa7c2096b90f8498fe253";

/**** weather form ****/

weatherForm.addEventListener("submit", async event => {
    event.preventDefault();
    const city = cityInput.value;
    if (city) {
        try {
            const weatherData = await getWeatherData(city);
            displayWeatherInfo(weatherData);

            saveCity(city);

            
        }
        catch (error) {
            console.error(error);
            displayError(error);
        }
    }
    else {
        displayError("Please enter a City!");
    }
});

/*** weather data fetch ****/

async function getWeatherData(city) {
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}`;
    const response = await fetch(apiUrl);

    if (!response.ok) {
        throw new Error("Could not fetch weather data");
    }

    return await response.json();
}

/**** weather card display ****/

function displayWeatherInfo(data) {

    const { name: city,
        coord: {lon , lat},
        main: { temp, humidity },
        weather: [{ description, id }] } = data;

    card.textContent= "";
    card.style.visibility="visible";

    pinCity(lon , lat);
    
    const cityDisplay = document.createElement("h1");
    const tempDisplay = document.createElement("p");
    const humidityDisplay = document.createElement("p");
    const descp = document.createElement("p");
    const emojiDisplay = document.createElement("p")

    cityDisplay.textContent = city;
    tempDisplay.textContent = `${(temp - 273.15).toFixed(1)}°C`;
    humidityDisplay.textContent = `humidity: ${humidity}`;
    descp.textContent = description;
    emojiDisplay.textContent = getWeatherEmoji(id);

    cityDisplay.classList.add("cityDisplay");
    tempDisplay.classList.add("tempDisplay");
    humidityDisplay.classList.add("humidityDisplay");
    descp.classList.add("descp");
    emojiDisplay.classList.add("emojiDisplay");

    card.appendChild(cityDisplay);
    card.appendChild(tempDisplay);
    card.appendChild(humidityDisplay);
    card.appendChild(descp);
    card.appendChild(emojiDisplay);
    
}

/**** weather emoji ****/

function getWeatherEmoji(weatherId) {
    switch(true){
        case (weatherId >= 200 && weatherId <300):
            return  "⛈️";
        case (weatherId >= 300 && weatherId <400):
            return  "🌦️";
        case (weatherId >= 500 && weatherId <600):
            return  "☔";
        case (weatherId >= 600 && weatherId <700):
            return  "❄️";
        case (weatherId >= 700 && weatherId <800):
            return  "🌫️";
        case (weatherId === 800):
            return  "🌞";
        case (weatherId >= 801 && weatherId <810):
            return  "☁️";
        default:
            return "⁉️"  
    }

}

/*** pin a city on map ***/
function pinCity(lon, lat){
    const map = document.querySelector(".map");
    const pinContainer= document.querySelector("#pinContainer");

    pinContainer.innerHTML = "";

    const pin = document.createElement("div");
    pin.classList.add("pin");

    const x = ((lon + 182)/360)* map.clientWidth;
    const y = ((112 - lat)/180)* map.clientHeight;
    
    pin.style.left = `${x}px`;
    pin.style.top = `${y}px`;

    pinContainer.appendChild(pin);
}


/**** error display ****/

function displayError(message) {
    const errorDisplay = document.createElement("p");
    errorDisplay.textContent = message;
    errorDisplay.classList.add("errorDisplay");


    card.textContent = "";
    card.style.visibility="visible";
    card.appendChild(errorDisplay);

}

/*** getting weather form history ***/

window.addEventListener("DOMContentLoaded", async () => {
    const savedCity = localStorage.getItem("selectedCity");
    if (savedCity) {
        cityInput.value = savedCity;
        const weatherData = await getWeatherData(savedCity);
        displayWeatherInfo(weatherData);
        localStorage.removeItem("selectedCity");
    }
});

/**** saving history ****/

function saveCity(cityName) {
    fetch('/history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: cityName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('City saved!');
        }
    });
}

/*** aleart message ***/

document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll('.flash-message');
    setTimeout(() => {
        messages.forEach(msg => msg.classList.add('hide'));
    }, 3000);
});