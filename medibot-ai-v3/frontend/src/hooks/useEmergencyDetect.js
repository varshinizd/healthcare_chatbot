import { useState, useEffect } from 'react'
import { detectEmergencyClient } from '../constants/emergencyKeywords'

export function useEmergencyDetect(inputText) {
  const [emergencyWarning, setEmergencyWarning] = useState(null)

  useEffect(() => {
    if (!inputText || inputText.length < 8) {
      setEmergencyWarning(null)
      return
    }
    const result = detectEmergencyClient(inputText)
    if (result.isEmergency) {
      setEmergencyWarning(result.matchedKeyword)
    } else {
      setEmergencyWarning(null)
    }
  }, [inputText])

  return emergencyWarning
}
