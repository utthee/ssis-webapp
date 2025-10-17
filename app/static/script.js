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
    $("#sidebar").addClass("animate");
    $(".main").addClass("animate-sidebar");
    $("#sidebar").toggleClass("collapsed");
    
    if ($("#sidebar").hasClass("collapsed")) {
        sessionStorage.setItem('sidebarCollapsed', 'true');
    } else {
        sessionStorage.setItem('sidebarCollapsed', 'false');
    }
    
    setTimeout(function() {
        $("#sidebar").removeClass("animate");
        $(".main").removeClass("animate-sidebar");
    }, 250);
});

// RETAIN SIDEBAR STATE WHEN GOING TO A DIFFERENT PAGE
$(document).ready(function() {
    if (sessionStorage.getItem('sidebarCollapsed') === 'true') {
        $("#sidebar").addClass("collapsed");
    } else if (sessionStorage.getItem('sidebarCollapsed') === 'false') {
        $("#sidebar").removeClass("collapsed");
    }
});

// CHANGE DASHBOARD TITLE TO THE PAGE
$("#sidebar .sidebar-link").click(function() {
    var pageTitle = $(this).data("title");
    $("#page-title").text(pageTitle);
});

$('.modal').on('hidden.bs.modal', function () {
    document.activeElement.blur();
});

// TOAST GREETINGS
$(document).ready(function() {
    $('.toast').each(function() {
        $(this).toast('show');
    });
});

// DATA TABLE INITIALIZATION
$(document).ready(function () {
    function initializeTableSearch(tableId, filterId, searchId, pageLength = 10) {
        if ($(tableId).length === 0) {
            return;
        }

        const dataTable = $(tableId).DataTable({
            pageLength: pageLength,
            lengthChange: false,
            searching: true,
            dom: '<"row"<"col-sm-12"tr>><"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7 d-flex justify-content-end"p>>',
        });

        const filterSelect = $(filterId);
        const searchInput = $(searchId);

        if (filterSelect.length && searchInput.length) {
            searchInput.on("keyup", function () {
                const searchValue = $(this).val();
                const columnIndex = parseInt(filterSelect.val());

                dataTable.search("").columns().search("");

                if (columnIndex === -1) {
                    dataTable.search(searchValue);
                } else {
                    dataTable.column(columnIndex).search(searchValue);
                }
                
                dataTable.draw();
            });

            filterSelect.on("change", function () {
                searchInput.val("");
                dataTable.search("").columns().search("").draw();
            });
        }
    }
    initializeTableSearch("#college-table", "#searchByFilterCollege", "#searchFieldCollege");
    initializeTableSearch("#program-table", "#searchByFilterProgram", "#searchFieldProgram");
    initializeTableSearch("#student-table", "#searchByFilterStudent", "#searchFieldStudent");
});

// -------------    EVENT HANDLER   -------------
//
//                  EVENT HANDLER
//
// -------------    EVENT HANDLER   -------------


$("#registerIdNumber").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[0-9\-]/.test(e.key)){
        e.preventDefault();
    }
    if (e.type === "input") {
        $(this).val($(this).val().replace(/[^0-9\-]/g, ''));
    }
});

$("#firstName, #lastName").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[a-zA-Z\s]/.test(e.key)) {
        e.preventDefault();
    }
    if (e.type === "input") {
        $(this).val($(this).val().replace(/[^a-zA-Z\s]/g, ''));
    }
});

$("#registerProgramCode, #editProgramCode, #registerCollegeCode, #editCollegeCode").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[a-zA-Z]/.test(e.key)) {
        e.preventDefault();
    }
    if (e.type === "input") {
        $(this).val($(this).val().replace(/[^a-zA-Z]/g, ''));
    }
});

$("#registerProgramName, #editProgramName, #registerCollegeName, #editCollegeName").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[a-zA-Z\s,]/.test(e.key)) {
        e.preventDefault();
    }
    if (e.type === "input") {
        $(this).val($(this).val().replace(/[^a-zA-Z\s,]/g, ''));
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
            
            sessionStorage.setItem('showRegisterStudentSuccess', 'true');

            location.reload();

        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
            const response = xhr.responseJSON;

            if (response.field == "id_number") {
                $("#registerIdNumber").addClass("is-invalid");
                $("#registerIdNumberError").text(response.message).show();
                $("#registerIdNumber").focus()
            } else {
                alert("Error: " + response.message);
            }
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

    modal.find('#editIdNumber').val(idNumber);
    modal.find('#editFirstName').val(firstName);
    modal.find('#editLastName').val(lastName);
    modal.find('#editGender').val(gender);
    modal.find('#editYearLevel').val(yearLevel);
    modal.find('#editProgramCode').val(program);
    modal.find('#originalIdNumber').val(idNumber);
});


