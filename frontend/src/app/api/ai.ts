import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';

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
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to generate AI explanation');
  }

  return data;
}