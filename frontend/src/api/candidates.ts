import { requestJson } from './client'

export type CandidateSkillInput = {
  name: string
  proficiency?: string
}

export type CandidateProfile = {
  summary: string
  skills: CandidateSkillInput[]
  location?: string
  years_experience?: number
}

export type MatchReason = {
  type: string
  message: string
}

export type MatchResult = {
  match_id: number | null
  job_id: number | null
  job_title: string
  source_name: string
  match_score: number
  matching_skills: string[]
  missing_skills: string[]
  confidence: number
  reasons: MatchReason[]
}

export function matchCandidate(
  profile: CandidateProfile,
  signal?: AbortSignal,
): Promise<MatchResult[]> {
  return requestJson<MatchResult[]>('/v1/candidates/matches', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
    signal,
  })
}
