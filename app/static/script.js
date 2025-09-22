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

// ---------- PROGRAMS PAGE ----------
$("#registerForm").submit(function(e) {
    e.preventDefault();
    $("#registerProgramModal").modal('hide');
    $("#registerConfirmationModal").modal('show');
});

//POPULATE PROGRAM EDIT FORM
$('#editProgramModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var programCode = button.data('program-code');
    var programName = button.data('program-name');
    var collegeCode = button.data('college-code');

    modal.find('#programCode').val(programCode);
    modal.find('#programName').val(programName);
    modal.find('#collegeCode').val(collegeCode);
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

//POPULATE COLLEGE EDIT FORM
$('#editCollegeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var code = button.data('college-code');
    var name = button.data('college-name');

    modal.find('#collegeCode').val(code);
    modal.find('#collegeName').val(name);
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