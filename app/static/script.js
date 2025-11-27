
// TOGGLE BUTTON FOR SIDEBAR COLLAPSE/EXPAND
$(document).ready(function () {
    $(".toggler-btn").click(function () {
        $("#sidebar").addClass("animate");
        $(".main").addClass("animate-sidebar");
        $("#sidebar").toggleClass("collapsed");

        if ($("#sidebar").hasClass("collapsed")) {
            sessionStorage.setItem('sidebarCollapsed', 'true');
        } else {
            sessionStorage.setItem('sidebarCollapsed', 'false');
        }

        setTimeout(function () {
            $("#sidebar").removeClass("animate");
            $(".main").removeClass("animate-sidebar");
        }, 250);
    });
});

// RETAIN SIDEBAR STATE WHEN GOING TO A DIFFERENT PAGE
$(document).ready(function () {
    if (sessionStorage.getItem('sidebarCollapsed') === 'true') {
        $("#sidebar").addClass("collapsed");
    } else if (sessionStorage.getItem('sidebarCollapsed') === 'false') {
        $("#sidebar").removeClass("collapsed");
    }
});

// CHANGE DASHBOARD TITLE TO THE PAGE
$(document).ready(function () {
    $("#sidebar .sidebar-link").click(function () {
        var pageTitle = $(this).data("title");
        $("#page-title").text(pageTitle);
    });
});

// REMOVE BLUR BACKGROUND OF MODALS WHEN HIDDEN
$(document).ready(function () {
    $('.modal').on('hide.bs.modal', function () {
        $(this).find(':focus').blur();
    });
    
    $('.modal').on('hidden.bs.modal', function () {
        document.activeElement.blur();
    });
});

