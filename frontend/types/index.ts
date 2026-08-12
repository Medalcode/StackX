export interface UserWeights {
  weights: Record<string, number>;
  proyecto?: string;
}

export interface TeamSuggestion {
  role: string;
  count: number;
}

export interface RecommendationItem {
  name: string;
  category?: string;
  final_score: number;
  justification?: string;
  team_suggestion?: TeamSuggestion[];
}

export interface RecommendationResponse {
  recommendations: RecommendationItem[];
}

export interface PaginatedRecommendationResponse {
  recommendations: RecommendationItem[];
  skip: number;
  limit: number;
}

export interface FavoriteItem {
  id: number;
  name: string;
  weights: Record<string, number>;
  proyecto?: string;
}
