export const EMERGENCY_KEYWORDS = [
  // Cardiac
  'chest pain', 'heart attack', 'cardiac arrest', 'myocardial',
  // Neurological
  'stroke', 'face drooping', 'arm weakness', 'slurred speech', 'seizure', 'convulsion',
  'passed out', 'fainted', 'unconscious', 'loss of consciousness',
  // Respiratory
  "can't breathe", 'cannot breathe', 'not breathing', 'stopped breathing',
  'choking', 'airway blocked', 'asthma attack', 'severe shortness of breath',
  // Toxicological
  'overdose', 'poisoning', 'poisoned', 'took too many pills', 'ingested too much',
  // Psychiatric
  'suicide', 'suicidal', 'want to die', 'kill myself', 'end my life',
  'self-harm', 'cutting myself', 'no reason to live',
  // Trauma
  'severe bleeding', "can't stop the bleeding", 'serious accident', 'spinal injury',
  // Allergic
  'anaphylaxis', 'severe allergic reaction', 'throat swelling', 'tongue swelling',
]

export function detectEmergencyClient(text) {
  const lower = text.toLowerCase()
  const matched = EMERGENCY_KEYWORDS.find((kw) => lower.includes(kw))
  return { isEmergency: !!matched, matchedKeyword: matched || null }
}
