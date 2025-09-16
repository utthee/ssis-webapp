// TOGGLE BUTTON FOR SIDEBAR COLLAPSE/EXPAND
$(".toggler-btn").click(function() {
    $("#sidebar").toggleClass("collapsed");
});

// CHANGE DASHBOARD TITLE TO THE PAGE
$(".sidebar-link").click(function(e) {
    $(".sidebar-link").removeClass("active");
    $(this).addClass("active");
});

// ---------- STUDENTS PAGE ----------
// SHOW REGISTER CONFIRMATION MESSAGE
$("#registerForm").submit(function(e) {
    e.preventDefault();
    $("#registerStudentModal").modal('hide');
    $("#confirmationModal").modal('show');
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

// ---------- PROGRAMS PAGE ----------
$("#registerForm").submit(function(e) {
    e.preventDefault();
    $("#registerProgramModal").modal('hide');
    $("#registerConfirmationModal").modal('show');
});

//SHOW EDIT CONFIRMATION MESSAGE
$("#editForm").submit(function(e) {
    e.preventDefault();
    $("#editProgramModal").modal('hide');
    $("#editConfirmationModal").modal('show');
});

// SHOW DELETE CONFIRMATION MESSAGE
$("#deleteForm").submit(function(e) {
    e.preventDefault();
    $("#deleteConfirmationModal").modal('hide');
    $("#deletionModal").modal('show');
});

// ---------- COLLEGES PAGE ----------
$("#registerForm").submit(function(e) {
    e.preventDefault();
    $("#registerCollegeModal").modal('hide');
    $("#registerConfirmationModal").modal('show');
});

//SHOW EDIT CONFIRMATION MESSAGE
$("#editForm").submit(function(e) {
    e.preventDefault();
    $("#editCollegeModal").modal('hide');
    $("#editConfirmationModal").modal('show');
});

// SHOW DELETE CONFIRMATION MESSAGE
$("#deleteForm").submit(function(e) {
    e.preventDefault();
    $("#deleteConfirmationModal").modal('hide');
    $("#deletionModal").modal('show');
});