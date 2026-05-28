import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';
import { Subject, Duration, GroupSize } from '../types/activity'; 

export interface AIRecommendationExplanationRequest {
  teacher_profile: unknown;
  class_profile: unknown;
  activities: unknown[];
  recommendation_reasons?: unknown[];
}

export interface AIActivityExplanation {
  activity_id: string;
  title: string;
  explanation: string;
  teacher_guidance: string;
  adaptation: string;
}

export interface AIRecommendationExplanationResponse {
  success: boolean;
  summary: string;
  activity_explanations: AIActivityExplanation[];
  recommendation_reasons?: unknown[];
  source: string;
}

export interface AdaptActivityRequest {
  activity: {
    title: string;
    subject: string;
    duration: string;
    groupSize: string;
    description: string;
    materials: string[];
    instructions: string[];
    learningGoals: string[];
  };
  teacher_profile?: {
    name?: string;
    years_experience?: string;
    specializations?: string[];
    teaching_style?: string;
  };
  class_profile?: {
    class_name?: string;
    age_group?: string;
    class_size?: number;
    learning_focus?: string[];
    available_resources?: string[];
    special_needs?: string[];
  };
  adaptation_prompt: string;
}

export interface AdaptActivityDraft {
    title: string;
    subject: Subject;
    duration: Duration;
    groupSize: GroupSize;
    description: string;
    materials: string[];
    instructions: string[];
    learningGoals: string[];
    assessmentQuestions?: string[];
    differentiationNotes?: string;
    familyCommunityNotes?: string;
    learningOutcomesSummary?: string;
}

export interface AdaptActivityResponse {
  activity_draft: AdaptActivityDraft;
  source: string;
}

export async function explainRecommendations(
  payload: AIRecommendationExplanationRequest
): Promise<AIRecommendationExplanationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ai/explain-recommendations`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yap.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'YZ açıklaması oluşturulamadı.');
  }

  return data;
}

export async function adaptActivity(
  payload: AdaptActivityRequest
): Promise<AdaptActivityResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ai/adapt-activity`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yap.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Etkinlik uyarlanamadı.');
  }

  return data;
}