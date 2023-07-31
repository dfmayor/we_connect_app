// function to fetch and display services

let services = []; // Array to store the fetched services
  const chunkSize = 5
  let start = 0;
  let end = chunkSize;

  // JavaScript function to display services
  function displayServices() {
    const container = document.getElementById('services-container');
    container.innerHTML = '';

    // Display the current chunk of services
    const currentChunk = services.slice(start, end);
    if (currentChunk.length === 0) {
      const noDataDiv = document.createElement('div');
      noDataDiv.innerText = 'No more data';
      container.appendChild(noDataDiv);
    } else {
      const serviceDiv = document.createElement('div');
      serviceDiv.classList.add('text-center');
      const rowDiv = document.createElement('div');
      rowDiv.classList.add('row');
      serviceDiv.appendChild(rowDiv);
      currentChunk.forEach((service) => {
        const colDiv = document.createElement('div');
        colDiv.classList.add('col');

        colDiv.innerHTML = `
          <div class="card mb-3" style="width: 18rem;">
            <img src="${service.picture}" class="card-img-top" alt="...">
            <div class="card-body">
              <h5 class="card-title">${service.title}</h5>
              <h6 class="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
              <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
              <a href="#" class="card-link">Card link</a>
              <a href="#" class="card-link">Another link</a>
            </div>
          </div>
        `;
        // Customize how you want to display the service data
        //serviceDiv.innerHTML = `<h2>${service.title}</h2><p>${service.user}</p>`;
        rowDiv.appendChild(colDiv);
      });
      container.appendChild(serviceDiv);
    }
  }

  // Fetch services from Django view using AJAX
  function fetchServices() {
    fetch('/services/get_services/') // Replace this with the URL of your Django view
      .then((response) => response.json())
      .then((data) => {
        services = data.services;
        displayServices();
      })
      .catch((error) => console.error('Error fetching services:', error));
  }

  // Call the fetchServices function when the page loads
  fetchServices();

  // Previous and Next buttons event listeners
  document.getElementById('prev-btn').addEventListener('click', () => {
    if (start - chunkSize >= 0) {
      start -= chunkSize;
      end -= chunkSize;
      displayServices();
    }
  });

  document.getElementById('next-btn').addEventListener('click', () => {
    if (end < services.length) {
      start += chunkSize;
      end += chunkSize;
      displayServices();
    }
  });
