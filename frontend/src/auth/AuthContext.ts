import { createContext } from "react";

import type { AuthState } from "./types";

export const disabledAuthState: AuthState = {
  enabled: false,
  isLoading: false,
  isAuthenticated: false,
  userEmail: null,
  login: async () => {},
  logout: () => {},
  getAccessToken: async () => null,
};

export const AuthContext = createContext<AuthState>(disabledAuthState);
