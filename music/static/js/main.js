/**
 * Main JavaScript file for Song Info Finder
 * Provides common UI functionality and utilities
 */

// Global variables
let currentLoadingMessage = "Processing...";

/**
 * Show a global snackbar/toast message
 * @param {string} message - The message to display
 * @param {string} type - The type of message (success, error, warning, info)
 * @param {number} duration - Duration in milliseconds (default: 3000)
 */
function showSnackbar(message, type = "info", duration = 3000) {
  const snackbar = document.getElementById("globalSnackbar");
  const messageEl = document.getElementById("snackbarMessage");

  if (!snackbar || !messageEl) {
    console.warn("Snackbar elements not found");
    return;
  }

  // Clear previous classes
  snackbar.classList.remove(
    "text-bg-success",
    "text-bg-danger",
    "text-bg-warning",
    "text-bg-info"
  );

  // Set message and type
  messageEl.textContent = message;

  // Add appropriate styling based on type
  switch (type) {
    case "success":
      snackbar.classList.add("text-bg-success");
      break;
    case "error":
      snackbar.classList.add("text-bg-danger");
      break;
    case "warning":
      snackbar.classList.add("text-bg-warning");
      break;
    case "info":
    default:
      snackbar.classList.add("text-bg-info");
      break;
  }

  // Show the snackbar
  snackbar.style.display = "block";
  const toast = new bootstrap.Toast(snackbar, { delay: duration });
  toast.show();

  // Hide after duration
  setTimeout(() => {
    snackbar.style.display = "none";
  }, duration + 100);
}

/**
 * Show loading overlay
 * @param {string} message - Loading message to display
 */
function showLoading(message = "Processing...") {
  currentLoadingMessage = message;
  const loading = document.getElementById("globalLoading");
  const loadingText = loading?.querySelector(".loading-text");

  if (loading) {
    if (loadingText) {
      loadingText.textContent = message;
    }
    loading.style.display = "flex";
  }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
  const loading = document.getElementById("globalLoading");
  if (loading) {
    loading.style.display = "none";
  }
}

/**
 * Show error message
 * @param {string} message - Error message
 * @param {string} title - Error title (optional)
 */
function showError(message, title = "Error") {
  showSnackbar(`${title}: ${message}`, "error");
}

/**
 * Show success message
 * @param {string} message - Success message
 */
function showSuccess(message) {
  showSnackbar(message, "success");
}

/**
 * Show warning message
 * @param {string} message - Warning message
 */
function showWarning(message) {
  showSnackbar(message, "warning");
}

/**
 * Show info message
 * @param {string} message - Info message
 */
function showInfo(message) {
  showSnackbar(message, "info");
}

/**
 * Format file size in human readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

/**
 * Format duration in MM:SS format
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration
 */
function formatDuration(seconds) {
  if (!seconds || isNaN(seconds)) return "00:00";

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
    .toString()
    .padStart(2, "0")}`;
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
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

/**
 * Throttle function to limit function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
function throttle(func, limit) {
  let inThrottle;
  return function () {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} Success status
 */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showSuccess("Copied to clipboard!");
    return true;
  } catch (err) {
    console.error("Failed to copy text: ", err);
    showError("Failed to copy to clipboard");
    return false;
  }
}

/**
 * Validate file path
 * @param {string} path - File path to validate
 * @returns {boolean} Is valid path
 */
function isValidFilePath(path) {
  if (!path || typeof path !== "string") return false;

  // Basic validation - check for common file extensions
  const validExtensions = [".mp3", ".MP3"];
  const hasValidExtension = validExtensions.some((ext) =>
    path.toLowerCase().endsWith(ext)
  );

  // Check for basic path structure
  const hasPathStructure =
    path.includes("/") || path.includes("\\") || path.includes(":");

  return hasValidExtension && hasPathStructure;
}

/**
 * Get file extension from path
 * @param {string} path - File path
 * @returns {string} File extension
 */
function getFileExtension(path) {
  if (!path) return "";
  const lastDot = path.lastIndexOf(".");
  return lastDot > 0 ? path.substring(lastDot + 1).toLowerCase() : "";
}

/**
 * Sanitize HTML string to prevent XSS
 * @param {string} str - String to sanitize
 * @returns {string} Sanitized string
 */
function sanitizeHTML(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Add fade-in animation to element
 * @param {HTMLElement} element - Element to animate
 */
function addFadeInAnimation(element) {
  if (element) {
    element.classList.add("fade-in");
  }
}

/**
 * Remove fade-in animation from element
 * @param {HTMLElement} element - Element to remove animation from
 */
function removeFadeInAnimation(element) {
  if (element) {
    element.classList.remove("fade-in");
  }
}

/**
 * Initialize common UI elements
 */
function initializeUI() {
  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Add fade-in animation to cards
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    setTimeout(() => {
      addFadeInAnimation(card);
    }, index * 100);
  });

  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize popovers
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
}

/**
 * Handle form submission with loading state
 * @param {HTMLFormElement} form - Form element
 * @param {string} loadingMessage - Loading message to show
 */
function handleFormSubmission(form, loadingMessage = "Processing...") {
  if (!form) return;

  form.addEventListener("submit", function (e) {
    showLoading(loadingMessage);

    // Hide loading after form submission (will be overridden by AJAX if needed)
    setTimeout(() => {
      hideLoading();
    }, 1000);
  });
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  initializeUI();

  // Global error handler
  window.addEventListener("error", function (e) {
    console.error("Global error:", e.error);
    showError("An unexpected error occurred. Please try again.");
  });

  // Handle unhandled promise rejections
  window.addEventListener("unhandledrejection", function (e) {
    console.error("Unhandled promise rejection:", e.reason);
    showError("An unexpected error occurred. Please try again.");
    e.preventDefault();
  });
});

// Export functions for use in other scripts
window.UI = {
  showSnackbar,
  showLoading,
  hideLoading,
  showError,
  showSuccess,
  showWarning,
  showInfo,
  formatFileSize,
  formatDuration,
  debounce,
  throttle,
  copyToClipboard,
  isValidFilePath,
  getFileExtension,
  sanitizeHTML,
  addFadeInAnimation,
  removeFadeInAnimation,
  handleFormSubmission,
};
