/* ==========================================
   ARISE LEARNING ERP
   Common JavaScript Functions
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    console.log("Arise Learning ERP Loaded Successfully");

    // Auto hide alerts
    autoHideAlerts();

    // Confirm delete actions
    confirmDeleteButtons();

    // Form validation
    validateForms();

});

/* ==========================================
   Auto Hide Flash Messages
========================================== */

function autoHideAlerts() {

    const alerts = document.querySelectorAll(
        ".success-alert, .alert"
    );

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "0.5s";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 3000);

    });

}

/* ==========================================
   Confirm Delete
========================================== */

function confirmDeleteButtons() {

    const deleteButtons =
        document.querySelectorAll(".btn-delete");

    deleteButtons.forEach(function (btn) {

        btn.addEventListener("click", function (e) {

            let confirmDelete = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmDelete) {
                e.preventDefault();
            }

        });

    });

}

/* ==========================================
   Search Table Function
========================================== */

function searchTable(inputId, tableId) {

    let input =
        document.getElementById(inputId);

    let filter =
        input.value.toUpperCase();

    let table =
        document.getElementById(tableId);

    let rows =
        table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {

        let text =
            rows[i].textContent ||
            rows[i].innerText;

        if (
            text.toUpperCase()
                .indexOf(filter) > -1
        ) {
            rows[i].style.display = "";
        }
        else {
            rows[i].style.display = "none";
        }

    }

}

/* ==========================================
   Form Validation
========================================== */

function validateForms() {

    const forms =
        document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (e) {

                let requiredFields =
                    form.querySelectorAll(
                        "[required]"
                    );

                let valid = true;

                requiredFields.forEach(
                    function (field) {

                        if (
                            field.value.trim() === ""
                        ) {

                            field.style.border =
                                "2px solid red";

                            valid = false;

                        }
                        else {

                            field.style.border =
                                "1px solid #ccc";

                        }

                    }
                );

                if (!valid) {

                    e.preventDefault();

                    alert(
                        "Please fill all required fields."
                    );

                }

            }
        );

    });

}

/* ==========================================
   Mobile Sidebar Toggle
========================================== */

function toggleSidebar() {

    const sidebar =
        document.querySelector(".sidebar");

    if (!sidebar) return;

    sidebar.classList.toggle("show");

}

/* ==========================================
   Current Date
========================================== */

function setCurrentDate() {

    const dateElement =
        document.getElementById("currentDate");

    if (!dateElement) return;

    let today = new Date();

    let options = {
        day: "numeric",
        month: "long",
        year: "numeric"
    };

    dateElement.innerHTML =
        today.toLocaleDateString(
            "en-IN",
            options
        );

}

setCurrentDate();

/* ==========================================
   Number Formatting
========================================== */

function formatCurrency(amount) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR"
        }
    ).format(amount);

}

/* ==========================================
   Dashboard Notification
========================================== */

function showNotification(message) {

    let notification =
        document.createElement("div");

    notification.className =
        "erp-notification";

    notification.innerHTML =
        message;

    document.body.appendChild(
        notification
    );

    setTimeout(function () {

        notification.style.opacity = "0";

        setTimeout(function () {

            notification.remove();

        }, 500);

    }, 3000);

}

/* ==========================================
   Student Search
========================================== */

function searchStudents() {

    searchTable(
        "searchInput",
        "studentTable"
    );

}

/* ==========================================
   Fee Search
========================================== */

function searchFees() {

    searchTable(
        "feeSearch",
        "feeTable"
    );

}

/* ==========================================
   Attendance Search
========================================== */

function searchAttendance() {

    searchTable(
        "attendanceSearch",
        "attendanceTable"
    );

}