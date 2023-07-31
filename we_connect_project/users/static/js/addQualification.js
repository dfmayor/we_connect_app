let qualificationIndex = 0;
function addQualification() {
    const createProfile = document.getElementById('createPro');
    const saveEdu = document.getElementById('saveEdu');
    const qualificationsDiv = document.getElementById('educationalQualifications');

    createProfile.style.display = 'none';
    saveEdu.style.display = 'block';
    const newQualification = document.createElement('div');
    //newQualification.classList.add('qualification');
    newQualification.innerHTML = `
      <p>Add Education:</p>
      <div class="input-group mb-3">
        <span class="input-group-text">
          <i class="fa-solid fa-location-dot"></i>
        </span>
        <input type="text" id="school_${qualificationIndex}" class="form-control" placeholder="Enter School Name">
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">
          <i class="fa-solid fa-location-dot"></i>
        </span>
        <input type="text" id="qualification_${qualificationIndex}" class="form-control" placeholder="What is your qualification?">
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">
          <i class="fa-solid fa-location-dot"></i>
        </span>
        <input type="text" id="course_${qualificationIndex}" class="form-control" placeholder="Your Course Of Study">
      </div>
      <div class="input-group mb-3">
        <label for='graduation_year'>Graduation Year:</label><br>
        <span class="input-group-text">
          <i class="fa-solid fa-location-dot"></i>
        </span>
        <input type="date" id="graduation_year_${qualificationIndex}" class="form-control">
      </div>
    `;
    qualificationsDiv.appendChild(newQualification);
    qualificationIndex ++;
}

function saveEducation() {
  // get user id
  const userId = document.getElementById('user_id');
  const qualificationsDiv = document.getElementById('educationalQualifications');
  const addEdu = document.getElementById('add');
  const createPro = document.getElementById('createPro');
  const saveEduc = document.getElementById('saveEdu');

  addEdu.style.display = 'none';
  saveEduc.style.display = 'none';
  createPro.style.display = 'block';
  // create an array to save the educational qualifications
  const qualifications = [];

  for (let i = 0; i < qualificationIndex; i++) {
    const school = document.getElementById(`school_${i}`).value;
    const qualification = document.getElementById(`qualification_${i}`).value;
    const course = document.getElementById(`course_${i}`).value;
    const graduationYear = document.getElementById(`graduation_year_${i}`).value;

    qualifications.push({
      school: school, qualification: qualification, course: course, graduation_year: graduationYear
    });
  }

  fetch('/users/save_education/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId, qualifications: qualifications
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      qualificationsDiv.innerHTML = '';
      successElement = document.createElement('div');
      successElement.classList.add("alert")
      successElement.classList.add("alert-success")
      successElement.innerHTML = `
        <p class="text-center">${data.message}</p>
      `
    } else {
      qualificationsDiv.innerHTML = '';
      successElement = document.createElement('div');
      successElement.classList.add("alert alert-danger")
      successElement.innerHTML = `
        <p class="text-center">${data.message}</p>
      `
    }
  })
  .catch(error => {
    console.log('Error', error)
  })
}