//SHOW EDIT STUDENT CONFIRMATION MESSAGE
$('#editStudentForm').submit(function(e) {
    e.preventDefault();
    $('#editStudentForm input').removeClass("is-invalid");

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editStudentModal").modal("hide");

            sessionStorage.setItem('showEditStudentSuccess', 'true');

            location.reload();

        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
            const response = xhr.responseJSON;

            if (response.message === "No changes detected.") {
                $("#editStudentModal").modal("hide");
                return;
            }

            if (response.field == "id_number") {
                $("#editIdNumber").addClass("is-invalid");
                $("#editIdNumberError").text(response.message).show();
                $("#editIdNumber").focus()
            } else{
                alert("Error: " + response.message);
            }
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});

$("#editStudentModal").on("hidden.bs.modal", function() {
    $("#editStudentForm")[0].reset();
    $("#editStudentForm input").removeClass("is-invalid");
    $("#editStudentForm .invalid-feedback").hide().text("");
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

            sessionStorage.setItem('showDeleteStudentSuccess', 'true');

            location.reload();

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


$(document).ready(function() {
    if (sessionStorage.getItem('showRegisterStudentSuccess') === 'true') {
        sessionStorage.removeItem('showRegisterStudentSuccess');

        showConfirmationModal(
            'Student Registered Successfully',
            'Student record has been successfully registered.'
        );
    }

    if (sessionStorage.getItem('showEditStudentSuccess') === 'true') {
        sessionStorage.removeItem('showEditStudentSuccess');

        showConfirmationModal(
            'Student Edited Successfully',
            'Student record has been successfully updated.'
        );
    }
    
    if (sessionStorage.getItem('showDeleteStudentSuccess') === 'true') {
        sessionStorage.removeItem('showDeleteStudentSuccess');
        
        showConfirmationModal(
            'Student Deleted',
            'Student record has been permanently deleted.'
        );
    }
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

            sessionStorage.setItem('showRegisterProgramSuccess', 'true');
            
            location.reload();

        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
            const response = xhr.responseJSON

            if (response.field == "program_code") {
                $("#registerProgramCode").addClass("is-invalid");
                $("#registerProgramCodeError").text(response.message).show();
                $("#registerProgramCode").focus()
            } else if (response.field == "program_name") {
                $("#registerProgramName").addClass("is-invalid");
                $("#registerProgramNameError").text(response.message).show();
                $("#registerProgramName").focus()
            } else{
                alert("Error: " + response.message);
            }
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});

$("#registerProgramModal").on("hidden.bs.modal", function() {
    $("#registerProgramForm")[0].reset();
    $("#registerProgramForm input").removeClass("is-invalid");
    $("#registerProgramForm .invalid-feedback").hide().text("");
});


// SHOW/POPULATE EDIT PROGRAM MODAL
$('#editProgramModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var programCode = button.data('program-code');
    var programName = button.data('program-name');
    var collegeCode = button.data('college-code');

    modal.find('#editProgramCode').val(programCode);
    modal.find('#editProgramName').val(programName);
    modal.find('#editCollegeCode').val(collegeCode);
    modal.find('#originalProgramCode').val(programCode);
    modal.find('#originalProgramName').val(programName);
});


// SHOW EDIT PROGRAM CONFIRMATION MESSAGE
$('#editProgramForm').submit(function(e) {
    e.preventDefault();
    $('#editProgramForm input').removeClass("is-invalid");

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editProgramModal").modal("hide");

            sessionStorage.setItem('showEditProgramSuccess', 'true');
            
            location.reload();

        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
            const response = xhr.responseJSON;

            if (response.message === "No changes detected.") {
                $("#editProgramModal").modal("hide");
                return;
            }

            if (response.field == "program_code") {
                $("#editProgramCode").addClass("is-invalid");
                $("#editProgramCodeError").text(response.message).show();
                $("#editProgramCode").focus()
            } else if (response.field == "program_name") {
                $("#editProgramName").addClass("is-invalid");
                $("#editProgramNameError").text(response.message).show();
                $("#editProgramName").focus()
            } else{
                alert("Error: " + response.message);
            }
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});

$("#editProgramModal").on("hidden.bs.modal", function() {
    $("#editProgramForm")[0].reset();
    $("#editProgramForm input").removeClass("is-invalid");
    $("#editProgramForm .invalid-feedback").hide().text("");
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

            sessionStorage.setItem('showDeleteProgramSuccess', 'true');
            
            location.reload();

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


$(document).ready(function() {
    if (sessionStorage.getItem('showRegisterProgramSuccess') === 'true') {
        sessionStorage.removeItem('showRegisterProgramSuccess');

        showConfirmationModal(
            'Program Registered Successfully',
            'Program record has been successfully registered.'
        );
    }

    if (sessionStorage.getItem('showEditProgramSuccess') === 'true') {
        sessionStorage.removeItem('showEditProgramSuccess');

        showConfirmationModal(
            'Program Edited Successfully',
            'Program record has been successfully updated.'
        );
    }
    
    if (sessionStorage.getItem('showDeleteProgramSuccess') === 'true') {
        sessionStorage.removeItem('showDeleteProgramSuccess');
        
        showConfirmationModal(
            'Program Deleted',
            'Program record has been permanently deleted.'
        );
    }
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

            sessionStorage.setItem('showRegisterCollegeSuccess', 'true');
            
            location.reload();

        } else {
            alert(response.message);
        }
    }).fail(function(xhr) {
        if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
            const response = xhr.responseJSON;
            
            if (response.field === "college_code") {
                $("#registerCollegeCode").addClass("is-invalid");
                $("#registerCollegeCodeError").text(response.message).show();
                $("#registerCollegeCode").focus();
            } else if (response.field === "college_name") {
                $("#registerCollegeName").addClass("is-invalid");
                $("#registerCollegeNameError").text(response.message).show();
                $("#registerCollegeName").focus();
            } else {
                alert("Error: " + response.message);
            }
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});

$("#registerCollegeModal").on("hidden.bs.modal", function() {
    $("#registerCollegeForm")[0].reset();
    $("#registerCollegeForm input").removeClass("is-invalid");
    $("#registerCollegeForm .invalid-feedback").hide().text("");
});

// SHOW/POPULATE COLLEGE EDIT FORM
$('#editCollegeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal  = $(this);

    var collegeCode = button.data('college-code');
    var collegeName = button.data('college-name');

    modal.find('#editCollegeCode').val(collegeCode);
    modal.find('#editCollegeName').val(collegeName);
    modal.find('#originalCollegeCode').val(collegeCode);
    modal.find('#originalCollegeName').val(collegeName);
});


// SHOW EDIT COLLEGE CONFIRMATION MESSAGE
$("#editCollegeForm").submit(function (e) {
    e.preventDefault();
    $("#editCollegeForm input").removeClass("is-invalid");

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
        if (response.success) {
            $("#editCollegeModal").modal("hide");

            sessionStorage.setItem('showEditCollegeSuccess', 'true');
            
            location.reload();


        } else {
            alert(response.message);
        }
    }).fail(function (xhr) {
        if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
            const response = xhr.responseJSON;
            
            if (response.message === "No changes detected.") {
                $("#editCollegeModal").modal("hide");
                return;
            }

            if (response.field === "college_code") {
                $("#editCollegeCode").addClass("is-invalid");
                $("#editCollegeCodeError").text(response.message).show();
                $("#editCollegeCode").focus();
            } else if (response.field === "college_name") {
                $("#editCollegeName").addClass("is-invalid");
                $("#editCollegeNameError").text(response.message).show();
                $("#editCollegeName").focus();
            } else {
                alert("Error: " + response.message);
            }
        } else if (xhr.status === 403) {
            alert("CSRF token validation failed. Please refresh the page and try again.");
        } else {
            alert("Error: Something went wrong");
        }
    });
});