// TOAST GREETINGS
$(document).ready(function () {
    $('.toast').each(function () {
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
            lengthChange: true,
            searching: true,
            lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
            dom: '<"row"<"col-sm-12"tr>><"row"<"col-sm-12 col-md-5"l><"col-sm-12 col-md-2"i><"col-sm-12 col-md-5 d-flex justify-content-end"p>>',
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                },
                {
                    targets: -1,
                    orderable: false,
                },
            ],
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


$("#registerIdNumber, #editIdNumber").on("keypress input", function (e) {
    if (e.type === "keypress" && !/[0-9\-]/.test(e.key)) {
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
$(document).ready(function () {
    if (!window.APP_CONFIG || !window.APP_CONFIG.DEFAULT_PROFILE_IMAGE) {
        return;
    }

    const DEFAULT_PROFILE_IMAGE = window.APP_CONFIG.DEFAULT_PROFILE_IMAGE;
    
    $("#registerStudentForm").submit(function (e) {
        e.preventDefault();
        $("#registerStudentForm input").removeClass("is-invalid");

        var formData = new FormData(this);

        $.ajax({
            url: $(this).attr("action"),
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    $("#registerStudentModal").modal("hide");
                    sessionStorage.setItem('showRegisterStudentSuccess', 'true');
                    location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function (xhr) {
                if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
                    const response = xhr.responseJSON;

                    if (response.field == "id_number") {
                        $("#registerIdNumber").addClass("is-invalid");
                        $("#registerIdNumberError").text(response.message).show();
                        $("#registerIdNumber").focus();
                    } else if (response.field == "student_photo") {
                        alert("Photo Error: " + response.message);
                    } else {
                        alert("Error: " + response.message);
                    }
                } else if (xhr.status === 403) {
                    alert("CSRF token validation failed. Please refresh the page and try again.");
                } else {
                    alert("Error: Something went wrong");
                }
            }
        });
    });

    $("#registerStudentModal").on("hidden.bs.modal", function () {
        $("#registerStudentForm")[0].reset();
        $("#registerStudentForm input").removeClass("is-invalid");
        $("#registerStudentForm .invalid-feedback").hide().text("");
        
        $('#registerImagePreview').attr('src', DEFAULT_PROFILE_IMAGE);
        $('#clearRegisterImage').hide();
    });
});

// IMAGE PREVIEW FOR REGISTER STUDENT MODAL
$(document).ready(function() {
    $('#studentPhoto').on('change', function(e) {
        const file = e.target.files[0];
        
        $('#photoError').hide().text('');
        $(this).removeClass('is-invalid');
        
        if (file) {
            const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg'];
            if (!validTypes.includes(file.type)) {
                $('#photoError').text('Please select a valid image file (JPG, PNG, or GIF)').show();
                $(this).addClass('is-invalid');
                $(this).val('');
                return;
            }
            
            const maxSize = 5 * 1024 * 1024;
            if (file.size > maxSize) {
                $('#photoError').text('File size must be less than 5MB').show();
                $(this).addClass('is-invalid');
                $(this).val('');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#registerImagePreview').attr('src', e.target.result).show();
                $('#registerPhotoPlaceholder').hide();
                $('#clearRegisterImage').show();
            }
            reader.readAsDataURL(file);
        }
    });
    
    $('#clearRegisterImage').on('click', function() {
        $('#studentPhoto').val('');
        $('#registerImagePreview').hide();
        $('#registerPhotoPlaceholder').show();
        $(this).hide();
        $('#photoError').hide().text('');
        $('#studentPhoto').removeClass('is-invalid');
    });
    
    $('#registerStudentModal').on('hidden.bs.modal', function () {
        $('#registerStudentForm')[0].reset();
        $('#registerImagePreview').hide();
        $('#registerPhotoPlaceholder').show();
        $('#clearRegisterImage').hide();
        $('#studentPhoto').val('');
        $('#registerStudentForm input').removeClass('is-invalid');
        $('#registerStudentForm .invalid-feedback').hide().text('');
        $('#photoError').hide().text('');
    });
});


// POPULATE STUDENT DETAILS MODAL
$(document).ready(function() {
    if (!window.APP_CONFIG || !window.APP_CONFIG.DEFAULT_PROFILE_IMAGE) {
        return;
    }

    const DEFAULT_PROFILE_IMAGE = window.APP_CONFIG.DEFAULT_PROFILE_IMAGE;
    
    $('#student-table tbody').on('click', 'tr', function(e) {
        if ($(e.target).closest('.btn-edit, .btn-delete, a, button').length) {
            return;
        }
        
        const row = $(this);
        const idNumber = row.data('id-number');
        const firstName = row.data('first-name');
        const lastName = row.data('last-name');
        const fullName = `${firstName} ${lastName}`;
        const gender = row.data('gender');
        const yearLevel = row.data('year-level');
        const program = row.data('program-code');
        const photoUrl = row.data('photo-url');
        
        const isDefaultOrNoPhoto = !photoUrl || 
                                   photoUrl === '' || 
                                   photoUrl === 'None' || 
                                   photoUrl === 'null' || 
                                   photoUrl === DEFAULT_PROFILE_IMAGE;
        
        $('#details-id-number').val(idNumber);
        $('#details-full-name').val(fullName);
        $('#details-gender').val(gender);
        $('#details-year-level').val(yearLevel);
        $('#details-program').val(program);
        
        if (isDefaultOrNoPhoto) {
            $('#detailsStudentPhoto').hide();
            $('#detailsPhotoPlaceholder').show();
        } else {
            $('#detailsStudentPhoto').attr('src', photoUrl).show();
            $('#detailsPhotoPlaceholder').hide();
        }
        
        $('#studentDetailsModal').modal('show');
    });
    
    $('#studentDetailsModal').on('hidden.bs.modal', function () {
        $('#detailsStudentPhoto').hide();
        $('#detailsPhotoPlaceholder').show();
    });
});


//POPULATE STUDENT EDIT FORM
$(document).ready(function () {
    if (!window.APP_CONFIG || !window.APP_CONFIG.DEFAULT_PROFILE_IMAGE) {
        return;
    }
    
    const DEFAULT_PROFILE_IMAGE = window.APP_CONFIG.DEFAULT_PROFILE_IMAGE;
    
    $('#editStudentModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modal = $(this);

        var idNumber = button.data('id-number');
        var firstName = button.data('first-name');
        var lastName = button.data('last-name');
        var gender = button.data('gender');
        var yearLevel = button.data('year-level');
        var program = button.data('program-code');
        var photoUrl = button.data('photo-url');

        modal.find('#editIdNumber').val(idNumber);
        modal.find('#editFirstName').val(firstName);
        modal.find('#editLastName').val(lastName);
        modal.find('#editGender').val(gender);
        modal.find('#editYearLevel').val(yearLevel);
        modal.find('#editProgramCode').val(program);
        modal.find('#originalIdNumber').val(idNumber);
        modal.find('#currentPhotoUrl').val(photoUrl);
        
        const isDefaultOrNoPhoto = !photoUrl || 
                                   photoUrl === '' || 
                                   photoUrl === 'None' || 
                                   photoUrl === 'null' || 
                                   photoUrl === DEFAULT_PROFILE_IMAGE;
        
        if (!isDefaultOrNoPhoto) {
            $('#editImagePreview').attr('src', photoUrl).show();
            $('#editPhotoPlaceholder').hide();
            $('#removePhotoBtn').show().prop('disabled', false).html('<i class="bi bi-trash"></i> Remove Photo');
        } else {
            $('#editImagePreview').hide();
            $('#editPhotoPlaceholder').show();
            $('#removePhotoBtn').hide();
        }
        
        $('#clearEditImage').hide();
        $('#removePhotoFlag').val('false');
        
        modal.data('originalPhotoUrl', photoUrl);
        modal.data('isDefaultPhoto', isDefaultOrNoPhoto);
    });
});


//SHOW EDIT STUDENT CONFIRMATION MESSAGE
$(document).ready(function () {
    $('#editStudentForm').submit(function (e) {
        e.preventDefault();
        $('#editStudentForm input').removeClass("is-invalid");

        var formData = new FormData(this);

        $.ajax({
            url: $(this).attr("action"),
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    $("#editStudentModal").modal("hide");
                    sessionStorage.setItem('showEditStudentSuccess', 'true');
                    location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function (xhr) {
                if ((xhr.status === 400 || xhr.status === 409) && xhr.responseJSON) {
                    const response = xhr.responseJSON;

                    if (response.message === "No changes detected.") {
                        $("#editStudentModal").modal("hide");
                        return;
                    }

                    if (response.field == "id_number") {
                        $("#editIdNumber").addClass("is-invalid");
                        $("#editIdNumberError").text(response.message).show();
                        $("#editIdNumber").focus();
                    } else if (response.field == "student_photo") {
                        alert("Photo Error: " + response.message);
                    } else {
                        alert("Error: " + response.message);
                    }
                } else if (xhr.status === 403) {
                    alert("CSRF token validation failed. Please refresh the page and try again.");
                } else {
                    alert("Error: Something went wrong");
                }
            }
        });
    });

    $("#editStudentModal").on("hidden.bs.modal", function () {
        $("#editStudentForm")[0].reset();
        $("#editStudentForm input").removeClass("is-invalid");
        $("#editStudentForm .invalid-feedback").hide().text("");
        
        $('#editImagePreview').hide();
        $('#editPhotoPlaceholder').show();
        $('#clearEditImage').hide();
        $('#removePhotoBtn').hide();
        $('#editStudentPhoto').val('');
        $('#removePhotoFlag').val('false');
    });
});

// IMAGE PREVIEW FOR EDIT STUDENT MODAL
$(document).ready(function() {
    if (!window.APP_CONFIG || !window.APP_CONFIG.DEFAULT_PROFILE_IMAGE) {
        return;
    }

    const DEFAULT_PROFILE_IMAGE = window.APP_CONFIG.DEFAULT_PROFILE_IMAGE;
    
    $('#editStudentPhoto').on('change', function(e) {
        const file = e.target.files[0];
        
        $('#editPhotoError').hide().text('');
        $(this).removeClass('is-invalid');
        
        if (file) {
            const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg'];
            if (!validTypes.includes(file.type)) {
                $('#editPhotoError').text('Please select a valid image file (JPG, PNG, or GIF)').show();
                $(this).addClass('is-invalid');
                $(this).val('');
                return;
            }
            
            const maxSize = 5 * 1024 * 1024;
            if (file.size > maxSize) {
                $('#editPhotoError').text('File size must be less than 5MB').show();
                $(this).addClass('is-invalid');
                $(this).val('');
                return;
            }

            $('#removePhotoFlag').val('false');
            
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#editImagePreview').attr('src', e.target.result).show();
                $('#editPhotoPlaceholder').hide();
                $('#removePhotoBtn').show().prop('disabled', false).html('<i class="bi bi-trash"></i> Remove Photo');
                $('#clearEditImage').hide();
            }
            reader.readAsDataURL(file);
        }
    });
    
    $('#removePhotoBtn').on('click', function() {
        const isDefaultPhoto = $('#editStudentModal').data('isDefaultPhoto');

        $('#removePhotoFlag').val('true');
        $('#editStudentPhoto').val('');
        $('#editImagePreview').hide();
        $('#editPhotoPlaceholder').show();
        $(this).hide();
        $('#editPhotoError').hide().text('');
        $('#editStudentPhoto').removeClass('is-invalid');
    });
    
    $('#editStudentModal').on('hidden.bs.modal', function () {
        $('#editPhotoError').hide().text('');
        $('#editStudentPhoto').removeClass('is-invalid');
    });
});


/// POPULATE HIDDEN INPUT
$(document).ready(function () {
    $('#deleteStudentModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var idNumber = button.data('id-number');

        $(this).find('#deleteIdNumber').val(idNumber);
    });
});


// SHOW DELETE STUDENT CONFIRMATION MESSAGE
$(document).ready(function () {
    $("#deleteStudentForm").submit(function (e) {
        e.preventDefault();

        $.post($(this).attr("action"), $(this).serialize(), function (response) {
            if (response.success) {
                $("#deleteStudentModal").modal("hide");

                sessionStorage.setItem('showDeleteStudentSuccess', 'true');

                location.reload();

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
});


$(document).ready(function () {
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
$(document).ready(function () {
    $("#registerProgramForm").submit(function (e) {
        e.preventDefault();
        $("#registerProgramForm input").removeClass("is-invalid");

        $.post($(this).attr("action"), $(this).serialize(), function (response) {
            if (response.success) {
                $("#registerProgramModal").modal("hide");

                sessionStorage.setItem('showRegisterProgramSuccess', 'true');

                location.reload();

            } else {
                alert(response.message);
            }
        }).fail(function (xhr) {
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

    $("#registerProgramModal").on("hidden.bs.modal", function () {
        $("#registerProgramForm")[0].reset();
        $("#registerProgramForm input").removeClass("is-invalid");
        $("#registerProgramForm .invalid-feedback").hide().text("");
    });
});


// SHOW/POPULATE EDIT PROGRAM MODAL
$(document).ready(function () {
    $('#editProgramModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modal = $(this);

        var programCode = button.data('program-code');
        var programName = button.data('program-name');
        var collegeCode = button.data('college-code');

        modal.find('#editProgramCode').val(programCode);
        modal.find('#editProgramName').val(programName);
        modal.find('#editCollegeCode').val(collegeCode);
        modal.find('#originalProgramCode').val(programCode);
        modal.find('#originalProgramName').val(programName);
    });
});


// SHOW EDIT PROGRAM CONFIRMATION MESSAGE
$(document).ready(function () {
    $('#editProgramForm').submit(function (e) {
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

    $("#editProgramModal").on("hidden.bs.modal", function () {
        $("#editProgramForm")[0].reset();
        $("#editProgramForm input").removeClass("is-invalid");
        $("#editProgramForm .invalid-feedback").hide().text("");
    });
});


/// POPULATE HIDDEN INPUT
$(document).ready(function () {
    $('#deleteProgramModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var code = button.data('program-code');

        $(this).find('#deleteProgramCode').val(code);
    });
});


// SHOW DELETE PROGRAM CONFIRMATION MESSAGE
$(document).ready(function () {
    $("#deleteProgramForm").submit(function (e) {
        e.preventDefault();

        $.post($(this).attr("action"), $(this).serialize(), function (response) {
            if (response.success) {
                $("#deleteProgramModal").modal("hide");

                sessionStorage.setItem('showDeleteProgramSuccess', 'true');

                location.reload();

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
});


$(document).ready(function () {
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
$(document).ready(function () {
    $("#registerCollegeForm").submit(function (e) {
        e.preventDefault();
        $("#registerCollegeForm input").removeClass("is-invalid");

        $.post($(this).attr("action"), $(this).serialize(), function (response) {
            if (response.success) {
                $("#registerCollegeModal").modal("hide");

                sessionStorage.setItem('showRegisterCollegeSuccess', 'true');

                location.reload();

            } else {
                alert(response.message);
            }
        }).fail(function (xhr) {
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

    $("#registerCollegeModal").on("hidden.bs.modal", function () {
        $("#registerCollegeForm")[0].reset();
        $("#registerCollegeForm input").removeClass("is-invalid");
        $("#registerCollegeForm .invalid-feedback").hide().text("");
    });
});

// SHOW/POPULATE COLLEGE EDIT FORM
$(document).ready(function () {
    $('#editCollegeModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modal = $(this);

        var collegeCode = button.data('college-code');
        var collegeName = button.data('college-name');

        modal.find('#editCollegeCode').val(collegeCode);
        modal.find('#editCollegeName').val(collegeName);
        modal.find('#originalCollegeCode').val(collegeCode);
        modal.find('#originalCollegeName').val(collegeName);
    });
});


// SHOW EDIT COLLEGE CONFIRMATION MESSAGE
$(document).ready(function () {
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

    $("#editCollegeModal").on("hidden.bs.modal", function () {
        $("#editCollegeForm")[0].reset();
        $("#editCollegeForm input").removeClass("is-invalid");
        $("#editCollegeForm .invalid-feedback").hide().text("");
    });
});


// POPULATE HIDDEN INPUT
$(document).ready(function () {
    $('#deleteCollegeModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var code = button.data('college-code');

        $(this).find('#deleteCollegeCode').val(code);
    });
});


// SHOW DELETE COLLEGE CONFIRMATION MESSAGE
$(document).ready(function () {
    $("#deleteCollegeForm").submit(function (e) {
        e.preventDefault();

        $.post($(this).attr("action"), $(this).serialize(), function (response) {
            if (response.success) {
                $("#deleteCollegeModal").modal("hide");

                sessionStorage.setItem('showDeleteCollegeSuccess', 'true');

                location.reload();

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
});

$(document).ready(function () {
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