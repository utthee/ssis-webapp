// DATA TABLE INITIALIZATION
$(document).ready(function(){
    $('#data-table').DataTable();
});

// CHART INITIALIZATION
document.addEventListener("DOMContentLoaded", () => {
    const chartCanvas = document.getElementById("donutChart");
    if (chartCanvas) {
        const labels = JSON.parse(chartCanvas.dataset.labels);
        const data = JSON.parse(chartCanvas.dataset.values);

        new Chart(chartCanvas, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        "#007bff","#28a745","#ffc107","#dc3545",
                        "#17a2b8","#6f42c1","#fd7e14","#20c997"
                    ]
                }]
            },
            options: {
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }
});


// TOGGLE BUTTON FOR SIDEBAR COLLAPSE/EXPAND
$(".toggler-btn").click(function() {
    $("#sidebar").toggleClass("collapsed");
});

// CHANGE DASHBOARD TITLE TO THE PAGE
$("#sidebar .sidebar-link").click(function() {
    var pageTitle = $(this).data("title");
    $("#page-title").text(pageTitle);
});

$('.modal').on('hidden.bs.modal', function () {
    document.activeElement.blur();
});

// -------------    EVENT HANDLER   -------------
//
//                  EVENT HANDLER
//
// -------------    EVENT HANDLER   -------------


$("#programCode, #collegeCode").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[a-zA-Z]/.test(e.key)) {
        e.preventDefault();
    }
    if (e.type === "input") {
        $(this).val($(this).val().replace(/[^a-zA-Z]/g, ''));
    }
});

$("#firstName, #lastName, #programNamem #collegeName").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[a-zA-Z\s]/.test(e.key)) {
        e.preventDefault();
    }
    if (e.type === "input") {
        $(this).val($(this).val().replace(/[^a-zA-Z\s]/g, ''));
    }
});


// -------------    STUDENT PAGE   -------------
//
//                     STUDENT
//
// -------------    STUDENT PAGE   -------------


// SHOW REGISTER CONFIRMATION MESSAGE
$("#registerStudentForm").submit(function(e) {
    e.preventDefault();
    $("#registerStudentForm input").removeClass("is-invalid");

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#registerStudentModal").modal("hide");
            
            showConfirmationModal(
                'Student Registered Successfully',
                'Student has been successfully registered.'
            );

            $("#registerStudentForm")[0].reset();

            $("#confirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


//POPULATE STUDENT EDIT FORM
$('#editStudentModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var idNumber   = button.data('id-number');
    var firstName  = button.data('first-name');
    var lastName   = button.data('last-name');
    var gender     = button.data('gender');
    var yearLevel  = button.data('year-level');
    var program    = button.data('program-code');

    modal.find('#idNumber').val(idNumber);
    modal.find('#firstName').val(firstName);
    modal.find('#lastName').val(lastName);
    modal.find('#gender').val(gender);
    modal.find('#yearLevel').val(yearLevel);
    modal.find('#programCode').val(program);
    modal.find('#originalIdNumber').val(idNumber);
});


//SHOW EDIT STUDENT CONFIRMATION MESSAGE
$('#editStudentForm').submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editStudentModal").modal("hide");

            showConfirmationModal(
                'Student Edited Successfully',
                'Student data has been successfully updated.'
            );

            $("#confirmationModal").off("hidden.bs.modal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


/// POPULATE HIDDEN INPUT
$('#deleteStudentModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var idNumber = button.data('id-number');

    $(this).find('#deleteIdNumber').val(idNumber);
});


// SHOW DELETE STUDENT CONFIRMATION MESSAGE
$("#deleteStudentForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#deleteStudentModal").modal("hide");

            showConfirmationModal(
                'Student Deleted',
                'Student has been successfully deleted.'
            );

            $("#confirmationModal").off("hidden.bs.modal").on("hidden.bs.modal", function () {
                location.reload();
            });

        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


// -------------    PROGRAMS PAGE   -------------
//
//                     PROGRAMS
//
// -------------    PROGRAMS PAGE   -------------


// SHOW REGISTER PROGRAM MODAL
$("#registerProgramForm").submit(function(e) {
    e.preventDefault();
    $("#registerProgramForm input").removeClass("is-invalid");

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#registerProgramModal").modal("hide");
            
            showConfirmationModal(
                'Program Registered Successfully',
                'Program has been successfully registered.'
            );

            $("#registerProgramForm")[0].reset();

            $("#confirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


// SHOW/POPULATE EDIT PROGRAM MODAL
$('#editProgramModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var programCode = button.data('program-code');
    var programName = button.data('program-name');
    var collegeCode = button.data('college-code');

    modal.find('#programCode').val(programCode);
    modal.find('#programName').val(programName);
    modal.find('#collegeCode').val(collegeCode);
    modal.find('#originalProgramCode').val(programCode);
});


// SHOW EDIT PROGRAM CONFIRMATION MESSAGE
$('#editProgramForm').submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editProgramModal").modal("hide");

            showConfirmationModal(
                'Program Edited Successfully',
                'Program data has been successfully updated.'
            );

            $("#confirmationModal").off("hidden.bs.modal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


/// POPULATE HIDDEN INPUT
$('#deleteProgramModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var code = button.data('program-code');

    $(this).find('#deleteProgramCode').val(code);
});


// SHOW DELETE PROGRAM CONFIRMATION MESSAGE
$("#deleteProgramForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#deleteProgramModal").modal("hide");

            showConfirmationModal(
                'Program Deleted',
                'Program has been successfully deleted.'
            );

            $("#confirmationModal").off("hidden.bs.modal").on("hidden.bs.modal", function () {
                location.reload();
            });

        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});



// -------------    COLLEGES PAGE   -------------
//
//                     COLLEGE
//
// -------------    COLLEGES PAGE   -------------


// SHOW REGISTER COLLEGE MODAL
$("#registerCollegeForm").submit(function(e) {
    e.preventDefault();
    $("#registerCollegeForm input").removeClass("is-invalid");

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#registerCollegeModal").modal("hide");

            showConfirmationModal(
                'College Registered Successfully',
                'College has been successfully registered.'
            );

            $("#registerCollegeForm")[0].reset();

            $("#confirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


// SHOW/POPULATE COLLEGE EDIT FORM
$('#editCollegeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var code = button.data('college-code');
    var name = button.data('college-name');

    modal.find('#collegeCode').val(code);
    modal.find('#collegeName').val(name);
    modal.find('#originalCollegeCode').val(code);
});


// SHOW EDIT COLLEGE CONFIRMATION MESSAGE
$("#editCollegeForm").submit(function (e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editCollegeModal").modal("hide");

            showConfirmationModal(
                'College Edited Successfully',
                'College data has been successfully updated.'
            );

            $("#confirmationModal").off("hidden.bs.modal").on("hidden.bs.modal", function () {
                location.reload();
            });

        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


// POPULATE HIDDEN INPUT
$('#deleteCollegeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var code = button.data('college-code');

    $(this).find('#deleteCollegeCode').val(code);
});


// SHOW DELETE COLLEGE CONFIRMATION MESSAGE
$("#deleteCollegeForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#deleteCollegeModal").modal("hide");

            showConfirmationModal(
                'College Deleted',
                'College has been successfully deleted.'
            );

            $("#confirmationModal").off("hidden.bs.modal").on("hidden.bs.modal", function () {
                location.reload();
            });

        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) {
            alert("Error: " + xhr.responseJSON.message);
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});


function showConfirmationModal(title, message) {
    document.getElementById('confirmationModalLabel').textContent = title;
    document.getElementById('confirmationModalMessage').textContent = message;

    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();
}