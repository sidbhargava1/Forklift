export type AuthState = {
  enabled: boolean;
  isLoading: boolean;
  isAuthenticated: boolean;
  userEmail: string | null;
  login: () => Promise<void>;
  logout: () => void;
  getAccessToken: () => Promise<string | null>;
};
