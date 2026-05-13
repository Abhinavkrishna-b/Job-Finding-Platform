// Tab Switching
function switchTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab content and activate button
    document.getElementById(tabId + 'Tab').classList.add('active');
    document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
}

// Modal Functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Toast Notification
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// Personal Info Form Submission
function savePersonalInfo(event) {
    event.preventDefault();
    
    // Update values
    document.getElementById('fullName').textContent = 
        document.getElementById('editFirstName').value + ' ' + 
        document.getElementById('editLastName').value;
    document.getElementById('email').textContent = document.getElementById('editEmail').value;
    document.getElementById('phone').textContent = document.getElementById('editPhone').value;
    document.getElementById('gender').textContent = document.getElementById('editGender').value;
    document.getElementById('dob').textContent = document.getElementById('editDob').value;
    
    // Close modal and show notification
    closeModal('personalInfoModal');
    showToast('Personal information updated successfully');
}

// Academic Info Form Submission
function saveAcademicInfo(event) {
    event.preventDefault();
    
    // Update values
    document.getElementById('tenthPercentage').textContent = document.getElementById('editTenthPercentage').value;
    document.getElementById('twelfthPercentage').textContent = document.getElementById('editTwelfthPercentage').value;
    document.getElementById('ugCgpa').textContent = document.getElementById('editUgCgpa').value;
    document.getElementById('backlogsHistory').textContent = document.getElementById('editBacklogsHistory').value;
    document.getElementById('currentBacklogs').textContent = document.getElementById('editCurrentBacklogs').value;
    document.getElementById('placementInterest').textContent = document.getElementById('editPlacementInterest').value;
    
    // Close modal and show notification
    closeModal('academicInfoModal');
    showToast('Academic information updated successfully');
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Initialize with academic tab active
document.addEventListener('DOMContentLoaded', () => {
    switchTab('academic');
});