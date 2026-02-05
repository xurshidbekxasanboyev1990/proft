/**
 * Validate email format
 * @param {string} email 
 * @returns {boolean}
 */
export function isValidEmail(email) {
  if (!email) return false
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate phone number (Uzbekistan format)
 * @param {string} phone 
 * @returns {boolean}
 */
export function isValidPhone(phone) {
  if (!phone) return false
  const phoneRegex = /^\+998[0-9]{9}$/
  return phoneRegex.test(phone.replace(/\s/g, ''))
}

/**
 * Validate password strength
 * @param {string} password 
 * @returns {{ isValid: boolean, errors: string[] }}
 */
export function validatePassword(password) {
  const errors = []
  
  if (!password || password.length < 8) {
    errors.push('Parol kamida 8 belgidan iborat bo\'lishi kerak')
  }
  
  if (password && !/[A-Z]/.test(password)) {
    errors.push('Parolda kamida bitta katta harf bo\'lishi kerak')
  }
  
  if (password && !/[a-z]/.test(password)) {
    errors.push('Parolda kamida bitta kichik harf bo\'lishi kerak')
  }
  
  if (password && !/[0-9]/.test(password)) {
    errors.push('Parolda kamida bitta raqam bo\'lishi kerak')
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

/**
 * Validate required field
 * @param {any} value 
 * @param {string} fieldName 
 * @returns {string|null}
 */
export function validateRequired(value, fieldName = 'Bu maydon') {
  if (value === null || value === undefined || value === '') {
    return `${fieldName} to'ldirilishi shart`
  }
  if (typeof value === 'string' && value.trim() === '') {
    return `${fieldName} to'ldirilishi shart`
  }
  return null
}

/**
 * Validate minimum length
 * @param {string} value 
 * @param {number} min 
 * @param {string} fieldName 
 * @returns {string|null}
 */
export function validateMinLength(value, min, fieldName = 'Bu maydon') {
  if (!value || value.length < min) {
    return `${fieldName} kamida ${min} belgidan iborat bo'lishi kerak`
  }
  return null
}

/**
 * Validate maximum length
 * @param {string} value 
 * @param {number} max 
 * @param {string} fieldName 
 * @returns {string|null}
 */
export function validateMaxLength(value, max, fieldName = 'Bu maydon') {
  if (value && value.length > max) {
    return `${fieldName} ${max} belgidan oshmasligi kerak`
  }
  return null
}
