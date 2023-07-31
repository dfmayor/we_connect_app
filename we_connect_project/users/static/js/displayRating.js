function displayRating(rating) {
  const roundedRating = Math.round(rating * 2) / 2; // Round the rating to the nearest 0.5
  const ratingContainer = document.querySelector('.rating-container');
  ratingContainer.innerHTML = ''; // Clear previous rating icons

  for (let i = 1; i <= roundedRating; i++) {
    const star = document.createElement('i');
    star.classList.add('fa-solid', 'fa-star', 'text-warning');
    if (i <= roundedRating) {
      star.classList.add('active');
    } else if (i === Math.ceil(roundedRating) && roundedRating % 1 !== 0) {
      star.classList.add('fa-solid', 'fa-star-half-stroke', 'text-warning');
    }

    ratingContainer.appendChild(star);
  }
}