$("#editCollegeModal").on("hidden.bs.modal", function() {
    $("#editCollegeForm")[0].reset();
    $("#editCollegeForm input").removeClass("is-invalid");
    $("#editCollegeForm .invalid-feedback").hide().text("");
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

            sessionStorage.setItem('showDeleteCollegeSuccess', 'true');
            
            location.reload();

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

$(document).ready(function() {
    if (sessionStorage.getItem('showRegisterCollegeSuccess') === 'true') {
        sessionStorage.removeItem('showRegisterCollegeSuccess');

        showConfirmationModal(
            'College Registered Successfully',
            'College record has been successfully registered.'
        );
    }

    if (sessionStorage.getItem('showEditCollegeSuccess') === 'true') {
        sessionStorage.removeItem('showEditCollegeSuccess');

        showConfirmationModal(
            'College Edited Successfully',
            'College record has been successfully updated.'
        );
    }
    
    if (sessionStorage.getItem('showDeleteCollegeSuccess') === 'true') {
        sessionStorage.removeItem('showDeleteCollegeSuccess');
        
        showConfirmationModal(
            'College Deleted',
            'College record has been permanently deleted.'
        );
    }
});


function showConfirmationModal(title, message) {
    $('#confirmationModalLabel').text(title);
    $('#confirmationModalMessage').text(message);
    $('#confirmationModal').modal('show');
}