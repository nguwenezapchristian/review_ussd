// popup handling
function openPopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = 'block';
}
function closePopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = 'none';
}
// Function to handle new applicant enrollment
function enrollApplicant(applicantId, program){
    // send AJAX request to the flask application 
    $.ajax({
        type: 'POST', // USE POST METHOD
        url: '/enroll', //URL to flask endpoint or url route
        data: {// data to be sent in the POST request
            applicant_id : applicantId,
            program : program,
        },
        success: function(response) { // Callback function on success
            // Log success message to the console
            console.log('Applicant enrolled successfully');
            // Remove the row from the table upon successful enrollment
            $('#applicant_row_' + applicantId).remove();
        },
        error: function(error) { // Callback function on error
            // Log error message to the console
            console.error('Error enrolling applicant:', error);
        }
    });
}

// function to handle a dropping of an applicant
function dropApplicant(applicantId){
    // send AJAX  REQUEST TO THE FLASK APP
    $.ajax({
        type: 'POST',
        url: '/drop',
        data: {
            applicant_id : applicantId // applicant ID
        },
        success: function(response){// call back function on success
            // log success message the console
            console.log('Applicant Dropped successfully');
            // remove the row from the table upon successfull dropping
            $('#application_row_' + applicantId).remove();

        },
        error: function(error) {// callback function on error
            // log error to the console
            console.error('Error dropping  applicant:', error);
        }
    });
    
}

// function to handle pending applicants
function pendingApplicant(applicantId){
    var reason = document.getElementById("reasonInput").value;
    // send AJAX  REQUEST TO THE FLASK APP
    $.ajax({
        type: 'POST',
        url: '/pending',
        data: {
            applicant_id : applicantId, // applicant ID
            reason : reason
        },
        success: function(response){// call back function on success
            // log success message the console
            console.log('Applicant Dropped successfully');
            // remove the row from the table upon successfull dropping
            $('#application_row_' + applicantId).remove();

        },
        error: function(error) {// callback function on error
            // log error to the console
            console.error('Error dropping  applicant:', error);
        }
    });
    document.getElementById("pending-popupContainer").style.display = "none";
}

//  Enroll the applicant from the pending list
function ReenrollApplicant(studentId, program){
    // send ajax request
    $.ajax({ 
        type: 'POST',
        url: '/reenroll',
        data: {
            student_id : studentId,
            program : program
        },
        success: function(response) { // Callback function on success
            // Log success message to the console
            console.log('Applicant enrolled successfully');
            // Remove the row from the table upon successful enrollment
            $('#applicant_row_' + studentId).remove();
        },
        error: function(error) { // Callback function on error
            // Log error message to the console
            console.error('Error enrolling applicant:', error);
        }
    });
    document.getElementById("pending-popupContainer").style.display = "none";
}

// function to Enroll the dropped applicant
function enrollDropped(studentId, program){
    // send ajax request
    $.ajax({
        type: 'POST',
        url: '/enrollment',
        data: {
            student_id : studentId,
            program : program
        },
        success: function (response) {
            console.log('drop success')
            $('#applicant_row_'+studentId).remove();
        },
        error: function(error) {
            console.error('Error when dropping')
            $('#applicant_row_'+studentId).remove()
        }
    });
}

// function to shift the student day to evening
function shiftApplicant(studentId, studentEmail){
    // send ajax request
    $.ajax({
        type: 'POST',
        url: '/shift_to_evening',
        data: {
            student_id : studentId,
            student_email: studentEmail, 
        },
        success: function (response) {
            console.log('drop success')
            $('#applicant_row_'+studentId).remove();
        },
        error: function(error) {
            console.error('Error when dropping')
            $('#applicant_row_'+studentId).remove()
        }

    });
    document.getElementById('shiftPopupContainer').style.display='none'
}

function dropFromDay(studentId){
    // send ajax request
    $.ajax({
        type: 'POST',
        url: '/drop_from_day',
        data: {
            student_id : studentId
        },
        success: function (response) {
            console.log('drop success')
            $('#applicant_row_'+studentId).remove();
        },
        error: function(error) {
            console.error('Error when dropping')
            $('#applicant_row_'+studentId).remove()
        }

    })
}

// function to shift the student from evening to day
function shiftEveningApplicant(studentId, studentEmail){
    // send ajax request
    $.ajax({
        type: 'POST',
        url: '/shift_to_day',
        data: {
            student_id : studentId,
            student_email: studentEmail
        },
        success: function (response) {
            console.log('drop success')
            $('#applicant_row_'+studentId).remove();
        },
        error: function(error) {
            console.error('Error when dropping')
            $('#applicant_row_'+studentId).remove()
        }

    });
    document.getElementById('shiftPopupContainer').style.display='none'
}

function dropFromEvening(studentId){
    // send ajax request
    $.ajax({
        type: 'POST',
        url: '/drop_from_evening',
        data: {
            student_id : studentId
        },
        success: function (response) {
            console.log('drop success')
            $('#applicant_row_'+studentId).remove();
        },
        error: function(error) {
            console.error('Error when dropping')
            $('#applicant_row_'+studentId).remove()
        }

    })
}