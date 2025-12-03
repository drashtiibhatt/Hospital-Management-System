// Hospital Management System - Main JavaScript File

// ========================================
// 1. UTILITY FUNCTIONS
// ========================================

/**
 * Show loading spinner on button
 */
function showButtonLoading(button, text = 'Loading...') {
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        ${text}
    `;
}

/**
 * Hide loading spinner on button
 */
function hideButtonLoading(button) {
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHTML;
    toastContainer.appendChild(toastElement.firstElementChild);

    const toast = new bootstrap.Toast(toastElement.firstElementChild);
    toast.show();

    // Remove toast element after it's hidden
    toastElement.firstElementChild.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-IN', options);
}

/**
 * Format time to readable string
 */
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========================================
// 2. FORM VALIDATION
// ========================================

/**
 * Validate email format
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone number (10 digits)
 */
function validatePhone(phone) {
    const re = /^[0-9]{10}$/;
    return re.test(phone);
}

/**
 * Validate password strength
 */
function validatePassword(password) {
    return password.length >= 6;
}

/**
 * Real-time form validation
 */
document.addEventListener('DOMContentLoaded', function() {
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                this.classList.add('is-invalid');
                showFieldError(this, 'Please enter a valid email address');
            } else {
                this.classList.remove('is-invalid');
                hideFieldError(this);
            }
        });
    });

    // Phone validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !validatePhone(this.value)) {
                this.classList.add('is-invalid');
                showFieldError(this, 'Please enter a valid 10-digit phone number');
            } else {
                this.classList.remove('is-invalid');
                hideFieldError(this);
            }
        });
    });

    // Password confirmation
    const confirmPasswordInputs = document.querySelectorAll('input[name="confirm_password"]');
    confirmPasswordInputs.forEach(input => {
        const passwordInput = document.querySelector('input[name="password"]');
        if (passwordInput) {
            input.addEventListener('input', function() {
                if (passwordInput.value !== this.value) {
                    this.setCustomValidity('Passwords do not match');
                    this.classList.add('is-invalid');
                    showFieldError(this, 'Passwords do not match');
                } else {
                    this.setCustomValidity('');
                    this.classList.remove('is-invalid');
                    hideFieldError(this);
                }
            });
        }
    });
});

function showFieldError(input, message) {
    let errorDiv = input.parentElement.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

function hideFieldError(input) {
    const errorDiv = input.parentElement.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// ========================================
// 3. SEARCH FUNCTIONALITY
// ========================================

/**
 * Live search for tables
 */
function initTableSearch() {
    const searchInputs = document.querySelectorAll('.search-box input');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', debounce(function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.card').querySelector('table tbody');

            if (table) {
                const rows = table.querySelectorAll('tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        }, 300));
    });
}

// ========================================
// 4. CONFIRMATION DIALOGS
// ========================================

/**
 * Confirm dangerous actions
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Add confirmation to delete buttons
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to delete this?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});

// ========================================
// 5. DYNAMIC DATE CONSTRAINTS
// ========================================

/**
 * Set minimum and maximum dates for date inputs
 */
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date to today for appointment bookings
    const appointmentDateInputs = document.querySelectorAll('input[name="appointment_date"]');
    appointmentDateInputs.forEach(input => {
        const today = new Date();
        const todayStr = today.toISOString().split('T')[0];
        input.min = todayStr;

        // Set max date to 7 days from now
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 7);
        const maxDateStr = maxDate.toISOString().split('T')[0];
        input.max = maxDateStr;
    });

    // Set max date to today for date of birth
    const dobInputs = document.querySelectorAll('input[name="date_of_birth"]');
    dobInputs.forEach(input => {
        const today = new Date().toISOString().split('T')[0];
        input.max = today;
    });
});

// ========================================
// 6. FLASH MESSAGES AUTO-DISMISS
// ========================================

/**
 * Auto-dismiss flash messages after 5 seconds
 */
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// ========================================
// 7. FORM SUBMISSION LOADING STATE
// ========================================

/**
 * Show loading state on form submission
 */
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form:not(.no-loading)');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && this.checkValidity()) {
                showButtonLoading(submitButton, 'Submitting...');
            }
        });
    });
});

// ========================================
// 8. SMOOTH SCROLLING
// ========================================

/**
 * Smooth scroll to anchors
 */
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// ========================================
// 9. TOOLTIPS & POPOVERS INITIALIZATION
// ========================================

/**
 * Initialize Bootstrap tooltips and popovers
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// ========================================
// 10. DATA TABLE ENHANCEMENTS
// ========================================

/**
 * Add sorting to table headers
 */
function initTableSorting() {
    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
        });
    });
}

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aText = a.cells[column].textContent.trim();
        const bText = b.cells[column].textContent.trim();
        return aText.localeCompare(bText);
    });

    rows.forEach(row => tbody.appendChild(row));
}

// ========================================
// 11. CLIPBOARD COPY
// ========================================

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'danger');
    });
}

// Add copy buttons to code elements
document.addEventListener('DOMContentLoaded', function() {
    const codeElements = document.querySelectorAll('code');
    codeElements.forEach(code => {
        if (code.textContent.length > 10) {
            code.style.cursor = 'pointer';
            code.title = 'Click to copy';
            code.addEventListener('click', function() {
                copyToClipboard(this.textContent);
            });
        }
    });
});

// ========================================
// 12. PRINT FUNCTIONALITY
// ========================================

/**
 * Print specific element
 */
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const printWindow = window.open('', '', 'height=600,width=800');
        printWindow.document.write('<html><head><title>Print</title>');
        printWindow.document.write('<link rel="stylesheet" href="/static/css/style.css">');
        printWindow.document.write('</head><body>');
        printWindow.document.write(element.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }
}

// ========================================
// 13. CHARACTER COUNTER
// ========================================

/**
 * Add character counter to textareas
 */
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('small');
        counter.className = 'text-muted d-block text-end';
        textarea.parentElement.appendChild(counter);

        function updateCounter() {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} characters remaining`;
        }

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
});

// ========================================
// 14. RESPONSIVE NAVBAR
// ========================================

/**
 * Close mobile menu when clicking outside
 */
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        document.addEventListener('click', function(event) {
            const isClickInside = navbarCollapse.contains(event.target) ||
                                 navbarToggler.contains(event.target);

            if (!isClickInside && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    }
});

// ========================================
// 15. INITIALIZE ALL FUNCTIONS
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Hospital Management System initialized');

    // Initialize table search
    initTableSearch();

    // Initialize table sorting (if needed)
    initTableSorting();

    // Log initialization complete
    console.log('All JavaScript modules loaded successfully');
});

// ========================================
// 16. EXPORT FUNCTIONS FOR GLOBAL USE
// ========================================

window.HMS = {
    showToast,
    showButtonLoading,
    hideButtonLoading,
    confirmAction,
    copyToClipboard,
    printElement,
    formatDate,
    formatTime,
    validateEmail,
    validatePhone,
    validatePassword
};
