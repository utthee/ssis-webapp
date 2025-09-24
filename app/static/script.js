$(document).ready(function(){
    $('#data-table').DataTable();
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

// ---------- STUDENTS PAGE ----------
// SHOW REGISTER CONFIRMATION MESSAGE
$("#registerForm").submit(function(e) {
    e.preventDefault();
    $("#registerStudentModal").modal('hide');
    $("#confirmationModal").modal('show');
});

//POPULATE STUDENT EDIT FORM
$('#editStudentModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var idNumber   = button.data('student-id');
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
});

//SHOW EDIT CONFIRMATION MESSAGE
$("#editForm").submit(function(e) {
    e.preventDefault();
    $("#editStudentModal").modal('hide');
    $("#editConfirmationModal").modal('show');
});

// SHOW DELETE CONFIRMATION MESSAGE
$("#deleteForm").submit(function(e) {
    e.preventDefault();
    $("#deleteConfirmationModal").modal('hide');
    $("#deletionModal").modal('show');
});

// -------------    PROGRAMS PAGE   -------------
//
//                     PROGRAMS
//
// -------------    PROGRAMS PAGE   -------------

// SHOW REGISTER PROGRAM MODAL
$("#registerProgramForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#registerProgramModal").modal("hide");
            $("#registerConfirmationModal").modal("show");
            $("#registerProgramForm")[0].reset();

            $("#registerConfirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
});


// SHOW/POPULATE EDIT PROGRAM MODAL
$('.btn-edit').on('click', function() {
    var programCode = $(this).data('program-code');
    var programName = $(this).data('program-name');
    var collegeCode = $(this).data('college-code');

    var modal = $('#editProgramModal');
    modal.find('#programCode').val(programCode);
    modal.find('#programName').val(programName);
    modal.find('#collegeCode').val(collegeCode);
    modal.find('#originalProgramCode').val(programCode);

    console.log("Populating modal with:", programCode, programName, collegeCode);
});


// SHOW EDIT PROGRAM CONFIRMATION MESSAGE
$('#editProgramForm').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var actionUrl = form.attr('action');

    $.post(actionUrl, form.serialize(), function(response) {
        if (response.success) {
            $('#editProgramModal').modal('hide');
            $("#editProgramConfirmationModal").modal("show");

            $("#editProgramConfirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert("Update failed: " + response.message);
        }
    }).fail(function(xhr) {
        alert("Error: " + (xhr.responseJSON?.message || xhr.responseText || "Something went wrong"));
    });
});


/// POPULATE HIDDEN INPUT
$('.btn-delete').on('click', function() {
    var programCode = $(this).data('program-code');
    $('#deleteProgramCode').val(programCode);
});


// SHOW DELETE PROGRAM CONFIRMATION MESSAGE
$("#deleteForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#deleteConfirmationModal").modal("hide");
            $("#deletionModal").modal("show");

            setTimeout(() => {
                location.reload();
            }, 1200);
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
});



// -------------    COLLEGES PAGE   -------------
//
//                     COLLEGE
//
// -------------    COLLEGES PAGE   -------------

// SHOW REGISTER COLLEGE MODAL
$("#registerForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#registerCollegeModal").modal("hide");
            $("#registerConfirmationModal").modal("show");
            $("#registerForm")[0].reset();

            $("#registerConfirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
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
$("#editForm").submit(function (e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editCollegeModal").modal("hide");

            $("#editConfirmationModal").modal("show");

            $("#editConfirmationModal").on("hidden.bs.modal", function () {
                location.reload();
            });

        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
});


// POPULATE HIDDEN INPUT
$('#deleteConfirmationModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var code = button.data('college-code');

    $(this).find('#deleteCollegeCode').val(code);
});


// SHOW DELETE COLLEGE CONFIRMATION MESSAGE
$("#deleteForm").submit(function(e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function(response) {
        if (response.success) {
            $("#deleteConfirmationModal").modal("hide");
            $("#deletionModal").modal("show");

            setTimeout(() => {
                location.reload();
            }, 1200);
        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
});