// GovAid JavaScript Functions

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize form validation
    initializeFormValidation();

    // Add loading states to buttons
    initializeButtonLoading();

    // Initialize scheme card interactions
    initializeSchemeCards();
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Add loading state to submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    addLoadingState(submitBtn);
                }
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Button Loading States
function initializeButtonLoading() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                addLoadingState(submitBtn);
            }
        });
    });
}

function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Processing...';
    button.disabled = true;

    // Reset after 10 seconds (fallback)
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 10000);
}

// Scheme Cards Interactions
function initializeSchemeCards() {
    const schemeCards = document.querySelectorAll('.scheme-card, .card');

    schemeCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Profile Form Functions
function validateProfileForm() {
    const form = document.querySelector('form');
    const role = document.querySelector('input[name="role"]')?.value || 
                 document.querySelector('#role')?.value || 
                 (window.location.pathname.includes('profile') ? getUserRole() : null);

    if (role === 'student') {
        return validateStudentForm();
    } else if (role === 'entrepreneur') {
        return validateEntrepreneurForm();
    }

    return true;
}

function validateStudentForm() {
    const requiredFields = ['state', 'category', 'annual_income', 'dob', 'gender', 'education_level', 'course'];
    return validateRequiredFields(requiredFields);
}

function validateEntrepreneurForm() {
    const requiredFields = ['state', 'age', 'industry_type', 'startup_stage', 'funding_needs'];
    return validateRequiredFields(requiredFields);
}

function validateRequiredFields(fields) {
    let isValid = true;

    fields.forEach(fieldName => {
        const field = document.querySelector(`[name="${fieldName}"]`);
        if (field && !field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else if (field) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }
    });

    return isValid;
}

function getUserRole() {
    // Extract user role from session or page context
    const roleElement = document.querySelector('[data-role]');
    return roleElement ? roleElement.dataset.role : null;
}

// Utility Functions
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const alertElement = document.createElement('div');
    alertElement.innerHTML = alertHTML;
    alertContainer.insertBefore(alertElement.firstElementChild, alertContainer.firstElementChild);
}

function hideElement(element) {
    element.style.display = 'none';
}

function showElement(element) {
    element.style.display = 'block';
}

// Dashboard Functions
function refreshSchemes() {
    const refreshBtn = document.querySelector('#refresh-schemes');
    if (refreshBtn) {
        addLoadingState(refreshBtn);
        // Reload the page to get fresh schemes
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
}

// Search and Filter Functions
function filterSchemes(searchTerm) {
    const schemeCards = document.querySelectorAll('.scheme-card');
    const searchLower = searchTerm.toLowerCase();

    schemeCards.forEach(card => {
        const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
        const provider = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
        const eligibility = card.querySelector('.eligibility')?.textContent.toLowerCase() || '';

        if (title.includes(searchLower) || provider.includes(searchLower) || eligibility.includes(searchLower)) {
            card.style.display = 'block';
            card.classList.add('fade-in');
        } else {
            card.style.display = 'none';
        }
    });
}

// Role Switching Confirmation
function confirmRoleSwitch(newRole) {
    const currentRole = getUserRole() || 'current';
    const message = `Are you sure you want to switch from ${currentRole} to ${newRole}? This will redirect you to update your profile.`;

    return confirm(message);
}

// Copy to Clipboard Function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Link copied to clipboard!', 'success');
    }).catch(function() {
        showAlert('Failed to copy link.', 'error');
    });
}

// Enhanced Error Handling
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);
    // You could send this to a logging service
});

// Performance Monitoring
window.addEventListener('load', function() {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log('Page load time:', loadTime + 'ms');
});

// Service Worker Registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js');
    });
}
